# Course: Blockchain and Decentralised Applicatons
# Project: Tool for monitoring nodes in Qtum network
# Author: Jakub Kubik (xkubik32)
# Date: 23.04.2022

import logging

USER = "test"
PASSWORD = "test1234"

LOCALHOST_NODE = 'http://127.0.0.1:3889'

FORMAT = "%(levelname)-2s %(asctime)s %(message)s"
logging.basicConfig(filename='monitor.log', level=logging.INFO, format=FORMAT)

MAX_CONNECTED_PEERS = 10

OUTPUT_FILENAME = "peers_info_ipv4.json"
POT_PEERS_FILENAME = "address_reader/potential_peers_db.json"
