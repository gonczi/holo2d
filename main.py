import math
import sys
from time import sleep
import pprint

import sdl2.ext

w = 100
h = 50
d = 10

c = []
for ci in range(100):
    z = round((255.0 / (100.0 - 1.0)) * ci)
    c.append(sdl2.ext.Color(z, z, z))

src = [[0 for _ in range(w)] for _ in range(h)]

src[18][25] = 99
src[19][25] = 99
src[20][25] = 99

src[24][25] = 99
src[25][25] = 99
src[26][25] = 99

src[30][25] = 99
src[31][25] = 99
src[32][25] = 99

for hy in range(h):
    hx = 50


def draw_diagram(r):
    for rx in range(w):
        for ry in range(h):
            r.fill([rx * d, ry * d, d, d], c[src[ry][rx]])

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    sdl2.ext.init()

    window = sdl2.ext.Window('holo2d demo', size=(w * d, h * d))
    window.show()

    renderer = sdl2.ext.Renderer(window)
    draw_diagram(renderer)
    renderer.present()

    running = True
    while running:
        for e in sdl2.ext.get_events():
            if e.type == sdl2.SDL_QUIT:
                running = False
                break
            if e.type == sdl2.SDL_KEYDOWN:
                if e.key.keysym.sym == sdl2.SDLK_ESCAPE:
                    running = False
                    break
        window.refresh()
        sleep(0.01)
