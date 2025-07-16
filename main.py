import math
import sys
from time import sleep
import pprint

import sdl2.ext

f = 1.0

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

pholo = [0 for i in range(h * d)]
pdst = [[0 for _x in range(w)] for _y in range(h)]

def recount():

    print("----------")

    holo = [[0,0] for _ in range(h)]
    for ry in range(h):
        for rx in reversed(range(w)):
            if src[ry][rx] > 0:
                dx = w - rx
                for hry in range(h):
                    dy = ry - hry
                    hl = dx + math.sqrt(math.pow(dx, 2) + math.pow(dy, 2))
                    holo[hry][0] = holo[hry][0] + math.sin(hl / (f * math.pi))
                    holo[hry][1] = holo[hry][1] + math.cos(hl / (f * math.pi))
                # print("--------")
                break

    # pprint.pp(holo)
    minh = 0.0
    maxh = 0.0
    for s,c in holo:
        amp = math.sqrt(math.pow(s, 2) + math.pow(c, 2))
        minh = min(amp, minh)
        maxh = max(amp, maxh)

    dh = (maxh - minh) / 99.0
    print(minh, maxh, dh)

    if dh == 0:
        dh = 1

    pholo = [round((math.sqrt(math.pow(holo[i][0], 2) + math.pow(holo[i][1], 2)) - minh) / dh) for i in range(h)]

    print(pholo)

    dst = [[0 for _ in range(w)] for _ in range(h)]

    for ry in range(h):
        for dx in range(w):
            for hry in range(h):
                dy = ry - hry
                hl = math.sqrt(math.pow(dx, 2) + math.pow(dy, 2))
                # ph = holo[hry] * (math.sin(hl * (math.pi)))
                #  ph = ((pholo[hry] / 100) * (math.sin(hl * (math.pi)))) + math.sin(dx * (math.pi))


                r = math.sqrt(math.pow(holo[hry][0], 2) + math.pow(holo[hry][1], 2))
                fi = math.atan2(holo[hry][0], holo[hry][1]) # FIXME, maybe wrong order
                if fi < 0.0:
                    fi = (fi + (math.pi * 2))


                ph = ((pholo[hry] / 100) * (math.sin(hl * (f * math.pi))))



                dst[ry][dx] = dst[ry][dx] + ph
        # pprint.pp(dst[ry])


    mind = 0.0
    maxd = 0.0
    for ry in range(h):
        for rx in range(w):
            mind = min(mind, dst[ry][rx])
            maxd = max(maxd, dst[ry][rx])

    dd = (maxd - mind) / 99.0
    print(mind, maxd, dd)

    if dd == 0:
        dd = 1

    pdst = [[round((dst[_y][_x] - mind) / dd) for _x in range(w)] for _y in range(h)]

    # pprint.pp(pdst)

    return pholo, pdst

def draw_diagram(r):
    for ry in range(h):
        for rx in range(w):
            r.fill([rx * d, ry * d, d, d], c[src[ry][rx]])
            r.fill([(rx + w + 1) * d, ry * d, d, d], dc[pdst[ry][rx]])
        r.fill([w * d, ry * d, d, d], hc[pholo[ry]])

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
    need_update = True
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
                mx = round(x/d)
                my = round(y/d)

                for x in range(2):
                    for y in range(2):
                        src[my + y][mx + x] = 99

                pholo, pdst = recount()
                draw_diagram(renderer)
                renderer.present()
                need_update = True

            # pprint.pp(e.type)
        if need_update:
            window.refresh()
            need_update = False
        sleep(0.01)
