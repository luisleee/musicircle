from moviepy.editor import *
from graphics import *
from sys import argv
from random import *
import numpy as np
from seq import *

screensize = (1920, 1080)

if len(argv) <= 1:
    print("Usage: python3 index.py <input_file>")
    exit(0)

filename = argv[1]

seq = get_seq(filename, [("harp", 21), ("piano", 22), ("drum", 0)])

max_radius = 200


def make_frame(t):
    frame = zero_mask(screensize)
    for (time, pitch, inst) in seq:
        if t >= time and t < time + 1:
            seed(pitch)
            if inst == "harp":
                r = randint(max_radius, screensize[0] - max_radius)
                frame += ring_mask(
                    screensize,
                    (r, max_radius),
                    max_radius - 100 + 100 * (t - time),
                    max_radius - 110 + 110 * (t - time),
                )
            elif inst == "piano":
                r = randint(max_radius * 2, screensize[1] - max_radius)
                frame += ring_mask(
                    screensize,
                    (max_radius, r),
                    max_radius - 100 + 100 * (t - time),
                    max_radius - 110 + 110 * (t - time),
                    norm=Linf_modified,
                )
            elif inst == "drum":
                frame += ring_mask(
                    screensize,
                    (screensize[0] - max_radius, screensize[1] / 2),
                    max_radius - 100 + 100 * (t - time),
                    max_radius - 110 + 110 * (t - time),
                    norm=L1,
                )
    return mask2screen(frame, screensize)

v = VideoClip(make_frame, duration=1)
v.write_videofile("index.mp4", fps=60)