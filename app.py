import mimetypes
import urllib.parse
import socket
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread
from json_handler import server as json_server
import time

BASE_DIR = Path()


def socket_send_message(message):
    host = socket.gethostname()
    port = 5000

    client_socket = socket.socket()

    try:
        client_socket.connect((host, port))

        while message:
            client_socket.send(message)
            data = client_socket.recv(1024).decode()
            if not data:
                break
    finally:
        client_socket.shutdown(socket.SHUT_RDWR)
        client_socket.close()

class HttpGetHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        data = self.rfile.read(int(self.headers['Content-Length']))
        socket_send_message(data)
        self.send_response(200)
        self.send_header('Location', '/message')
        self.end_headers()
        self.wfile.flush()
        time.sleep(0.1)
        self.connection.shutdown(socket.SHUT_WR)
        self.connection.close()

    def do_GET(self):
        route = urllib.parse.urlparse(self.path)
        match route.path:
            case '/':
                self.send_html("index.html")
            case '/message':
                self.send_html("message.html")
            case _:
                file = BASE_DIR.joinpath(route.path[1:])
                if file.exists():
                    self.send_static(file)
                else:
                    self.send_html('error.html', 404)

    def send_html(self, filename, status_code=200):
        with open(filename, 'rb') as file:
            response_content = file.read()
        self.send_response(status_code)
        self.send_header('Content-Type', 'text/html')
        self.send_header('Content-Length', str(len(response_content)))
        self.end_headers()
        self.wfile.write(response_content)

    def send_static(self, filename, status_code=200):
        self.send_response(status_code)
        mime_type, *_ = mimetypes.guess_type(filename)
        if mime_type:
            self.send_header('Content-Type', mime_type)
        else:
            self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        with open(filename, 'rb') as file:
            self.wfile.write(file.read())


def run_http_server(server_class=HTTPServer, handler_class=HttpGetHandler):

    server_address = ("", 3000)
    http = server_class(server_address, handler_class)
    try:
        http.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        http.server_close()


if __name__ == '__main__':
    json_handler = Thread(target=json_server)
    json_handler.start()
    print("Start server")
    run_http_server()