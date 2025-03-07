import serial
import threading

uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=1)
lock = threading.Lock()


def write(command: int):
    with lock:
        uart.write(bytes([command]))


def write_read(command: int):
    with lock:
        uart.write(bytes([command]))
        data = uart.read(1)
        return data[0] if data else None
