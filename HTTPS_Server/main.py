from HTTPServer.server import HTTPSServer, Re_Pathes
from HTTPServer.requests import HTMLRequest, MIME_TYPES
from HTTPServer.HttpParser.response import HTTPResponse

server = HTTPSServer()
path = Re_Pathes()

def icon(req):
    return HTMLRequest(MIME_TYPES[".png"]).FileResponse('/static/Помпа.png')

def lol(request):
    return HTMLRequest().FileResponse('templates/index1.html')

def omg(request):
    return HTMLRequest().FileResponse('templates/index1.html')

def main(request):
    return HTMLRequest().FileResponse('templates/index.html')

def lokea(request: HTTPResponse):
    return HTMLRequest().CleanHTML('<h1>Как-то так</h1>')

server.PATH = {
    "/": main,
    "/lokea": lokea,
    "/favicon.ico": icon,
}

server.RE_PATH = \
[
path.re_path(r'/lokea/\D+', omg),
path.re_path(r"/\d+/?", lol),
]

server.run()
