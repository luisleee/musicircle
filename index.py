from moviepy.editor import *
from sys import argv
from utils import *
import numpy as np
from seq import *
import cairo

# todo: add comments

screensize = (1920, 1080)

if len(argv) <= 1:
    print("Usage: python3 index.py <input_file>")
    exit(0)

filename = argv[1]

# todo: read config from file
seq, tr = get_seq(
    filename,
    [
        ("guitar", "1.Guitar and Banjo"),
        ("square", "2.SquareWave"),
        ("drum1", "3.Drums1"),
        ("drum2", "4.Drums2"),
        ("broken", "5.BrokenSynth"),
        ("piano", "6.Piano"),
        ("tubular", "7.TubularBell"),
        ("synth1", "8.Synth1"),
        ("synth2", "9.Synth2"),
    ],
)


def w(t):
    return map_range((0, 1), (5, 0), t)


def r(t):
    return map_range((0, 1), (100, 140), t)


def phi(t, omega):
    return t * omega


def make_frame(t):
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, screensize[0], screensize[1])
    ctx = cairo.Context(surface)
    ctx.set_source_rgb(0, 0, 0)
    ctx.rectangle(0, 0, screensize[0], screensize[1])
    ctx.fill()

    c = 0
    first_drum2 = None
    last_drum2 = None
    last_synth1 = []
    for (time, pitch, inst, velocity) in seq:
        if inst == "drum2":
            if time < t:
                last_drum2 = pitch
                if c == 0:
                    first_drum2 = time
                c += 1
            c %= 26 * 4
        if inst == "synth1":
            if time < t:
                last_synth1.append(time)

    for (time, pitch, inst, velocity) in seq:
        if t >= time and t < time + 1:
            delta = t - time
            random.seed(time)
            if inst == "guitar":
                x = random.uniform(0, screensize[0])
                y = random.uniform(0, screensize[1])
                circle(
                    ctx,
                    x,
                    y,
                    r(delta),
                    w(delta),
                    alpha=map_range((45, 100), (0, 1), velocity),
                )
            elif inst == "square":
                x = map_range((0, tr["square"]), (r(1), screensize[0] - r(1)), pitch)
                y = r(1)
                square(ctx, x, y, r(delta), w(delta))
            elif inst == "drum1":
                _x = random.randint(0, 7)
                x = map_range((0, 7), (r(1), screensize[0] - r(1)), _x)
                y = screensize[1] - r(1)

                square(ctx, x, y, r(delta) / 2, w(delta), phi=math.pi / 4)
            elif inst == "drum2":
                if first_drum2 != None:
                    d = t - first_drum2
                    beat = (d * 26 // 15) % 2
                    r_beat = (d * 26 / 15) - int(d * 26 / 15)
                    drift = ((d * -10) % screensize[1] + screensize[1]) % screensize[1]
                    for i in range(-7, 8):
                        blink = (i + beat) % 2 == 0
                        r_ = 10
                        if (i + 7) % 5 == last_drum2:
                            r_ += 20
                        cross(
                            ctx,
                            screensize[1] / 14,
                            i * screensize[1] / 7 + drift,
                            screensize[1] / 14 + map_range((0, 1), (r_, 0), r_beat),
                            20,
                            fill=blink,
                        )
                        cross(
                            ctx,
                            screensize[0] - screensize[1] / 14,
                            screensize[1] - (i * screensize[1] / 7 + drift),
                            screensize[1] / 14 + map_range((0, 1), (r_, 0), r_beat),
                            20,
                            fill=blink,
                        )
            elif inst == "broken":
                if velocity < 100:
                    continue
                x = random.uniform(
                    screensize[1] / 7, screensize[0] - screensize[1] / 7
                )
                y = random.uniform(0, screensize[1])
                phi0 = random.uniform(0, math.pi * 2)
                omega = math.pi / 10
                dir = random.choice([1, -1])
                for i in range(4):
                    eq_triangle(
                        ctx,
                        x,
                        y,
                        100 - (100 - 60 / 2**i) * delta,
                        w(delta),
                        phi=(phi0 + phi(delta, omega * (i + 1))) * dir,
                    )
            elif inst == "piano":
                x = random.uniform(
                    screensize[1] / 7, screensize[0] - screensize[1] / 7
                )
                y = random.uniform(0, screensize[1])
                circle(
                    ctx,
                    x,
                    y,
                    r(delta),
                    w(delta),
                    alpha=map_range((19, 127), (0, 1), velocity),
                )
            elif inst == "tubular":
                x = screensize[0] / 2 + random.uniform(
                    -screensize[0] / 8, screensize[0] / 8
                )
                y = map_range((0, tr["tubular"]), (0, screensize[1]), pitch)
                pentagon(ctx, x, y, r(delta), w(delta))
            elif inst == "synth1":
                notes = last_synth1[-10:]
                arr = []
                for i in notes:
                    random.seed(i)
                    x = random.uniform(0, screensize[0] / 5)
                    y = random.uniform(50, screensize[1] - 50)
                    arr.append((x, y))
                    circle(ctx, x, y, 5, 0, fill=True)
                
                ctx.set_line_width(2)
                for i in range(3):
                    j = len(arr) - 1 - i
                    if j - 1 > 0:
                        alpha = map_range((0, 45 / 104),(1, 0), t - notes[j])
                        ctx.set_source_rgba(1, 1, 1, alpha)
                        ctx.move_to(arr[j][0], arr[j][1])
                        ctx.line_to(arr[j-1][0], arr[j-1][1])
                        ctx.stroke()
            elif inst == "synth2":
                x = screensize[0] - r(1)
                y = map_range(
                    (0, tr["tubular"]),
                    (screensize[1] / 4, screensize[1] / 4 * 3),
                    pitch,
                )
                hexagon(ctx, x, y, r(delta), w(delta))

    buf = surface.get_data()
    arr = np.reshape(buf, (screensize[1], screensize[0], 4))
    return arr[:, :, 2::-1] * np.dstack([arr[:, :, 3] / 255] * 3)


v = VideoClip(make_frame, duration=270)
v.write_videofile("index.mp4", fps=60)
