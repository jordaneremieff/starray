from afiqah import Afiqah
from starlette import HTMLResponse
from jinja2 import Environment, FileSystemLoader
from starray import WebSocketApp, StreamApp

env = Environment(loader=FileSystemLoader("templates"))


app = Afiqah()


@app.route("/")
def homepage(scope):
    template = env.get_template("index.html")
    return HTMLResponse(template.render())


@app.route("/ws")
def pyray_ws(scope):
    return WebSocketApp(scope)


@app.route("/streampage/")
def streampage(scope):
    template = env.get_template("stream.html")
    return HTMLResponse(template.render())


@app.route("/stream/")
def pyray_stream(scope):
    return StreamApp(scope)
