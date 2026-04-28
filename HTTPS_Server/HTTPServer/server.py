import socket
import ssl
import threading
from .requests import HTMLRequest, MIME_TYPES
from .exceptions import HTTPException as _HTTPException
from .HttpParser.parser import HTTPParser
import re

def _favicon(req):
    return HTMLRequest(mime=MIME_TYPES[".ico"]).FileResponse(f'{req.path}', _HTTPException().Not_Found_Favicon)

def _static(request):
    return HTMLRequest(mime=MIME_TYPES[".css"]).FileResponse(f'{request.path}')

class Re_Pathes:
    def __init__(self):
        self._RE_PATH: list[object] = [self.re_path(r"/static/css/\D+", _static)]
    @property
    def RE_PATH(self):
        return self._RE_PATH
    @RE_PATH.setter
    def RE_PATH(self, newpath):
        self._RE_PATH += newpath
    
    def re_path(self, path_pattern: str, func: object) -> object: 
        def regular(nowpath) -> bool|object:
            data: re.Match[str]|None = re.fullmatch(path_pattern, nowpath)
            if data:
                return func
            else:
                return False
        
        return regular

class Pathes:
    def __init__(self):    
        self._PATH = {
            "/": _HTTPException().Not_Found,
            "/favicon.ico": _favicon,
        }
    @property
    def PATH(self):
        return self._PATH
    @PATH.setter
    def PATH(self, newpath):
        self._PATH.update(newpath)

class HTTPServer():
    _Path = Pathes()
    _re_path = Re_Pathes()
    def __init__(self, host: tuple[str, int] = ('127.0.0.1', 8000)):
        """
        host: tuple 
        """
        self.SERVER_HOST, self.SERVER_PORT = host
    
    @property
    def PATH(self):
        return self._Path.PATH
    @PATH.setter
    def PATH(self, newpath):
        self._Path.PATH.update(newpath)

    @property
    def RE_PATH(self):
        return self._re_path.RE_PATH
    @RE_PATH.setter
    def RE_PATH(self, newpath):
        self._re_path.RE_PATH = newpath

    def _Regular(self, nowpath: str):
        for i in self.RE_PATH:
            answ = i(nowpath)
            if answ:
                return answ
        return _HTTPException().Not_Found


    def client_handler(self, crs: socket.socket):
        parser = HTTPParser()
        try:
            data = crs.recv(1024)
            if data:
                data = parser.parse(data)
                print(f"Метод: {data.method}")
                crs.send(self.PATH.get(data.path, self._Regular(data.path))(data))
        except Exception as e:
            print(f"Ошибка: {e}")
        finally:
            crs.close()
            print(f"client завершил соединение")

    def run(self) -> None:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.SERVER_HOST, self.SERVER_PORT))
        server_socket.listen(5)
        print(f"Сервер слушает на {self.SERVER_HOST}:{self.SERVER_PORT}")
        while True:
            client_raw_socket, client_addr = server_socket.accept()
            print(f"Подключен клиент: {client_addr}")
            threading.Thread(target=self.client_handler, kwargs={"crs": client_raw_socket}, daemon=True).start()

class HTTPSServer(HTTPServer):
    def __init__(self, ssld: tuple[str, str] = ("./ssl/cert.pem", "./ssl/key.pem"), host: tuple[str, int] = ('127.0.0.1', 8443)):
        super().__init__(host)
        self.SERVER_CERT, self.SERVER_KEY = ssld

    def run(self) -> None:
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain(certfile=self.SERVER_CERT, keyfile=self.SERVER_KEY)
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.SERVER_HOST, self.SERVER_PORT))
        server_socket.listen(5)
        print(f"Сервер слушает на {self.SERVER_HOST}:{self.SERVER_PORT}")
        while True:
            try:
                client_raw_socket, client_addr = server_socket.accept()
                tls_conn = context.wrap_socket(client_raw_socket, server_side=True)

                print(f"Подключен клиент: {client_addr}")
                print("TLS рукопожатие успешно завершено")
                print(f"Версия TLS: {tls_conn.version()}")

                threading.Thread(target=self.client_handler, kwargs={"crs": tls_conn}, daemon=True).start()
            except ssl.SSLError as e:
                print(f"Ошибка TLS: {e}")
                client_raw_socket.close()