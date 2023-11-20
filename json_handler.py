import json
import pathlib
import socket
import urllib
import time

BASE_DIR = pathlib.Path()


def save_data_to_json(data):
    data_parse = urllib.parse.unquote_plus(data)
    data_parse = {key: value for key, value in [el.split('=') for el in data_parse.split('&')]}
    data_parse['timestamp'] = time.strftime("%Y-%m-%d %H:%M:%S.%f", time.localtime())

    with open(BASE_DIR.joinpath('storage/data.json'), 'r', encoding='utf-8') as existing_file:
        try:
            existing_data = json.load(existing_file)
        except json.decoder.JSONDecodeError:
            existing_data = {}

    existing_data[data_parse['timestamp']] = {
        "username": data_parse['username'],
        "message": data_parse['message']
    }

    with open(BASE_DIR.joinpath('storage/data.json'), 'w', encoding='utf-8') as fd:
        json.dump(existing_data, fd, ensure_ascii=False, indent=2)


def server():
    print("Json server started")
    host = socket.gethostname()
    port = 5000



    while True:
        server_socket = socket.socket()
        server_socket.bind((host, port))
        server_socket.listen()
        conn, address = server_socket.accept()
        print(f'Connection from {address}')

        try:
            data = conn.recv(100).decode()
            if not data:
                break
            save_data_to_json(data)
        finally:
            conn.close()