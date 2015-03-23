#!/bin/bash

source "$(dirname '$0')/config"

if ! docker ps | grep -q -E " $CONTAINER_NAME *$" ;
then
    echo "Sorry, $CONTAINER_NAME is not running, try to restart-service.sh"
    exit 2
fi;

if [ $# == 1 ] ;
then
    IP=$(docker inspect $CONTAINER_NAME | grep IPAddress | cut -f2 -d: | tr '",' '  ')
    echo "Requesting container $CONTAINER_NAME with ip=$IP to analize: $1"
    echo $1 | nc -w30 $IP $SERVICE_PORT
else
    echo "Usage: $0 <path-to-file-available-under-container>"
    echo
    echo "You can list any directory from container with command: docker exec $CONTAINER_NAME ls \$DIRECTORY"
fi
