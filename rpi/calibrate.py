#!/usr/bin/env python3

from time import sleep, monotonic
import socket

from punch import SolenoidDriver

class PunchyDriver():

    NEUTRAL_POSITION_Z = 15  # mm above the workpiece where the needle touches the surface

    def __init__(self):

        self.sd = SolenoidDriver()

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)                   
        self.socket.connect(("10.1.1.5", 23))                
        # Wait for grbl to wake up
        sleep(2)

        self.cur_z = self.NEUTRAL_POSITION_Z

        while True:
            r = self.receive()
            if r.startswith("Grbl"):
                break

        print("GRBL ready")

    def init_machine(self):
        sleep(1)
        while True:
            if not self.send_cmd("$X"):
                print("unlock failed. try again.")
                sleep(1)
                continue
            break

    def receive(self):
        while True:
            resp = self.socket.recv(80)
            if len(resp) == 0:
                sleep(.0001)
                continue
            break

        resp = str(resp, "ascii")
        #print("r [%s]" % resp.strip())
        return resp.strip()

    def send(self, s):
        #print("s [%s]" % s)
        self.socket.send(bytes(s + "\n", "ascii"))

    def send_cmd(self, cmd):

        self.send(cmd)
        while True:
            resp = self.receive()
            if resp.startswith("ok"):
                return True

            if resp.startswith("error"):
                return False

    def wait_for_idle(self):
        while True:
            self.send("?")
            info = self.receive()
            resp = self.receive()
            if info.startswith("<Idle") and resp == "ok":
                return True


    def move(self, x=None, y=None, z=None):
        cmd = "G21G00"

        if x is not None:
            cmd += "X%.5f" % x
        if y is not None:
            cmd += "Y%.5f" % y
        if z is not None:
            cmd += "Z%.5f" % z

        self.send_cmd(cmd)

    def move_to_punchy_home(self):
        self.move(x=0, y=0, z=self.NEUTRAL_POSITION_Z)

    def calibrate_depth(self, x, y, start_ms, end_ms):
        for i, p in enumerate(range(start_ms, end_ms, 2)):
            self.move(x+(i * 10), y)
            self.wait_for_idle()
            self.sd.punch(p)
            sleep(.01)

    def punch_grid(self, x_offset, y_offset, rows, cols, step):

        for r in range(rows):
            for c in range(cols):
                self.move(x_offset + (c * step), y_offset + (r * step))
                self.wait_for_idle()
                self.sd.punch(22)
                sleep(.01)

pd = PunchyDriver()
pd.init_machine()
pd.move_to_punchy_home()
#pd.calibrate_depth(0, 0, 16, 30)
pd.punch_grid(0, 0, 5, 5, 10)
pd.move_to_punchy_home()
