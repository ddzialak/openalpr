#from ubuntu:14.04
from resin/rpi-raspbian


# Install prerequisites
run apt-get update && apt-get install -y \
    build-essential \
    cmake \
    curl \
    git \
    libcurl3-dev \
    libleptonica-dev \
    liblog4cplus-dev \
    libopencv-dev \
    libtesseract-dev \
    wget

# Copy all data
copy . /srv/openalpr

# Setup the build directory
run mkdir /srv/openalpr/src/build
workdir /srv/openalpr/src/build

# Setup the compile environment
run cmake -DCMAKE_INSTALL_PREFIX:PATH=/usr -DCMAKE_INSTALL_SYSCONFDIR:PATH=/etc ..

# Compile the library
run make

# Install the binaries/libraries to your local system (prefix is /usr)
run make install

run apt-get -y install python-psutil

workdir /

EXPOSE 23432

entrypoint ["/srv/openalpr/scripts/alpr_pipes2net.py"]

