import math
import sys
from time import sleep
import pprint

import sdl2.ext

w = 50
h = 50
d = 10

c = []
hc = []
dc = []
for ci in range(100):
    z = round((255.0 / (100.0 - 1.0)) * ci)
    c.append(sdl2.ext.Color(z, z, z))
    hc.append(sdl2.ext.Color(z, 0, 0))
    dc.append(sdl2.ext.Color(z, z, 0))

src = [[0 for _ in range(w)] for _ in range(h)]

src[18][25] = 99
src[19][25] = 99
src[20][25] = 99

src[24][27] = 99
src[25][27] = 99
src[26][27] = 99

src[30][23] = 99
src[31][23] = 99
src[32][23] = 99

pholo = [0 for i in range(h)]
pdst = [[0 for _x in range(w)] for _y in range(h)]

def recount():

    holo = [0 for _ in range(h)]
    for ry in range(h):
        for rx in range(w):
            if src[ry][rx] > 0:
                dx = 50 - rx
                for hry in range(h):
                    dy = ry - hry
                    hl = dx + math.sqrt(math.pow(dx, 2) + math.pow(dy, 2))
                    ph = math.sin(hl * math.pi)
                    # print(hry, hl, ph)
                    holo[hry] = holo[hry] + ph
                # print("--------")
    pprint.pp(holo)
    minh = min(holo)
    maxh = max(holo)
    dh = (maxh - minh) / 100.0
    print(minh, maxh, dh)

    pholo = [round((holo[i] - minh) / dh) - 1 for i in range(h)]

    print(pholo)

    dst = [[0 for _ in range(w)] for _ in range(h)]

    for ry in range(h):
        for dx in range(w):
            for hry in range(h):
                dy = ry - hry
                hl = math.sqrt(math.pow(dx, 2) + math.pow(dy, 2))
                # FIXME: asin !!!
                ph = math.sin(hl * math.pi)
                dst[ry][dx] = dst[ry][dx] + ph
        pprint.pp(dst[ry])


    mind = 0.0
    maxd = 0.0
    for ry in range(h):
        for rx in range(w):
            mind = min(mind, dst[ry][rx])
            maxd = max(maxd, dst[ry][rx])

    dd = (maxd - mind) / 100.0
    print(mind, maxd, dd)

    pdst = [[round((dst[_y][_x] - mind) / dd) - 1 for _x in range(w)] for _y in range(h)]

    # pprint.pp(pdst)

    return pholo, pdst

def draw_diagram(r):
    for ry in range(h):
        for rx in range(w):
            r.fill([rx * d, ry * d, d, d], c[src[ry][rx]])
            r.fill([(rx + w + 1) * d, ry * d, d, d], dc[pdst[ry][rx]])
        r.fill([50 * d, ry * d, d, d], hc[pholo[ry]])

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    sdl2.ext.init()

    window = sdl2.ext.Window('holo2d demo', size=((w + 1 + w) * d, h * d))
    window.show()

    renderer = sdl2.ext.Renderer(window)
    pholo, pdst = recount()
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
            if e.type == sdl2.SDL_MOUSEBUTTONUP:
                pprint.pp(sdl2.ext.mouse.mouse_coords())

                x,y = sdl2.ext.mouse.mouse_coords()
                src[round(y / 10)][round(x / 10)] = 99

                pholo, pdst = recount()
                draw_diagram(renderer)
                renderer.present()

            # pprint.pp(e.type)
        window.refresh()
        sleep(0.01)
