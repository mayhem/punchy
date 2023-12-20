#!/usr/bin/env python3

from time import sleep
from gerbil import Gerbil

def my_callback(eventstring, *data):
    args = []
    for d in data:
        args.append(str(d))
    print("MY CALLBACK: event={} data={}".format(eventstring.ljust(30), ", ".join(args)))
    # Now, do something interesting with these callbacks

grbl = Gerbil(my_callback)
grbl.setup_logging()
grbl.cnect("/dev/ttyAMA0", 115200)
grbl.poll_start()

sleep(2)
print("move!")
grbl.send_immediately("G0 X200")
