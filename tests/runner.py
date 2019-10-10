import socket
from hashlib import sha256
from time import time


def generate_public_key(private_key):
    current_mixed_string = str(round(time() / 5)) + "%$%" + private_key

    return sha256(current_mixed_string.encode('utf-8')).hexdigest()


def test_connection(public_key, task_string, gpio_action):
    s = socket.socket()
    port = 6785
    s.connect(('10.0.2.15', port))
    msg = public_key + "@#@" + task_string + "@#@" + gpio_action
    s.send(msg.encode("utf-8"))
    response = s.recv(4096)
    s.close()
    return response.decode("utf-8")


for i in range(10):
    assert test_connection(generate_public_key("passwd"), "task_1", "off") == "starting_task\n"
    print("Passed " + str(i) + " check")
