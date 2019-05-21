import pyglet
from pyglet.gl import *


class Window(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.frame_rate = 1/60.0
        
    def on_draw(self):
        # glClear(GL_COLOR_BUFFER_BIT)
        # glBegin(GL_LINES)
        
        # glVertex2i(30, 60)
        # glVertex2i(400, 700)
        
        # glVertex2i(400, 700)
        # glVertex2i(1000, 200)
        
        # glEnd()
       pyglet.graphics.draw(2, pyglet.gl.GL_LINES,
    ('v2i', (100, 150, 300, 350)),
    ('c3B', (255, 0, 255, 255, 0, 255))
)


    def update(self, dt):
        pass


def main():
    window = Window(1360, 768, 'Visualzation')
    pyglet.clock.schedule_interval(window.update, window.frame_rate)
    pyglet.app.run()


if __name__ == '__main__':
    main()
