import socket
from hashlib import sha256
from time import time


def get_ip_address_of_current_device():
    """
    Returns local ip address of current device.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip


def generate_public_key(private_key):
    current_mixed_string = str(round(time() / 5)) + "%$%" + private_key

    return sha256(current_mixed_string.encode('utf-8')).hexdigest()


def test_connection(public_key, task_string, gpio_action):
    s = socket.socket()
    port = 6785
    s.connect((get_ip_address_of_current_device(), port))
    msg = public_key + "@#@" + task_string + "@#@" + gpio_action
    s.send(msg.encode("utf-8"))
    response = s.recv(4096)
    s.close()
    return response.decode("utf-8")


print("Case 1 ---> correct data received")
for i in range(1, 5):
    assert test_connection(generate_public_key("passwd"), "task_1", "off") == "starting_task\n"
    print("Passed " + str(i) + " check")

print("Case 2 ---> incorrect public key received")
for i in range(1, 5):
    assert test_connection(generate_public_key("bad_passwd"), "task_1", "off") == "incorrect SHA-key\n"
    print("Passed " + str(i) + " check")

print("Case 3 ---> non existing task string received")
for i in range(1, 5):
    assert test_connection(generate_public_key("passwd"), "no_existing_task", "off") == "invalid task string\n"
    print("Passed " + str(i) + " check")
