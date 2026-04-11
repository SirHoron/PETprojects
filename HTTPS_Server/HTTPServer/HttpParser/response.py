class HTTPResponse():
    def __init__(self, httpdict: dict):
        self.host: tuple = httpdict.get("host")
        self.method: str = httpdict.get("method")
        self.path: str = httpdict.get("path")
        self.version: str = httpdict.get("version")
        self.header: dict = httpdict.get("header")
        self.body: any = httpdict.get("body")

class HTTPSResponse(HTTPResponse):
    def __init__(self, httpdict: dict):
        super().__init__(httpdict)