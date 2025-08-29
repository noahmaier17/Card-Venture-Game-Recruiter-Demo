import pyglet
from pyglet import shapes
from pyglet.window import mouse

def trd(value: int) -> int:
    return round(value / 3)

window = pyglet.window.Window(width=trd(1280), height=trd(720), caption="Hello World")
window.set_location(x=trd(400), y=trd(200))
# window.set_mouse_visible(False)
cursor = window.get_system_mouse_cursor(window.CURSOR_HELP)

batch = pyglet.graphics.Batch()

circle1 = shapes.Circle(x=trd(700), y=trd(150), radius=trd(10), color=(50, 225, 30), batch=batch)
circle2 = shapes.Circle(x=trd(100), y=trd(100), radius=trd(25), color=(255, 0, 0), batch=batch)

@window.event
def on_draw() -> None:
    window.clear()
    batch.draw()

@window.event
def on_mouse_motion(x: int, y: int, dx: int, dy: int) -> None:
    curr_x = circle1.x
    curr_y = circle1.y
    circle1.position = (x, y)

@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers) -> None:
    if buttons & mouse.LEFT:
        circle2.position = (x, y)
        window.set_mouse_cursor(cursor)

pyglet.app.run()