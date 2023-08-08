# Course: Blockchain and Decentralised Applicatons
# Project: Tool for monitoring nodes in Qtum network
# Author: Jakub Kubik (xkubik32)
# Date: 23.04.2022

def is_ipv6(ip: str) -> bool:
    """Check if ip string is IPv6 or not."""
    return len(ip.split(":")) > 2
