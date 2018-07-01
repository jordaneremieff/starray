import asyncio

import io
import numpy as np
from PIL import Image, ImageDraw
from pyray.shapes.circle import draw_sphere
from pyray.rotation import rotation

from starlette import Response


HTML_BODY = """<!DOCTYPE html>
<html>
<head>
<link href="https://fonts.googleapis.com/css?family=Open+Sans" rel="stylesheet">
<style>
body {
  font-family: 'Open Sans', sans-serif;
  font-size: 20px;
  background: #fff;
}
</style>
</head>
<body>
<h1>pyray test</h1>
<h3>testing pyray</h3>
<br>
<img id="imgtest">
<script>
    var ws = new WebSocket("ws://localhost:8000/");
    ws.onmessage = function(msg) {
        var r = new FileReader();
        r.readAsBinaryString(msg.data);
        r.onload = function(){
            var img=new Image();
            document.getElementById("imgtest").src = "data:image/jpeg;base64,"+window.btoa(r.result);
        };
};
</script>
</body>
</html>
"""


class App:

    def __init__(self, scope):
        self.scope = scope

    async def __call__(self, receive, send):
        message = await receive()

        if message["type"] == "http.request":
            response = Response(HTML_BODY, headers=[["content-type", "text/html"]])
            await response(receive, send)

        if message["type"] == "websocket.connect":
            await send({"type": "websocket.accept"})
            number_of_circles = 20
            line_thickness = 2

            for i in np.arange(60):
                r = rotation(
                    3,
                    2.5 + np.pi * np.sin(i / 10.0) * np.random.uniform(0.75, 1) / 20.0,
                )
                im = Image.new("RGB", (500, 500), (1, 1, 1))
                draw = ImageDraw.Draw(im, "RGBA")
                draw_sphere(
                    draw,
                    np.array([0, 0, 0]),
                    np.array([0, 0, 1]),
                    1 * np.random.uniform(0.75, 1) + 0.4 * np.sin(np.pi / 10.0 * i),
                    r,
                    num_circle=number_of_circles,
                    rgba=(182, 183, 186, 255),
                    width=line_thickness,
                )
                img_bytes = io.BytesIO()
                im.save(img_bytes, format="PNG")
                await asyncio.sleep(0.1)
                await send({"type": "websocket.send", "bytes": img_bytes.getvalue()})
            await send({"type": "websocket.close", "code": 1000})
