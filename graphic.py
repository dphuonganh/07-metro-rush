import pyglet
from pyglet.window import mouse


def write_content(string):
    f = open('data', 'a')
    f.write(string)
    f.close()


def read_content():
    with open('data', 'r') as f:
        return f.readlines()


class Train:
    def __init__(self, posx, posy, img):
        self.posx = posx
        self.posy = posy
        self.sprite = self.Sprite(img)
        self.sprite.x = self.posx
        self.sprite.y = self.posy
    
    def draw(self):
        self.sprite.draw()
    
    def Sprite(self, img):
        return pyglet.sprite.Sprite(pyglet.image.load(img))
    
    def update(self):
        self.sprite.x = self.posx
        self.sprite.y = self.posy


class Window(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.frame_rate = 1/60.0
        
        temp_background = pyglet.image.load('metro.jpg')
        self.background = pyglet.sprite.Sprite(temp_background)

        self.list_train = []
        self.list_move = read_content()
        start = self.list_move[0].split(',')
        for _ in range(1):
            self.list_train.append(Train(int(start[0]), int(start[1]), 'train.png'))
        self.cur_index = 0
    
    def on_draw(self):
        self.clear()
        self.background.draw()
        for x in self.list_train:
            x.draw()
        
    def on_mouse_press(self, x, y, button, modifier):
        if button == mouse.LEFT:
            # write_content('{},{}\n'.format(x, y))
            self.cur_index += 1
            for x in self.list_train:
                temporary = self.list_move[self.cur_index].split(',')
                x.posx = int(temporary[0])
                x.posy = int(temporary[1])
    
    def update(self, dt):
        for x in self.list_train:
            x.update()


def main():
    window = Window(1360, 768, 'Visualzation')
    pyglet.clock.schedule_interval(window.update, window.frame_rate)
    pyglet.app.run()


if __name__ == '__main__':
    main()