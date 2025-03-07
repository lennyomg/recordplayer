import board
import analogio
from uart import uart

PIN_VOLUME = board.A0

input = analogio.AnalogIn(PIN_VOLUME)
num_readings = 5
readings = [0] * num_readings
index = 0
total = 0
value = 0
prev_value = None

def read():
    global index, total, value, prev_value
    total -= readings[index]
    readings[index] = input.value
    total += readings[index]
    index = (index + 1) % num_readings
    prev_value = value
    value = 100 - int(100 * total / num_readings / 65000)
    return value

def send():
    try:
        uart.write(bytes([value]))
    except:
        print("cannot write uart")

    

    

    