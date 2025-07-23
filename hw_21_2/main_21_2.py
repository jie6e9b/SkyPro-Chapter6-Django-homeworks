from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import json

hostName = "localhost"
serverPort = 8080


class MyServer(BaseHTTPRequestHandler):

    def do_GET(self):
        # Отправляем страницу контактов на любой GET-запрос
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        # Читаем HTML-файл
        try:
            with open("contacts.html", "r", encoding="utf-8") as file:
                content = file.read()
                # Заменяем пути к локальным файлам на CDN
                content = content.replace('bootstrap/css/bootstrap.min.css',
                                          'https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css')
                content = content.replace('bootstrap/js/bootstrap.bundle.min.js',
                                          'https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js')
                content = content.replace('avatar.jpg',
                                          'https://via.placeholder.com/32x32')

                self.wfile.write(bytes(content, "utf-8"))
        except FileNotFoundError:
            self.wfile.write(bytes("Файл contacts.html не найден", "utf-8"))

    def do_POST(self):
        # Получаем длину данных
        content_length = int(self.headers['Content-Length'])
        # Читаем данные
        post_data = self.rfile.read(content_length)

        # Пытаемся декодировать как form-data
        try:
            # Декодируем данные формы
            form_data = post_data.decode('utf-8')
            print("Получены POST данные:")

            # Разбираем данные формы
            parsed_data = parse_qs(form_data)
            for key, value in parsed_data.items():
                print(f"{key}: {value[0]}")
        except:
            # Если не получилось декодировать как form-data, выводим как есть
            print("Получены POST данные (необработанные):")
            print(post_data)

        # Отправляем ответ на POST запрос
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        # Отправляем страницу с подтверждением отправки
        response = """
        <html>
        <head>
            <title>Форма отправлена</title>
            <meta http-equiv="refresh" content="3;url=/">
        </head>
        <body>
            <h1>Данные успешно отправлены!</h1>
            <p>Вы будете перенаправлены на главную страницу через 3 секунды...</p>
        </body>
        </html>
        """
        self.wfile.write(bytes(response, "utf-8"))


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Сервер запущен http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Сервер остановлен.")