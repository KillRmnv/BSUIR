import socket
import threading
import time
from urllib.parse import urlparse

# Простой кэш: словарь для хранения ответов по URL
cache = {}
CACHE_EXPIRATION = 300  # Время жизни кэша в секундах (5 минут)

def handle_client(client_socket):
    # Получаем запрос от клиента
    request = client_socket.recv(4096).decode('utf-8')
    if not request:
        client_socket.close()
        return

    # Парсим первую строку запроса
    first_line = request.split('\n')[0]
    method = first_line.split()[0]
    url = first_line.split()[1]

    # Поддерживаем только GET-запросы для простоты
    if method != 'GET':
        response = b"HTTP/1.1 405 Method Not Allowed\r\n\r\n"
        client_socket.send(response)
        client_socket.close()
        return

    # Нормализуем URL (убираем http:// если есть)
    if url.startswith('http://'):
        url = url[7:]

    # Парсим URL
    parsed_url = urlparse('http://' + url)
    host = parsed_url.hostname
    path = parsed_url.path or '/'
    port = parsed_url.port or 80

    # Проверяем кэш
    cache_key = f"{host}{path}"
    if cache_key in cache:
        cached_data = cache[cache_key]
        if time.time() - cached_data['timestamp'] < CACHE_EXPIRATION:
            print(f"Returning cached response for {url}")
            client_socket.send(cached_data['response'])
            client_socket.close()
            return

    # Соединяемся с целевым сервером
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.connect((host, port))

        # Формируем запрос к серверу (заменяем Host)
        server_request = request.replace(first_line, f"GET {path} HTTP/1.1")
        server_request = server_request.replace('Proxy-Connection', 'Connection')  # Изменяем на Connection: close
        server_socket.send(server_request.encode('utf-8'))

        # Получаем ответ от сервера
        response = b""
        while True:
            data = server_socket.recv(4096)
            if not data:
                break
            response += data

        server_socket.close()

        # Кэшируем ответ
        cache[cache_key] = {
            'response': response,
            'timestamp': time.time()
        }
        print(f"Cached response for {url}")

        # Отправляем ответ клиенту
        client_socket.send(response)
    except Exception as e:
        error_response = f"HTTP/1.1 500 Internal Server Error\r\n\r\nError: {str(e)}".encode('utf-8')
        client_socket.send(error_response)

    client_socket.close()

def main():
    proxy_host = '0.0.0.0'
    proxy_port = 8080

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((proxy_host, proxy_port))
    server.listen(5)
    print(f"Proxy server listening on {proxy_host}:{proxy_port}")

    while True:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    main()