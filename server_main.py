from home_smart_server import HomeSmartServer

"""
########################################################################################################################
Here is example configuration of connection observer with 2 tasks 
########################################################################################################################
----->
"""
config = {"task_1": 21,
          "task_2": 22,
          "task_3": 23,
          "task_4": 24}

destination_port = 1111
private_secret_key = "okon"

"""
########################################################################################################################
End of configuration code
########################################################################################################################
"""


def _create_task_list():
    task_list = config.keys()
    return task_list


def _create_gpio_pin_list():
    gpio_pin_list = config.values()
    return gpio_pin_list


def create_android_app_cfg_string():
    return "asd"


connection_observer = HomeSmartServer(destination_port, private_secret_key, _create_task_list(),
                                      _create_gpio_pin_list())
connection_observer.start_server()

while True:
    print('waiting for a connection')

    connection, client_address = connection_observer.sock.accept()
    print("connection from", client_address)

    while True:
        received_string = connection.recv(4096)
        received_string = received_string.decode("utf-8")
        if received_string:
            print("Received data: %s" % received_string)
            if connection_observer.verify_received_public_key(received_string):
                response_data = 'starting_task\n'
                connection_observer.start_action_if_task_string_known(received_string, client_address)
            else:
                response_data = 'inncorrect SHA-key\n'
                print("bad data")
            response_data = response_data.encode("utf-8")
            connection.sendall(response_data)
        else:
            print("closing connection\n", client_address)
            break
