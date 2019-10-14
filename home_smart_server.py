import raspberry_utilities as rasp_util
from hashlib import sha256
from time import time
import socket


class HomeSmartServer:

    def __init__(self, server_port, private_key, accepted_tasks, raspberry_gpio_pins):
        """
        Create connection observer with equal private key and two list of task string and raspberry gpio pins
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

    def _some_operations_before_starting_the_server(self):
        self._create_task_dict()
        self.server_address = rasp_util.get_ip_address_of_current_device(), self.server_port
        rasp_util.prepare_raspberry_gpio(self.raspberry_gpio_pins)

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
                rasp_util.start_raspberry_gpio_task(self.task_dict[task_string], received_data.split("@#@")[2])
                rasp_util.save_logging_info_to_log_file(task_string, self.task_dict[task_string], client_ip)
                print('Starting ' + str(self.task_dict[task_string]) + ' gpio pin ' + received_data.split("@#@")[
                    2] + ' task ')

                return 'starting_task\n'

        return 'invalid task string\n'
