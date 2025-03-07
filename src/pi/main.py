import light
import motor
import playback
import syslog
from threading import Thread, Event
from traceback import format_exc

stop_event = Event()


def thread(func):
    try:
        func()
    except:
        e = format_exc()
        print(e)
        syslog.syslog(syslog.LOG_ERR, e)
        stop_event.set()


try:
    playback.init()
    Thread(target=lambda: thread(playback.daemon_control), daemon=True).start()
    Thread(target=lambda: thread(playback.daemon_rfid), daemon=True).start()
    stop_event.wait()
finally:
    light.error()
    motor.stop()
