openalpr
========

OpenALPR is an open source *Automatic License Plate Recognition* library written in C++ with bindings in C#, Java, and Python.  The library analyzes images and video streams to identify license plates.  The output is the text representation of any license plate characters.

Check out a live online demo here: http://www.openalpr.com/demo-image.html

User Guide
-----------

If you don't know what openalpr is please see details on original project's page: [openalpr/openalpr](https://github.com/openalpr/openalpr)

This branch support openalpr as a service on RPi in docker.
Basic idea:
 - run openalpr in container (with shared volume: /mnt/data)
 - wait for incomming connection on port 23432
 - read a path to processed file (usually /mnt/data/some-picture.jpg)
 - process file with openalpr with parameters -j (json) -e eu (europen plates) -p pl (region)
 - send json response to the client

