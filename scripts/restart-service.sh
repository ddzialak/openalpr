#!/bin/bash

set -e

source "$(dirname '$0')/config"

if docker ps | grep -q -E " $CONTAINER_NAME *$";
then
    ( set -x; docker kill $CONTAINER_NAME )
fi;
if docker ps -a | grep -q -E " $CONTAINER_NAME *$" ;
then
    ( set -x; docker rm $CONTAINER_NAME )
fi

docker run -d -v /tmp:/tmp --name "${CONTAINER_NAME}" `get_volumes_option` ${DOCKER_IMAGE}

