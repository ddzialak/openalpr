#!/bin/bash

cd "$(dirname '$0')/.."
source scripts/config
docker build -t ${DOCKER_IMAGE} .

