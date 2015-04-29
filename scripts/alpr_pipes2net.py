#!/usr/bin/python

import os
import select
import socket
import time
import psutil
from subprocess import Popen, PIPE

alpr = None

HOST=None
PORT=23432
COMMAND="/usr/bin/alpr -p pl -j -c eu"

def restart():
    global alpr
    global alpr_info

    if alpr:
        print ("Killing old pid [%s]" % alpr.pid)
        alpr.kill()
        print ("wait for process end")
        alpr.wait()

    alpr = Popen(COMMAND + " 2>&1", shell=True, stdin=PIPE, stdout=PIPE)
    alpr_info = psutil.Process(alpr.pid)


def read_no_block(pipe):
    s = ""
    while select.select([pipe], [], [], 0.1)[0] == [pipe]:
        s += str(os.read(pipe, 1))
    return s


def clear_output(pipe):
    s = read_no_block(pipe)
    for m in s.splitlines():
        print ("Dropped: ", m)

MAGIC_FILE="END_OF_PROCESSING"
END_MESSAGE="Image file not found: " + MAGIC_FILE
def get_output(timeout=30):
    if timeout:
        end_time = time.time() + timeout
    resp = ""
    while alpr_info.get_cpu_percent(interval=0.5) > 10 or not resp:
        new_data = read_no_block(alpr.stdout.fileno())
        new_data = new_data.replace("libdc1394 error: Failed to initialize libdc1394", "").strip()
        resp += new_data
        #if resp:
        #    alpr.stdin.write(MAGIC_FILE)
        #    alpr.stdin.flush()
        #if resp.endswith(END_MESSAGE):
        #    resp = resp[:-len(END_MESSAGE)]
        #    break

        if timeout and end_time < time.time():
            print ("Timeout... restarting")
            restart()
            break
        time.sleep(0.1)
    return resp


def wait_for_connection(data_processor):
    s = None
    for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC,
                  socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
        af, socktype, proto, canonname, sa = res
        try:
            s = socket.socket(af, socktype, proto)
        except socket.error as msg:
            s = None
            continue
        try:
            s.bind(sa)
            s.listen(1)
        except socket.error as msg:
            s.close()
            s = None
            continue
        break
    
    if s is None:
        print ('could not open socket')
        sys.exit(1)
    while 1:
        conn, addr = s.accept()
        print ('Connected by', addr)
        data = conn.recv(1024)
        if data:
            conn.send(data_processor(str(data).strip()+'\n'))
        conn.close()
    
def process(cmd):
    if not alpr or alpr.poll() is not None:
        restart()
    print ("Has command:", cmd)
    clear_output(alpr.stdout.fileno())
    print ("Sending to alpr")
    alpr.stdin.write(cmd)
    alpr.stdin.flush()

    print ("Reading response:")
    resp = get_output()

    print ("Has response:", resp)
    return resp


restart()
while 1:
    try:
        wait_for_connection(process)
    except KeyboardInterrupt:
        print "exiting..."
        break
    except Exception as ex:
        print ("Ops: %s" % str(ex))
        print ("Restarting server...")

