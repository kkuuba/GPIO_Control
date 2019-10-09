from time import time
from datetime import datetime


def output(gpio_pin, action):
    write_to_log_file(action, gpio_pin)


def setup(gpio_pin, action):
    write_to_log_file(action, gpio_pin)


def OUT():
    return "set as out"


def HIGH():
    return "set high state"


def LOW():
    return "set low state"


def write_to_log_file(task_string, gpio_pin):
    file = open('log_test.txt', 'a+')
    time_stamp = datetime.fromtimestamp(time()).strftime('%Y-%m-%d %H:%M:%S')
    file.write(time_stamp + ' | ' + task_string + ' | ' + 'Setting ' +
               str(gpio_pin) + ' gpio pin HIGH on 1000 ms interval\n')
    file.close()
