from adafruit_led_animation import color
from adafruit_led_animation.animation import Animation
from adafruit_led_animation.animation.comet import Comet
from adafruit_led_animation.animation.solid import Solid
from adafruit_led_animation.animation.chase import Chase
from adafruit_led_animation.sequence import AnimationSequence
import board
import neopixel

PIN_NEOPIXEL = board.A2

pixels = neopixel.NeoPixel(PIN_NEOPIXEL, 10, brightness=0.2, auto_write=False)
current: Animation = None

AMBER_DIM = (64, 25, 0)
AMBER_DIM_EXTRA = (41, 16, 0)


class ChaseFillAmber(Chase):

    def __init__(self, pixel_object, speed, color=color.AMBER, size=2, spacing=3, reverse=False, name=None):
        super().__init__(pixel_object, speed, color, size, spacing, reverse, name)

    @staticmethod
    def space_color(n, pixel_no=0):
        return AMBER_DIM


def off():
    global current
    current = Solid(pixels, color=color.BLACK)


def error():
    global current
    current = Solid(pixels, color=color.RED)


def stopped():
    global current
    current = Solid(pixels, color=AMBER_DIM_EXTRA)


def loading():
    global current
    current = Comet(
        pixels,
        speed=0.1,
        color=color.BLUE,
        background_color=(0, 0, 32),
        tail_length=4,
        bounce=True)


def playing():
    global current
    current = ChaseFillAmber(pixels, speed=0.1, size=4, spacing=32)
