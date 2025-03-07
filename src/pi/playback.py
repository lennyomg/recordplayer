import board
import media
import light
import motor
import library
import uart
import busio
import syslog
from time import sleep
from digitalio import DigitalInOut, Pull
from rotaryio import IncrementalEncoder
from traceback import print_exc, format_exc
from adafruit_debouncer import Button, Debouncer
from adafruit_pn532.spi import PN532_SPI

PIN_SWITCH_MUTE = board.D5
PIN_SWITCH_MODE = board.D6
PIN_ROTARY_FORWARD = board.D16
PIN_ROTARY_BACKWARD = board.D20
PIN_ROTARY_CLICK = board.D13

OUTPUTS = [
    ["0"],
    ["95475557245033"],
]


def error():
    exc = format_exc()
    print(exc)
    light.error()
    sleep(1)
    light.stopped()


def outputs_volume(outputs: list[str], volume: int):
    try:
        for item in outputs:
            media.volume(item, volume)
    except:
        error()


def outputs_enable(outputs: list[str]):
    try:
        for i in range(15):
            loaded = [p["id"] for p in media.outputs()["outputs"]]
            if all([id in loaded for id in outputs]):
                print(f"output ready {outputs}")
                break
            sleep(0.5)

        media.set_outputs(outputs)
    except:
        error()


def queue(id):

    data: dict[str, str] = library.playlists.get(id)
    if not data:
        print(f"no data for {id}, add new tag to library")
        syslog.syslog(syslog.LOG_WARNING, f"new tag {id}")
        return

    print("queue", data)
    try:
        media.queue(data)
        media.repeat("all")
    except:
        error()
        return

    light.playing()
    motor.forward(motor.PWM_DUTY_CYCLE_FAST)
    sleep(1)
    motor.forward()


def stop():

    print("stop")
    try:
        media.stop()
    except:
        error()
        return

    light.stopped()
    motor.stop()


def pause():

    print("toogle")
    try:
        playing = media.player()["state"] == "play"
    except:
        error()
        return

    if playing:
        print("pause")
        try:
            media.pause()
        except:
            error()
            return
        motor.stop()
        light.stopped()
    else:
        print("resume")
        try:
            media.play()
        except:
            error()
            return
        motor.forward()
        light.playing()


def next():
    print("next track")
    motor.forward(motor.PWM_DUTY_CYCLE_FAST)
    try:
        media.next()
    except:
        error()
    finally:
        motor.forward()


def previous():
    print("previous track")
    motor.backward()
    try:
        media.previous()
    except:
        error()
    finally:
        motor.forward()


def init():

    print("waiting for media server")
    light.loading()
    motor.stop()

    while True:
        sleep(0.5)
        try:
            if media.library()["updating"] == False:
                print("library updated")
                break
        except:
            pass

    print("media server ready")
    light.stopped()


def daemon_control():

    output_pin = DigitalInOut(PIN_SWITCH_MODE)
    output_pin.switch_to_input(Pull.UP)

    mute_pin = DigitalInOut(PIN_SWITCH_MUTE)
    mute_pin.switch_to_input(Pull.UP)

    rotary_pin = DigitalInOut(PIN_ROTARY_CLICK)
    rotary_pin.switch_to_input(Pull.UP)
    rotary_btn = Button(rotary_pin)

    rotary_enc = IncrementalEncoder(PIN_ROTARY_FORWARD, PIN_ROTARY_BACKWARD)
    rotary_dec = Debouncer(lambda: False, interval=0.05)
    rotary_inc = Debouncer(lambda: False, interval=0.05)
    rotary_pos = 0

    volume = 10
    output = -1

    while True:

        volume_changed = False
        if mute_pin.value:
            if volume != 0:
                print("mute")
                volume = 0
                volume_changed = True
        else:
            try:
                tmp = uart.write_read(21)
            except:
                tmp = None
                print_exc()
            if tmp != None:
                if abs(volume - tmp) > 2:
                    print("volume", tmp)
                    volume = tmp
                    volume_changed = True
            else:
                print("volume error")

        output_changed = False
        if not output_pin.value and output != 0:
            output = 0
            output_changed = True
            print("output", output)

        if output_pin.value and output != 1:
            output = 1
            output_changed = True
            print("output", output)

        rotary_btn.update()
        if rotary_btn.pressed:
            print("rotary pressed")
            pause()

        if output_changed:
            print("output changed")
            outputs_enable(OUTPUTS[output])
            outputs_volume(OUTPUTS[output], volume)

        if volume_changed and not output_changed:
            print("volume changed")
            outputs_volume(OUTPUTS[output], volume)

        rotary_inc.update(rotary_pos < rotary_enc.position)
        rotary_dec.update(rotary_pos > rotary_enc.position)
        rotary_pos = rotary_enc.position

        if rotary_inc.rose:
            print("rotary increased")
            next()

        if rotary_dec.rose:
            print("rotary decreased")
            previous()

        sleep(0.1)


def daemon_rfid():

    spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
    cs_pin = DigitalInOut(board.CE0)
    pn532 = PN532_SPI(spi, cs_pin, debug=False)
    pn532.SAM_configuration()
    uid: str = None

    while True:

        sleep(0.5)

        uid_read = pn532.read_passive_target(timeout=0.5)
        if uid_read:
            uid_read_str = uid_read.hex()
            if uid_read_str != uid:
                uid = uid_read_str
                print("nfc tag placed", uid)
                queue(uid)
        elif uid:
            uid = None
            print("nfc tag removed")
            stop()
