from socket import *
import sys
import os
import time
from urllib.parse import urlparse

CACHE_TTL = 60  

def is_cache_valid(filename):
    if not os.path.exists(filename):
        return False
    return (time.time() - os.path.getmtime(filename)) < CACHE_TTL


if len(sys.argv) <= 1:
    print('Используйте : "python ProxyServer.py server_ip"\n[server_ip – IP-адрес прокси-сервера]')
    sys.exit(2)

tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
tcpSerSock.bind((sys.argv[1], 8888))
tcpSerSock.listen(5)

while True:
    print('Готов к обслуживанию...')
    tcpCliSock, addr = tcpSerSock.accept()
    print('Установлено соединение с:', addr)

    try:
        message = tcpCliSock.recv(4096).decode()
        print(message)

        if not message:
            raise ValueError("Пустой запрос")

        url = message.split()[1]
        parsed = urlparse(url)

        if not parsed.netloc:
            raise ValueError("Неверный URL")

        hostn = parsed.netloc
        path = parsed.path if parsed.path else "/"

        filename = hostn + path.replace("/", "_")
        filetouse = filename

        if is_cache_valid(filetouse):
            with open(filetouse, "rb") as f:
                outputdata = f.read()

            tcpCliSock.send(b"HTTP/1.0 200 OK\r\n")
            tcpCliSock.send(b"Content-Type: text/html\r\n\r\n")
            tcpCliSock.send(outputdata)

            print("Читаем из кэша:", filetouse)

        else:
            if os.path.exists(filetouse):
                os.remove(filetouse)
                print("Кэш устарел — удалён")

            c = socket(AF_INET, SOCK_STREAM)
            print("Подключаемся к:", hostn)

            try:
                c.connect((hostn, 80))

                request_line = f"GET {path} HTTP/1.0\r\nHost: {hostn}\r\n\r\n"
                c.send(request_line.encode())

                response = b""
                while True:
                    data = c.recv(4096)
                    if not data:
                        break
                    response += data

                with open(filetouse, "wb") as tmpFile:
                    tmpFile.write(response)

                tcpCliSock.send(response)
                print("Записано в кэш:", filetouse)

            except Exception as e:
                print("Ошибка соединения:", e)
                tcpCliSock.send(b"HTTP/1.0 502 Bad Gateway\r\n\r\n")

            finally:
                c.close()

    except ValueError as e:
        print("Ошибка запроса:", e)
        tcpCliSock.send(b"HTTP/1.0 400 Bad Request\r\n\r\n")

    except Exception as e:
        print("Внутренняя ошибка:", e)
        tcpCliSock.send(b"HTTP/1.0 500 Internal Server Error\r\n\r\n")

    finally:
        tcpCliSock.close()

tcpSerSock.close()
