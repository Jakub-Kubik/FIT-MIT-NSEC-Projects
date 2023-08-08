# Course: Blockchain and Decentralised Applicatons
# Project: Tool for monitoring nodes in Qtum network
# Author: Jakub Kubik (xkubik32)
# Date: 23.04.2022
# Inspired by: https://github.com/fruit098/crypto_monitor/blob/master/app/request_wrapper.py

import logging
import json
import requests

from config import USER, PASSWORD

log = logging.getLogger(__name__)


class RequestWrapper:
    def __init__(self, rpc_address: str):
        self.rpc_address = rpc_address

    def _request_node(self, method: str, params: list=[]) -> list:
        try:
            response = requests.post(
                self.rpc_address,
                data=json.dumps({"method": method, "params": params}),
                auth=(USER, PASSWORD),
            )
            parsed_response = response.json()
            result = parsed_response["result"]
            if parsed_response["error"]:
                log.info(f"_request_node.error_from_node {parsed_response['error']}")
            else:
                log.info("_request_node.response_from_node_ok")
        except Exception:
            log.exception("_request_node")
            result = []

        return result

    def post_new_peer(self, address: str) -> None:
        log.info(f"_request_node.post_new_peer.address-{address}")

        payload = {
            "method": "addnode",
            "params": [
                address,
                "onetry",
            ],
        }
        self._request_node(**payload)

    def disconnect_peer(self, address: str) -> None:
        log.info(f"_request_node.disconnect_peer.address-{address}")

        payload = {
            "method": "disconnectnode",
            "params": [
                address,
            ],
        }
        self._request_node(**payload)

    def fetch_addresses(self) -> list:
        log.info("_request_node.fetch_addresses")

        return self._request_node("getnodeaddresses", [2500, ])

    def fetch_active_peers(self) -> list:
        log.info("_request_node.fetch_active_peers")

        return self._request_node(method="getpeerinfo")
