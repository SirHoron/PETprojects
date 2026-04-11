from .response import HTTPResponse
import json
class HTTPParser():
    def __init__(self):
        pass
    def _texttype(self, content_type: str, text: str) -> str|dict:
        match content_type:
            case "application/json":
                return json.loads(text)
            case _:
                return text
                
    def parse(self, text: bytes) -> HTTPResponse:
        textlist = text.decode().split("\r\n")
        method, path, version = textlist[0].split(" ")
        host = (textlist[1][6:].split(":"))
        response = {"method": method, "path": path, "version": version, "host": host, "header": {}}
        for i in textlist[2:textlist.index('')]:
            if i:
                i = i.split(":")
                response["header"].update({i[0]:i[1].lstrip()})

        response.update({"body": self._texttype(response["header"].get("Content-Type"), textlist[textlist.index('')+1:])})

        return HTTPResponse(response)