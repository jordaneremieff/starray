from afiqah import Afiqah
from starlette import HTMLResponse
from jinja2 import Environment, FileSystemLoader
from starray import WebSocketApp

env = Environment(loader=FileSystemLoader("templates"))
template = env.get_template("index.html")


app = Afiqah()


@app.route("/")
def homepage(scope):
    return HTMLResponse(template.render())


@app.route("/ws")
def pyray_ws(scope):
    return WebSocketApp(scope)
