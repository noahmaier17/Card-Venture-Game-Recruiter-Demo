import pyglet
from pyglet import shapes

def trd(value: int) -> int:
    return round(value / 3)

window = pyglet.window.Window(width=trd(1280), height=trd(720), caption="Hello World")
window.set_location(x=trd(400), y=trd(200))

batch = pyglet.graphics.Batch()

circle = shapes.Circle(x=trd(700), y=trd(150), radius=trd(100), color=(125, 125, 125), batch=batch)
square = shapes.Rectangle(x=trd(200), y=trd(200), width=trd(400), height=trd(400), color=(125, 125, 125), batch=batch)
square.anchor_position = (trd(400) / 2, trd(400) / 2)

@window.event
def on_draw() -> None:
    window.clear()
    batch.draw()

def update(dt):
    square.rotation += 1

pyglet.clock.schedule_interval(update, 1/60)
pyglet.app.run()