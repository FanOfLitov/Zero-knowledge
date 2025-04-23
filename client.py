import random
import socket
from math import gcd


def generate_secret_and_v(n):
    while True:
        s = random.randint(2, n - 1)
        if gcd(s, n) == 1:
            v = pow(s, 2, n)
            return s, v

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))

    n = int(client_socket.recv(1024).decode())
    print(f"Клиент: Получен n = {n} с сервера")

    s, v = generate_secret_and_v(n)
    print(f"Клиент: Секретный s = {s}, Публичный v = {v}")

    client_socket.send(str(v).encode())
    print(f"Клиент: Отправлен v = {v} на сервер")

    rounds = 16
    for i in range(rounds):
        print(f"\nRound {i + 1}/{rounds}")

        r = random.randint(1, n - 1)
        x = pow(r, 2, n)
        print(f"Клиент: Отправлено x = {x}")
        client_socket.send(str(x).encode())

        c = int(client_socket.recv(1024).decode())
        print(f"Клиент: Получено c = {c}")

        y = (r * pow(s, c, n)) % n
        print(f"Клиент: Отправлено y = {y}")
        client_socket.send(str(y).encode())

    client_socket.close()

if __name__ == "__main__":
    main()
