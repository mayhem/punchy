import sys
import os

import click
import serial

BAUD_RATE = 115200

class CommandException(Exception):
    pass

def open_serial(device):
    try:
        log.info("Opening %s" % device)
        return serial.Serial(device,
            BAUD_RATE,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=.01)
    except serial.serialutil.SerialException as err:
        print("Failed to open serial port %s" % device, str(err))
        return None

def send_cmd(ser, cmd):
    ser.write(cmd)
    resp = ser.read()
    if resp != "ok":
        raise CommandException(resp)


@click.command()
@click.argument("device", nargs=1)
def main(device):

    ser = open_serial(device)
    if not ser:
        return

    try:
        send_cmd(ser, "$H")
        send_cmd(ser, "G0 X10 Y0")
        send_cmd(ser, "G0 X10 Y10")
        send_cmd(ser, "G0 X0 Y10")
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
