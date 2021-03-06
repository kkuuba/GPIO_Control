from home_smart_server import HomeSmartServer
import raspberry_utilities as rasp_util

"""
########################################################################################################################
Here is example configuration of connection observer of 3 impulse tasks and 2 switch tasks 
########################################################################################################################
----->
"""
config = {"task_1": 14,  # impulse task (you can change 'task_1' to your own name)
          "task_2": 15,  # impulse task (you can change 'task_2' to your own name)
          "task_3": 25,  # impulse task (you can change 'task_3' to your own name)
          "task_4": 24,  # switch task (you can change 'task_4' to your own name)
          "task_5": 25,  # switch task (you can change 'task_5' to your own name)
          }

destination_port = 6785
private_secret_key = "passwd"  # maybe change on something more complicated ...

"""
########################################################################################################################
End of configuration code
########################################################################################################################
"""

f = open("android_config.txt", "w")
f.write(rasp_util.create_android_app_cfg_string(config, destination_port, private_secret_key))

connection_observer = HomeSmartServer(destination_port, private_secret_key, list(config.keys()),
                                      list(config.values()))
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
                response_data = connection_observer.start_action_if_task_string_known(received_string, client_address)
            else:
                response_data = 'inncorrect SHA-key\n'
                print("Authentication failed")
            response_data = response_data.encode("utf-8")
            connection.sendall(response_data)
        else:
            print("closing connection\n", client_address)
            break
