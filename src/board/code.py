from uart import uart
import volume
import light
import gc

commands = {
    11: light.off,
    12: light.error,
    13: light.playing,
    14: light.stopped,
    15: light.loading,
    21: volume.send
}

light.loading()

while True:

    volume.read()

    try:
        data = uart.read(1)
        if data:
            commands[data[0]]()
    except:
        print("uart error")

    if light.current:
        light.current.animate()

