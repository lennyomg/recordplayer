import board
import pwmio

PWM_FREQUENCY = 30
PWM_DUTY_CYCLE_SLOW = 5000
PWM_DUTY_CYCLE_FAST = 20000
PIN_FORWARD = board.D24
PIN_BACKWARD = board.D23

motor_forward = pwmio.PWMOut(PIN_FORWARD, frequency=PWM_FREQUENCY)
motor_backward = pwmio.PWMOut(PIN_BACKWARD, frequency=PWM_FREQUENCY)


def backward():
    motor_backward.duty_cycle = PWM_DUTY_CYCLE_FAST
    motor_forward.duty_cycle = 0


def forward(speed=PWM_DUTY_CYCLE_SLOW):
    motor_forward.duty_cycle = speed
    motor_backward.duty_cycle = 0


def stop():
    motor_backward.duty_cycle = 0
    motor_forward.duty_cycle = 0


if __name__ == "__main__":
    forward()
    while True:
        pass
