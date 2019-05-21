import pyglet
from pyglet.gl import *
from metro_rush import Metro
from time import sleep


def Init():
    def find_index(Graph, line, position):
        for x, y in enumerate(Graph[line]):
            if y.name == Graph[position[0]][position[1]].name:
                return x

    Graph = Metro('delhi-metro-stations')
    output = {}
    point = 1
    for key, list_station in Graph.metro.items():
        temp = []
        for index, _ in enumerate(list_station, 1):
            temp.append(Object(index*40, point*100, 'sta.jpg'))
        point += 1
        output[key.split()[0]] = temp
    
    connect = []
    for key, value in Graph.metro.items():
        for index, ele in enumerate(value):
            if not ele.line:
                continue
            try:
                obj1 = output[key.split()[0]][index]
                obj2 = output[ele.line.split()[0]][find_index(Graph.metro, ele.line, [key, index])]
                connect.append([obj1.posx, obj1.posy, obj2.posx, obj2.posy])
            except TypeError:
                pass
    return output, connect
    

class Object:
    def __init__(self, posx, posy, img):
        self.posx = posx
        self.posy = posy
        self.sprite = self.Sprite(img)
        self.sprite.x = self.posx
        self.sprite.y = self.posy
    
    def draw(self):
        self.sprite.draw()
    
    def Sprite(self, img):
        image = pyglet.image.load(img)
        image.anchor_x = image.width // 2
        image.anchor_y = image.width // 2
        return pyglet.sprite.Sprite(image)
    
    def update(self):
        self.sprite.x = self.posx
        self.sprite.y = self.posy


class Window(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.frame_rate = 1/60.0
        self.graph, self.connect = Init()
        self.color = {
            'Pink' : [255, 20, 147],
            'Red' : [255, 0, 0],
            'Airport' : [255, 69, 0],
            'Violet' : [238, 130, 238],
            'Green' : [84, 255, 159],
            'Yellow' : [255, 255, 0],
            'Blue' : [0, 0, 255],
            'Magenta' : [255, 0, 255]
        }
        
    def on_draw(self):
        self.clear()
        for x in self.connect:
            pyglet.graphics.draw(2, pyglet.gl.GL_LINES,
                            ('v2i', (x[0], x[1], x[2], x[3])),
                            ('c3B', (255, 255, 255, 255, 255, 255)))
        for key, x in self.graph.items():
            x0 = x[0].posx
            y0 = x[0].posy
            x1 = x[-1].posx
            y1 = x[-1].posy
            if key in self.color:
                temp = self.color[key]
                pyglet.graphics.draw(2, pyglet.gl.GL_LINES,
                            ('v2i', (x0, y0, x1, y1)),
                            ('c3B', (temp[0], temp[1], temp[2], temp[0], temp[1], temp[2])))
            else:
                pyglet.graphics.draw(2, pyglet.gl.GL_LINES,
                                    ('v2i', (x0, y0, x1, y1)),
                                    ('c3B', (255, 255, 255, 255, 255, 255)))
            for y in x:
                y.draw()

    def update(self, dt):
        pass


def main():
    window = Window(1920, 768, 'Visualzation')
    pyglet.clock.schedule_interval(window.update, window.frame_rate)
    pyglet.app.run()


if __name__ == '__main__':
    main()
