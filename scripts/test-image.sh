#!/bin/bash

source "$(dirname '$0')/config"

if [ $# == 1 ] && [ -e "$1" ] ;
then
    from_dir="`dirname \"$1\"`"
    from_dir="`readlink -f \"$from_dir\"`"
    fname="`basename \"$1\"`"
    echo "dir=$from_dir fname=$fname"
    echo "set -x; /usr/bin/alpr -p pl -c eu \"/data/$fname\"" | docker run -i --rm -v "$from_dir:/data:ro"  --entrypoint "/bin/bash" $DOCKER_IMAGE
else
    echo "Usage: $0 <filename>" >&2
    exit 1
fi

