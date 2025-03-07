import board
import busio

uart = busio.UART(board.TX, board.RX, baudrate=9600, timeout=0)
