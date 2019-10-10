import socket
from time import sleep, time
from datetime import datetime

try:
    import RPi.GPIO as GPIO
except ImportError:
    import tests.GPIO_abstract as GPIO


def get_ip_address_of_current_device():
    """
    Returns local ip address of current device.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip


def _gpio_impulse_task(gpio_pin_id, duration):
    """
    Set defined gpio pin high with duration interval.
    """
    GPIO.output(gpio_pin_id, GPIO.HIGH)
    sleep(duration)
    GPIO.output(gpio_pin_id, GPIO.LOW)
    sleep(1)


def _gpio_change_state_task(gpio_pin_id, task_data):
    """
    Switch state of defined gpio pin.
    """
    if task_data == "on":
        GPIO.output(gpio_pin_id, GPIO.HIGH)
        sleep(1)
    if task_data == "off":
        GPIO.output(gpio_pin_id, GPIO.LOW)
        sleep(1)


def start_raspberry_gpio_task(gpio_pin_id, gpio_action_string):
    """
    Start equal gpio task in dependency of gpio_action_string.
    """
    print("starting gpio task ...\n")
    if gpio_action_string == "impulse":
        _gpio_impulse_task(gpio_pin_id, 1)
    else:
        _gpio_change_state_task(gpio_pin_id, gpio_action_string)


def prepare_raspberry_gpio(raspberry_gpio_pins):
    GPIO.setmode(GPIO.BCM)
    for gpio_pin in raspberry_gpio_pins:
        GPIO.setup(gpio_pin, GPIO.OUT)
        GPIO.output(gpio_pin, GPIO.LOW)


def save_logging_info_to_log_file(task_string, gpio_pin, client_ip):
    """
    Write gpio task to log file with all specified information about task.
    """
    file = open('log_info.txt', 'a+')
    time_stamp = datetime.fromtimestamp(time()).strftime('%Y-%m-%d %H:%M:%S')
    file.write(time_stamp + ' | ' + task_string + ' | ' + client_ip[0] + ' | ' + 'Setting ' +
               str(gpio_pin) + ' gpio pin HIGH on 1000 ms interval\n')
    file.close()


def create_task_list(config):
    task_list = list(config.keys())
    return task_list


def create_gpio_pin_list(config):
    gpio_pin_list = list(config.values())
    return gpio_pin_list


def create_android_app_cfg_string(config, destination_port, private_secret_key):
    task_list = list(config.keys())
    config_string = get_ip_address_of_current_device() + "#@#" + str(
        destination_port) + "#@#" + private_secret_key + "#@#" + task_list[0] + "###" + task_list[1] + "###" + \
                    task_list[2] + "###" + task_list[3]

    return config_string
