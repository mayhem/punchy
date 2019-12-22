#!/usr/bin/env python3

import sys
import os
from time import sleep

import click
import serial

BAUD_RATE = 115200

class CommandException(Exception):
    pass

def open_serial(device):
    try:
        ser = serial.Serial(device,
            BAUD_RATE,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=.01)
    except serial.serialutil.SerialException as err:
        print("Failed to open serial port %s" % device, str(err))
        return None

    print("wait until shit warms up...")
    sleep(3)

    while True:
        if not ser.in_waiting:
            break

        ser.read()

    return ser


def dump(s):
    for ch in s:
        print("%d" % ord(ch))
    print()


def readline(ser):

    while True:
        resp = ser.readline().decode('utf-8')
        resp = resp.replace("\n", "")
        resp = resp.replace("\r", "")
        if not resp:
            continue

        break

    return resp


def send_cmd(ser, cmd):
    cmd += "\n"
    ser.write(bytes(cmd, 'utf-8'))
    resp = readline(ser)
    if resp != "ok":
        print("'%s'" % resp)
        raise CommandException(resp)



@click.command()
@click.argument("device", nargs=1)
def main(device):

    ser = open_serial(device)
    if not ser:
        return

    print("opened serial port")

    try:
        send_cmd(ser, "$H")
        send_cmd(ser, "G0 X40 Y0")
        send_cmd(ser, "G0 X40 Y40")
        send_cmd(ser, "G0 X0 Y40")
        send_cmd(ser, "G0 X0 Y0")

    except CommandException as err:
        print("command exception: %s" % str(err))
    else:
        print("program completed successfully.")

    ser.close()


def usage(command):
    with click.Context(command) as ctx:
        click.echo(command.get_help(ctx))


if __name__ == "__main__":
    main()
    sys.exit(0)
