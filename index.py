from moviepy.editor import *
from sys import argv
from random import *
from utils import *
import numpy as np
from seq import *
import cairo
import math

screensize = (1920, 1080)

if len(argv) <= 1:
    print("Usage: python3 index.py <input_file>")
    exit(0)

filename = argv[1]

seq = get_seq(
    filename,
    [("piano", 10), ("harp", 11), ("bell", 12), ("drum", 24), ("pendulum", 25)],
)

max_radius = 200
cute_radius = max_radius / 2

def make_frame(t):
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, screensize[0], screensize[1])
    ctx = cairo.Context(surface)
    ctx.set_source_rgb(1, 1, 1)
    ctx.rectangle(0, 0, screensize[0], screensize[1])
    ctx.fill()
    for (time, pitch, inst) in seq:
        if t >= time and t < time + 1:
            if inst == "piano":
                ctx.set_source_rgb(0, 0, 0)

                ctx.set_line_width(5-(t-time)*5)
                ctx.arc(900, 500, 50+20*(t-time),0 ,2*math.pi)
                ctx.stroke()

    buf = surface.get_data()
    return np.reshape(buf, (screensize[1], screensize[0], 4))[:, :, 2::-1]


v = VideoClip(make_frame, duration=1)
v.write_videofile("index.mp4", fps=60)
