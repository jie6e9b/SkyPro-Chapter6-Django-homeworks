from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import os

hostName = "localhost"
serverPort = 8080


class MyServer(BaseHTTPRequestHandler):

    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        # Определяем, какой файл запрашивается
        if path == "/" or path == "":
            # По умолчанию возвращаем contacts.html
            file_path = "contacts.html"
        elif path.endswith(".html"):
            # Если запрашивается .html файл, пытаемся его найти
            file_path = path[1:]  # Убираем начальный '/'
        else:
            # Для всех остальных запросов тоже возвращаем contacts.html
            file_path = "contacts.html"

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        # Читаем запрошенный HTML-файл
        try:
            with open(file_path, "r", encoding="utf-8") as file:
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
            # Если файл не найден, возвращаем contacts.html
            try:
                with open("contacts.html", "r", encoding="utf-8") as file:
                    content = file.read()
                    content = content.replace('bootstrap/css/bootstrap.min.css',
                                              'https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css')
                    content = content.replace('bootstrap/js/bootstrap.bundle.min.js',
                                              'https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js')
                    content = content.replace('avatar.jpg',
                                              'https://via.placeholder.com/32x32')

                    self.wfile.write(bytes(content, "utf-8"))
            except FileNotFoundError:
                self.wfile.write(bytes("<html><body><h1>Файл не найден</h1></body></html>", "utf-8"))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        try:
            form_data = post_data.decode('utf-8')
            print("Получены POST данные:")

            parsed_data = parse_qs(form_data)
            for key, value in parsed_data.items():
                print(f"{key}: {value[0]}")
        except:
            print("Получены POST данные (необработанные):")
            print(post_data)

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

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
    print(f"Сервер запущен http://{hostName}:{serverPort}")

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Сервер остановлен.")