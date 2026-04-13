import os
from .exceptions import HTTPException
MIME_TYPES = {
    ".html": "text/html",
    ".css":  "text/css",
    ".js":   "application/javascript",
    ".json": "application/json",
    ".png":  "image/png",
    ".jpg":  "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif":  "image/gif",
    ".ico":  "image/x-icon",
    ".svg":  "image/svg+xml",
    ".txt":  "text/plain",
    ".pdf":  "application/pdf",
    ".zip":  "application/zip",
    ".mp4":  "video/mp4",
    ".mp3":  "audio/mpeg",
}

class HTMLRequest():
    def __init__(self, mime: str = MIME_TYPES[".html"]):
        if "text" in mime or "xml" in mime or "json" in mime:
            self.header = "HTTP/1.1 200 OK\r\n"\
    f"Content-Type: {mime}; charset=utf-8\r\n"\
    "Connection: keep-alive\r\n"\
    "Cache-Control: public, max-age=0, must-revalidate\r\n"\
    "X-Content-Type-Options: nosniff\r\n"\
    "Content-Length: "
        else:
            self.header = "HTTP/1.1 200 OK\r\n"\
    f"Content-Type: {mime}; charset=utf-8\r\n"\
    "Connection: keep-alive\r\n"\
    "Cache-Control: public, max-age=0, must-revalidate\r\n"\
    "X-Content-Type-Options: nosniff\r\n"\
    "Content-Length: "
            
    def CleanHTML(self, htmltext: str) -> bytes:
        html = f'<!DOCTYPE html><html lang="ru"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Document</title></head><body>{htmltext}</body></html>'
        response = self.header + f"{len(html)}\r\n\r\n" + html
        return response.encode()
    
    def FileResponse(self, fullpath, exception: object|None = None) -> bytes:
        if fullpath[0] in "//":
            fullpath = "." + fullpath
        if os.path.exists(fullpath):
            with open(fullpath, "rb") as bfile:
                file = bfile.read()
            response = self.header.encode() + f"{len(file)}\r\n\r\n".encode() + file
            return response
        else:
            if exception:
                return exception()
            else:
                return HTTPException().Not_Found()