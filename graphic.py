import pyglet
from pyglet.window import mouse


def write_content(string):
    f = open('data', 'a')
    f.write(string)
    f.close()


class Window(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.frame_rate = 1/60.0
        
        temp_background = pyglet.image.load('metro.jpg')
        self.background = pyglet.sprite.Sprite(temp_background)
    
    def on_draw(self):
        self.clear()
        self.background.draw()
        
    def on_mouse_press(self, x, y, button, modifier):
        if button == mouse.LEFT:
            write_content('{},{}\n'.format(x, y))
    
    def update(self, dt):
        pass


def main():
    window = Window(1360, 768, 'Visualzation')
    pyglet.clock.schedule_interval(window.update, window.frame_rate)
    pyglet.app.run()


if __name__ == '__main__':
    main()