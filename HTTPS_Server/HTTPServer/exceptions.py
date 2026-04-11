class HTTPException():
    def __init__(self):
        pass
    def Not_Found(self, *args, **kwargs) -> bytes:
        return b"HTTP/1.1 404 Not Found\r\n Content-Length: 0\r\n Connection: close\r\n\r\n"
    def Not_Found_Favicon(self, *args, **kwargs) -> bytes:
        return b"HTTP/1.1 204 No Content\r\n Content-Length: 0\r\n Connection: close\r\n\r\n"