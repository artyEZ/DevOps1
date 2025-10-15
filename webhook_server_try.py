#!/usr/bin/env python3
from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import subprocess
import json

REPO_URL = "https://github.com/YOUR_USERNAME/YOUR_REPO.git"
APP_DIR = "/home/vboxuser/app"
APP_SERVICE = "app.service"
HOST = "0.0.0.0"
PORT = 8080

class WebhookHandler(BaseHTTPRequestHandler):
    def _set_response(self, code=200):
        self.send_response(code)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()

    def do_GET(self):
        self._set_response()
        self.wfile.write(b'ok\n')

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)

        event = self.headers.get('X-GitHub-Event')
        print(f"Получено событие: {event}")

        if event == 'push':
            try:
                if not os.path.exists(APP_DIR):
                    print(f"Клонируем репозиторий в {APP_DIR}...")
                    subprocess.run(["git", "clone", REPO_URL, APP_DIR], check=True)
                else:
                    print(f"Обновляем репозиторий в {APP_DIR}...")
                    subprocess.run(["git", "-C", APP_DIR, "pull"], check=True)

                print(f"Перезапуск сервиса {APP_SERVICE}...")
                result = subprocess.run(
                    ["sudo", "systemctl", "restart", APP_SERVICE],
                    capture_output=True, text=True
                )
                if result.returncode == 0:
                    print("Код обновлён и приложение перезапущено.")
                else:
                    print("Ошибка при перезапуске приложения:", result.stderr)

            except subprocess.CalledProcessError as e:
                print("Ошибка при выполнении git:", e)
            except Exception as e:
                print("Общая ошибка:", e)

        self._set_response()
        self.wfile.write(b'ok\n')

def run_server():
    server_address = (HOST, PORT)
    httpd = HTTPServer(server_address, WebhookHandler)
    print(f"Запуск webhook-сервера на http://{HOST}:{PORT}/")
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()
