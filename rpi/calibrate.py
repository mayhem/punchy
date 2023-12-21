#!/usr/bin/env python3

from time import sleep, monotonic
from gerbil import Gerbil

_pd = None

def grbl_callback(event, *data):
    if _pd is not None:
        _pd.callback(event, *data)


class PunchyDriver():

    NEUTRAL_POSITION_Z = 15  # mm above the workpiece where the needle touches the surface

    def __init__(self):
        global _pd

        self.grbl = Gerbil(grbl_callback)
        _pd = self
        self.grbl.setup_logging()
        self.grbl.cnect("/dev/ttyAMA0", 115200)
        self.grbl.poll_start()

        # Wait for grbl to wake up
        sleep(2)

    def callback(self, event, *data):
        args = []
        for d in data:
            args.append(str(d))
        print("callback: event={} data={}".format(event.ljust(30), ", ".join(args)))

        if event == "on_alarm":
            print("ALARM!")
        if event == "on_error":
            print("ERROR!")


    def init_machine(self):
        print("init machine!")
        self.grbl.send_immediately("$X")
        sleep(2)

        # select mm, 200 feed rate
        self.grbl.stream("G21F200")

    def move_z_axis_to_neutral(self):
        print("move z!")
#        self.grbl.stream("G00X-20")
#        self.grbl.stream("G00Z-%d" % self.NEUTRAL_POSITION_Z)
        self.grbl.job_new()
        self.grbl.stream("G00X10 G00Y10 G00Z5 G00X-10 G00Y-10 G00Z-5")


pd = PunchyDriver()
pd.init_machine()
pd.move_z_axis_to_neutral()
print("idle")
sleep(5)
