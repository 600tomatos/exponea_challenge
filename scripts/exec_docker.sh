#!/bin/bash

docker exec -it $(docker ps | awk '/exponea_api/ {print $1}') bash