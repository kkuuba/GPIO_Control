from hashlib import sha256
from time import sleep, time
import socket
import RPi.GPIO as GPIO
from datetime import datetime


def get_ip_address_of_current_device():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip


def _gpio_impulse_task(gpio_pin_id, duration):
    GPIO.output(gpio_pin_id, GPIO.HIGH)
    sleep(duration)
    GPIO.output(gpio_pin_id, GPIO.LOW)
    sleep(1)


def _gpio_change_state_task(gpio_pin_id, task_data):
    if task_data == "on":
        GPIO.output(gpio_pin_id, GPIO.HIGH)
        sleep(1)
    if task_data == "off":
        GPIO.output(gpio_pin_id, GPIO.LOW)
        sleep(1)


def _start_raspberry_gpio_task(gpio_pin_id, gpio_action_string):
    print("starting gpio task ...\n")
    if gpio_action_string == "impulse":
        _gpio_impulse_task(gpio_pin_id, 1)
    else:
        _gpio_change_state_task(gpio_pin_id, gpio_action_string)


def save_logging_info_to_log_file(task_string, gpio_pin, client_ip):
    file = open('log_info.txt', 'a+')
    time_stamp = datetime.fromtimestamp(time()).strftime('%Y-%m-%d %H:%M:%S')
    file.write(time_stamp + ' | ' + task_string + ' | ' + client_ip[0] + ' | ' + 'Setting ' +
               str(gpio_pin) + ' gpio pin HIGH on 1000 ms interval\n')
    file.close()


class HomeSmartServer:

    def __init__(self, server_port, private_key, accepted_tasks, raspberry_gpio_pins):
        """
        Create connection observer with equal private key and two list of task string and raspberry gpio pins,
        which listen to incoming connection and verify received information about requesting device.

        :param server_port: listening port of server device
        :param private_key: string containing secret key which should be the same of both side of connection
        :param accepted_tasks: list containing all tasks string, must have equivalent gpio pin on the same position
        :param raspberry_gpio_pins: list containing all gpio pins which are in use
        """
        self.server_port = server_port
        self.private_key = private_key
        self.accepted_tasks = accepted_tasks
        self.raspberry_gpio_pins = raspberry_gpio_pins
        self.sock = socket.socket()
        self.server_address = ('0.0.0.0', 1111)
        self.task_dict = dict()

    def _create_task_dict(self):
        try:
            for i in range(len(self.accepted_tasks)):
                self.task_dict[self.accepted_tasks[i]] = self.raspberry_gpio_pins[i]
        except IndexError:
            print('Cannot create tasks dict. Every task string must have gpio pin assigned')

    def _update_public_keys(self):
        current_mixed_string = str(round(time() / 5)) + "%$%" + self.private_key
        previous_mixed_string = str(round(time() / 5) - 1) + "%$%" + self.private_key
        actual_public_key = sha256(current_mixed_string.encode('utf-8'))
        previous_public_key = sha256(previous_mixed_string.encode('utf-8'))

        return [previous_public_key.hexdigest(), actual_public_key.hexdigest()]

    def _prepare_raspberry_gpio(self):
        GPIO.setmode(GPIO.BCM)
        for gpio_pin in self.raspberry_gpio_pins:
            GPIO.setup(gpio_pin, GPIO.OUT)
            GPIO.output(gpio_pin, GPIO.LOW)

    def _some_operations_before_starting_the_server(self):
        self._create_task_dict()
        self.server_address = get_ip_address_of_current_device(), self.server_port
        self._prepare_raspberry_gpio()

    def start_server(self):
        self._some_operations_before_starting_the_server()
        print('starting up on %s port %s\n' % self.server_address)
        self.sock.bind(self.server_address)
        self.sock.listen(1)

    def verify_received_public_key(self, received_data):
        if received_data.split("@#@")[0] in self._update_public_keys():
            return True
        else:
            return False

    def start_action_if_task_string_known(self, received_data, client_ip):
        for task_string in self.accepted_tasks:
            if received_data.split("@#@")[1] == task_string:
                _start_raspberry_gpio_task(self.task_dict[task_string], received_data.split("@#@")[2])
                save_logging_info_to_log_file(task_string, self.task_dict[task_string], client_ip)
                print('Starting ' + str(self.task_dict[task_string]) + 'gpio pin' + received_data.split("@#@")[
                    2] + ' task ')
