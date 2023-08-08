# Qtum_monitor

Qtum_monitor is a platform for monitoring active nodes in Qtum blockchain network.
```
.
├── Dockerfile_addresses_reader
├── Dockerfile_monitor
├── Dockerfile_node
├── docker-compose.yaml                 # Handles all 3 services (node, monitor and addresses_reader)
├── README.md                   
├── requirements.txt                    # Python requirements
├── app/
    ├── config.py                       # Credentials for and hardcoded values for configuration 
    ├── monitor.py                      # Main module for monitor service
    ├── monitor.log                     # Logs from monitor service
    ├── peers_info_ipv4.json            # Used peers with its metadata
    ├── potential_peers_db.py           # Monitor service - merges peers.dat with available peers from grpc method `getnodeaddresses` 
    ├── requests_wrapper.py             # Monitor service - wrapper that handles all grpc requests
    ├── utils.py                        # Monitor service - usefull functions
    ├── address_reader/
        ├── address_reader.sh           # Main module for address_reader service
        ├── potential_peers_db.json     # Parsed peers by address_reader 
    ├── qtumd/
        ├── debug.log                   # Debugging logs from running client node
        ├── peers.dat                   # Binary database with `gossiped` peers
└──
``` 

## Project setup instructions
### Installation:
```bash
# export path to clonned project
export PROJECT_PATH=path

# build all images
docker-compose build node
docker-compose build monitor
docker-compose build address_reader
```

### Running all services:

```bash
docker-compose up -d node
docker-compose up -d address_reader
docker-compose up monitor
```

## Author
- [Jakub Kubík](https://github.com/Jakub-Kubik)