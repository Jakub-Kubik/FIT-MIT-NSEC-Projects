# Course: Blockchain and Decentralised Applicatons
# Project: Tool for monitoring nodes in Qtum network
# Author: Jakub Kubik (xkubik32)
# Date: 23.04.2022

import json

from utils import is_ipv6


def load_potential_peers_from_db(file: str) -> set:
    """Load and parse just IP v4 peers from adjusted peers db."""

    with open(file) as potential_peers_raw:
        potential_peers_json = json.load(potential_peers_raw)

    potential_peers = set()
    for key in ["new_addr_info", "tried_addr_info"]:
        for pot_peers in potential_peers_json[key]:
            x = pot_peers["address"]["ip"]

            if not is_ipv6(x):
                potential_peers.add(x)

    return potential_peers
