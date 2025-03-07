import uart
import sys


def off():
    uart.write(11)


def error():
    uart.write(12)


def playing():
    uart.write(13)


def stopped():
    uart.write(14)


def loading():
    uart.write(15)


if __name__ == "__main__":
    locals()[sys.argv[1]]()
