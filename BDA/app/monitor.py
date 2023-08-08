# Course: Blockchain and Decentralised Applicatons
# Project: Tool for monitoring nodes in Qtum network
# Author: Jakub Kubik (xkubik32)
# Date: 23.04.2022

import time
import json
import logging

from potential_peers_db import load_potential_peers_from_db
from requests_wrapper import RequestWrapper
from utils import is_ipv6
from config import LOCALHOST_NODE, MAX_CONNECTED_PEERS, OUTPUT_FILENAME, POT_PEERS_FILENAME


def get_all_potential_peers() -> set:
    """Merge potential IPv4 addresses from peers.dat DB with requested potential peers."""

    potential_peers_db = load_potential_peers_from_db(POT_PEERS_FILENAME)
    potential_peers = set(potential_peers_db)

    potential_peers_request = RequestWrapper(LOCALHOST_NODE).fetch_addresses()
    if len(potential_peers_request) > 0:
        potential_peers_request = [f"{p['address']}:{p['port']}" for p in potential_peers_request]
        potential_peers_request = [p for p in potential_peers_request if not is_ipv6(p)]
        potential_peers.update(set(potential_peers_request))

    return potential_peers


def parse_connected_peer_data(connected_peer: dict, time: float) -> dict:
    """Parse connected peer data."""

    return {
        "addr": connected_peer["addr"],
        "services": connected_peer["servicesnames"],
        "version": connected_peer["version"],
        "subversion": connected_peer["subver"],
        "inbound": connected_peer["inbound"],
        "addnode": connected_peer["addnode"],
        "check_time": time,
    }


def monitor() -> None:
    """Main function for monitoring active IPv4 nodes in Qtum blockchain."""

    start_time = time.time()
    output_f = open(OUTPUT_FILENAME, "w")

    checked_peers = set()

    i = 1
    while True:
        logging.info(f"Iteration number: {i}")

        potential_peers = get_all_potential_peers()
        peers_for_check = potential_peers.difference(checked_peers)
        logging.info(f"Peers for check: {peers_for_check}")
        logging.info(f"Peers for check size: {len(peers_for_check)}")

        for potential_peer_address in peers_for_check:
            connected_peers = RequestWrapper(LOCALHOST_NODE).fetch_active_peers()
            logging.info(f"Connected peers: {len(connected_peers)}")

            # disconnect peer if required and save its properties if already not saved
            if len(connected_peers) >= MAX_CONNECTED_PEERS:
                connected_peer = connected_peers[0]
                connected_peer_addr = connected_peer["addr"]

                if connected_peer_addr not in checked_peers:
                    output_f.write(json.dumps(parse_connected_peer_data(connected_peer, time.time() - start_time)))
                    output_f.write("\n")
                    output_f.flush()

                    checked_peers.add(connected_peer_addr)

                RequestWrapper(LOCALHOST_NODE).disconnect_peer(connected_peer_addr)

            # add new peer
            a = RequestWrapper(LOCALHOST_NODE).post_new_peer(potential_peer_address)

            # check all connected peers and save its properties if required
            for connected_peer in connected_peers:
                addr = connected_peer["addr"]
                if addr in checked_peers:
                    continue

                output_f.write(json.dumps(parse_connected_peer_data(connected_peer, time.time() - start_time)))
                output_f.write("\n")
                output_f.flush()

                checked_peers.add(addr)

        i += 1


if __name__ == "__main__":
    monitor()
