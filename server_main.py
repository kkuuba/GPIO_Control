from home_smart_server import HomeSmartServer, get_ip_address_of_current_device

"""
########################################################################################################################
Here is example configuration of connection observer of 3 impulse tasks and 2 switch tasks 
########################################################################################################################
----->
"""
config = {"task_1": 14,  # impulse task
          "task_2": 15,  # impulse task
          "task_3": 25,  # impulse task
          "task_4": 24,  # switch task
          "task_5": 25,  # switch task
          }

destination_port = 6785
private_secret_key = "okon"

"""
########################################################################################################################
End of configuration code
########################################################################################################################
"""


def _create_task_list():
    task_list = list(config.keys())
    return task_list


def _create_gpio_pin_list():
    gpio_pin_list = list(config.values())
    return gpio_pin_list


def create_android_app_cfg_string():
    task_list = list(config.keys())
    config_string = get_ip_address_of_current_device() + "#@#" + str(
        destination_port) + "#@#" + private_secret_key + "#@#" + task_list[0] + "###" + task_list[1] + "###" + \
                    task_list[2] + "###" + task_list[3]

    return config_string


f = open("android_config.txt", "w")
f.write(create_android_app_cfg_string())

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
