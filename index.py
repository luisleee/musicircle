from moviepy.editor import *
from sys import argv
from random import *
from utils import *
from seq import *

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
    frame = zero_mask(screensize)
    c = 0
    for (time, pitch, inst) in seq:
        if inst == "pendulum":
            c += 1
        if t >= time and t < time + 1:
            seed(pitch)
            if inst == "harp":
                pos = map_range(
                    (50, 88), (max_radius * 3, screensize[0] - max_radius * 3), pitch
                )
                frame += ring_mask(
                    screensize,
                    (pos, max_radius / 3 + 50),
                    max_radius / 3 - 50 + 100 * (t - time),
                    max_radius / 3 - 60 + 110 * (t - time),
                    norm=L2,
                )
            elif inst == "bell":
                pos = map_range(
                    (55, 72), (max_radius * 3, screensize[0] - max_radius * 3), pitch
                )
                frame += ring_mask(
                    screensize,
                    (pos, screensize[1] - max_radius),
                    max_radius - 100 + 100 * (t - time),
                    max_radius - 110 + 110 * (t - time),
                    norm=Linf,
                )
            elif inst == "piano":
                pos = map_range(
                    (33, 93), (screensize[1] - max_radius / 4, max_radius / 4), pitch
                )
                frame += ring_mask(
                    screensize,
                    (max_radius, pos),
                    max_radius - 100 + 100 * (t - time),
                    max_radius - 110 + 110 * (t - time),
                    norm=Linf_modified,
                )
            elif inst == "drum":
                r = randint(max_radius, screensize[1] - max_radius)
                frame += ring_mask(
                    screensize,
                    (screensize[0] - max_radius, r),
                    max_radius - 100 + 100 * (t - time),
                    max_radius - 110 + 110 * (t - time),
                    norm=L1,
                )
            elif inst == "pendulum":
                frame += opaque(
                    ring_mask(
                        screensize,
                        (
                            screensize[0] / 4 + (c % 2) * screensize[0] / 2,
                            screensize[1] / 2,
                        ),
                        max_radius * 2 - 100 + 100 * (t - time),
                        max_radius * 2 - 110 + 110 * (t - time),
                        norm=L2,
                    ),
                    0.3,
                )
    return mask2screen(frame, screensize)


v = VideoClip(make_frame, duration=120)
v.write_videofile("index.mp4", fps=60)