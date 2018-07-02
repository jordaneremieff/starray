import asyncio
import io
import numpy as np
from PIL import Image, ImageDraw
from pyray.shapes.circle import draw_sphere
from pyray.rotation import rotation
from afiqah.consumers import WebSocketConsumer


class WebSocketApp(WebSocketConsumer):

    async def websocket_connect(self, message):
        await self.send({"type": "websocket.accept"})

        number_of_circles = 20
        line_thickness = 2

        for i in np.arange(60):
            r = rotation(
                3, 2.5 + np.pi * np.sin(i / 10.0) * np.random.uniform(0.75, 1) / 20.0
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

            await self.send({"type": "websocket.send", "bytes": img_bytes.getvalue()})

        await self.send({"type": "websocket.close", "code": 1000})


class StreamApp:

    def __init__(self, scope):
        self.scope = scope

    async def __call__(self, receive, send):
        message = await receive()
        await send(
            {
                "type": "http.response.start",
                "status": 200,
                "headers": [
                    [b"Content-Type", b"multipart/x-mixed-replace; boundary=frame"]
                ],
            }
        )
        async for data in stream():
            await send({"type": "http.response.body", "body": data, "more_body": True})
            await asyncio.sleep(0.1)


async def stream():
    number_of_circles = 20
    line_thickness = 2

    for i in np.arange(60):
        r = rotation(
            3, 2.5 + np.pi * np.sin(i / 10.0) * np.random.uniform(0.75, 1) / 20.0
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

        yield b"".join(
            [
                b"--frame\r\n",
                b"Content-Type: image/jpeg\r\n\r\n",
                img_bytes.getvalue(),
                b"\r\n",
            ]
        )
