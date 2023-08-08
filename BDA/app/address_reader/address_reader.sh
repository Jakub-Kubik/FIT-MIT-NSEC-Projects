#!/bin/bash
# Course: Blockchain and Decentralised Applicatons
# Project: Tool for monitoring nodes in Qtum network
# Author: Jakub Kubik (xkubik32)
# Date: 23.04.2022

BITPEERS_PATH="/go/bin/"
BINARY_PEERS_PATH="${PROJECT_PATH}/app/qtumd/peers.dat"
OUTPUT_FILE='/app/address_reader/potential_peers_db.json'
FORMAT='json'

SLEEP_SECONDS=$((15 * 60))

echo $BITPEERS_PATH

cd $BITPEERS_PATH

BITPEERS='bitpeers'
chmod '+x' $BITPEERS

COUNTER=1
COMMAND="${BITPEERS} '--filepath' $BINARY_PEERS_PATH '--format' $FORMAT > $OUTPUT_FILE"
while true
do
  echo '======================================================================================================'
  eval $COMMAND

  echo $COMMAND
  echo "executed $COUNTER times"
  COUNTER=$(($COUNTER + 1))

  echo "Sleep for $SLEEP_SECONDS"
  sleep $SLEEP_SECONDS
done