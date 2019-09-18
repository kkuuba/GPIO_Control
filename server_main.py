from home_smart_server import HomeSmartServer

"""
########################################################################################################################
Here is example configuration of connection observer with 2 tasks 
########################################################################################################################
----->
"""

private_secret_key = 'ASg453Jd3rdr43dfr4443dfsdf'
connection_observer = HomeSmartServer(6555, private_secret_key, ['open_fence_gate', 'open_garage_gate'],
                                      [21, 11])
connection_observer.start_server()

"""
########################################################################################################################
End of configuration code
########################################################################################################################
"""

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
