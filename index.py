from moviepy.editor import *
from sys import argv
from utils import *
import numpy as np
from seq import *
import cairo

# TODO: add comments

screensize = (1920, 1080)

if len(argv) <= 1:
    print("Usage: python3 index.py <input_file>")
    exit(0)

filename = argv[1]

# TODO: read config from file
seq, tr, duration = get_seq(
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


r0 = screensize[1] / 14
r1 = r0 + 10
r2 = r0 + 20


def make_frame(t):
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, screensize[0], screensize[1])
    ctx = cairo.Context(surface)
    ctx.set_source_rgb(0, 0, 0)
    ctx.rectangle(0, 0, screensize[0], screensize[1])
    ctx.fill()

    c_drum2 = 0
    first_drum2 = None
    drum2 = [None] * 5
    last_synth1 = []
    for (time, pitch, inst, velocity) in seq:
        if inst == "drum2":
            if time < t:
                drum2[pitch] = time
                if c_drum2 == 0:
                    first_drum2 = time
                c_drum2 += 1
            c_drum2 %= 26 * 4
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
                d = t - first_drum2
                beat = int(d * 26 / 15)
                d_beat = ((d * 26 / 15) - int(d * 26 / 15)) * 15 / 26
                for i in range(15):
                    h = screensize[1]
                    y = -15 / 14 * h + i / 7 * h + int(20 * d) % int(15 / 7 * h)

                    m = ((i % 5) + 5) % 5
                    d_note = 100
                    if drum2[m] != None:
                        d_note = t - drum2[m]

                    radius = max(
                        r0,
                        map_range((0, 13 / 30), (r2, r1), d_note),
                        map_range((0, 13 / 30), (r1, r0), d_beat),
                    )

                    alpha = 1
                    if c_drum2 == 0:
                        last = 0
                        for note in drum2:
                            last = max(last, note)
                        d_last = t - last

                        radius_last = max(
                            r0,
                            map_range((0, 13 / 30), (r2, r1), last - drum2[m]),
                            map_range(
                                (0, 13 / 30),
                                (r1, r0),
                                (
                                    ((last - first_drum2) * 26 / 15)
                                    - int((last - first_drum2) * 26 / 15)
                                )
                                * 15
                                / 26,
                            ),
                        )

                        alpha = map_range((0, 1), (1, 0), d_last)
                        radius = map_range(
                            (0, 1), (radius_last, radius_last + 20), d_last
                        )
                        beat = int((last - first_drum2) * 26 / 15)

                    fill = (i + beat) % 2 == 0

                    cross(
                        ctx,
                        r0,
                        h - y,
                        radius,
                        20,
                        alpha=alpha,
                        fill=fill,
                    )
                    cross(
                        ctx,
                        screensize[0] - r0,
                        y,
                        radius,
                        20,
                        alpha=alpha,
                        fill=fill,
                    )
            elif inst == "broken":
                if velocity < 100:
                    continue
                x = random.uniform(
                    screensize[1] / 7 + 100, screensize[0] - screensize[1] / 7 - 100
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
                        map_range((0, 1), (100, 60 / 2**i), delta),
                        w(delta),
                        phi=(phi0 + phi(delta, omega * (i + 1))) * dir,
                    )
            elif inst == "piano":
                x = random.uniform(
                    screensize[1] / 7 + r(1), screensize[0] - screensize[1] / 7 - r(1)
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
                y = map_range((0, tr["tubular"]), (r(1), screensize[1] - r(1)), pitch)
                pentagon(ctx, x, y, r(delta), w(delta))
            elif inst == "synth1":
                notes = last_synth1[-10:]
                arr = []
                for i in notes:
                    random.seed(i)
                    x = random.uniform(0, screensize[0] / 5)
                    y = random.uniform(50, screensize[1] - 50)
                    arr.append((x, y))
                    circle(
                        ctx,
                        x,
                        y,
                        5,
                        0,
                        alpha=map_range((0, 75 / 52), (1, 0), t - i),
                        fill=True,
                    )

                ctx.set_line_width(2)
                for i in range(3):
                    j = len(arr) - 1 - i
                    if j - 1 > 0:
                        alpha = map_range((0, 45 / 104), (1, 0), t - notes[j])
                        ctx.set_source_rgba(1, 1, 1, alpha)
                        ctx.move_to(arr[j][0], arr[j][1])
                        ctx.line_to(arr[j - 1][0], arr[j - 1][1])
                        ctx.stroke()
            elif inst == "synth2":
                x = screensize[0] - r(1)
                y = map_range(
                    (0, tr["synth2"]),
                    (screensize[1] / 4, screensize[1] / 4 * 3),
                    pitch,
                )
                hexagon(ctx, x, y, r(delta), w(delta))

    buf = surface.get_data()
    arr = np.reshape(buf, (screensize[1], screensize[0], 4))
    return arr[:, :, 2::-1] * np.dstack([arr[:, :, 3] / 255] * 3)

v = VideoClip(make_frame, duration=duration)
v.write_videofile("index.mp4", fps=60)
