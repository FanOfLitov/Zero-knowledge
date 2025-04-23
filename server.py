import random
import socket
from math import gcd

def generate_prime(bits):
    while True:
        num = random.getrandbits(bits)
        if is_prime(num):
            return num

def is_prime(n, k=5):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for __ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

p = generate_prime(512)
q = generate_prime(512)
n = p * q

print(f"Server: Public key n = {n}")


v = None

def register_client(v_client):
    global v
    v = v_client
    print(f"Server: Registered client with v = {v}")


def authenticate(conn):
    rounds = 16
    for i in range(rounds):
        print(f"\nРаунд {i + 1}/{rounds}")
        # Получаем x от клиента
        x = int(conn.recv(1024).decode())
        print(f"Сервер: получен x = {x}")
        # Генерируем вызов c (случайный бит)
        c = random.randint(0, 1)
        print(f"Сервер: отправка вызова c = {c}")
        conn.send(str(c).encode())
        # Получаем ответ y от клиента
        y = int(conn.recv(1024).decode())
        print(f"Сервер: получен y = {y}")
        # Проверяем условие
        if pow(y, 2, n) == (x * pow(v, c, n)) % n:
            print("Сервер: раунд пройден")
        else:
            print("Сервер: Аутентификация не удалась")
            return False
    print("Сервер: Аутентификация успешна")
    return True

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))
    server_socket.listen(1)
    print("Сервер: ожидается подключение клиента...")
    conn, addr = server_socket.accept()
    print(f"Сервер: клиент подключен на {addr}")

    conn.send(str(n).encode())
    print(f"Сервер: отправлено n = {n} клиенту")

    v_client = int(conn.recv(1024).decode())
    register_client(v_client)

    authenticate(conn)

    conn.close()

if __name__ == "__main__":
    main()
