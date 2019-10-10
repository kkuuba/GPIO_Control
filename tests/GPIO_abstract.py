from time import time
from datetime import datetime

OUT = "set as out"
BCM = "set pins in bcm mode"
HIGH = "set pin high"
LOW = "set pin low"


def output(gpio_pin, action):
    write_to_log_file(gpio_pin, action)


def setup(gpio_pin, action):
    write_to_log_file(gpio_pin, action)


def setmode(action):
    write_to_log_file(99, action)


def write_to_log_file(gpio_pin, task_string):
    file = open('log_test.txt', 'a+')
    time_stamp = datetime.fromtimestamp(time()).strftime('%Y-%m-%d %H:%M:%S')
    file.write(time_stamp + ' | ' + task_string + " | pin: " + str(gpio_pin) + ' \n')
    file.close()
