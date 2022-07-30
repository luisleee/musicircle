import math
import random


def map_range(r1, r2, x):
    (x1, x2) = r1
    (y1, y2) = r2
    return y1 + (x - x1) * (y2 - y1) / (x2 - x1)


def pol2rec(rho, theta):
    return (rho * math.cos(theta), rho * math.sin(theta))


def circle(ctx, x, y, r, w, color=(1, 1, 1), alpha=1, phi=0, fill=False):
    ctx.save()
    ctx.translate(x, y)
    ctx.set_line_width(w)
    ctx.rotate(phi)
    ctx.set_source_rgba(color[0], color[1], color[2], alpha)

    ctx.arc(0, 0, r, 0, 2 * math.pi)
    if fill:
        ctx.fill()
    else:
        ctx.stroke()
    ctx.restore()


def star(ctx, x, y, r, w, color=(1, 1, 1), alpha=1, phi=0):
    ctx.save()
    ctx.translate(x, y)
    ctx.set_line_width(w)
    ctx.rotate(phi)
    ctx.set_source_rgba(color[0], color[1], color[2], alpha)

    theta0 = -math.pi / 10
    x0, y0 = pol2rec(r, theta0)

    c = math.sin(math.pi / 10) / math.sin(math.pi * 3 / 10)
    ctx.move_to(x0, y0)
    for i in range(10):
        ri = r
        if i % 2 == 0:
            ri *= c
        theta = theta0 + (i + 1) * math.pi / 5
        xi, yi = pol2rec(ri, theta)
        ctx.line_to(xi, yi)

    ctx.stroke()
    ctx.restore()


def square(ctx, x, y, r, w, color=(1, 1, 1), alpha=1, phi=0):
    ctx.save()
    ctx.translate(x, y)
    ctx.set_line_width(w)
    ctx.rotate(phi)
    ctx.set_source_rgba(color[0], color[1], color[2], alpha)

    r *= math.sqrt(2)
    theta0 = math.pi / 4
    x0, y0 = pol2rec(r, theta0)

    ctx.move_to(x0, y0)
    for i in range(4):
        theta = theta0 + (i + 1) * math.pi / 2
        xi, yi = pol2rec(r, theta)
        ctx.line_to(xi, yi)

    ctx.stroke()
    ctx.restore()


def hexagon(ctx, x, y, r, w, color=(1, 1, 1), alpha=1, phi=0):
    ctx.save()
    ctx.translate(x, y)
    ctx.set_line_width(w)
    ctx.rotate(phi)
    ctx.set_source_rgba(color[0], color[1], color[2], alpha)

    theta0 = math.pi / 2
    x0, y0 = pol2rec(r, theta0)

    ctx.move_to(x0, y0)
    for i in range(6):
        theta = theta0 + (i + 1) * math.pi / 3
        xi, yi = pol2rec(r, theta)
        ctx.line_to(xi, yi)

    ctx.stroke()
    ctx.restore()


def pentagon(ctx, x, y, r, w, color=(1, 1, 1), alpha=1, phi=0):
    ctx.save()
    ctx.translate(x, y)
    ctx.set_line_width(w)
    ctx.rotate(phi)
    ctx.set_source_rgba(color[0], color[1], color[2], alpha)

    theta0 = math.pi / 2
    x0, y0 = pol2rec(r, theta0)

    ctx.move_to(x0, y0)
    for i in range(5):
        theta = theta0 + (i + 1) * math.pi * 2 / 5
        xi, yi = pol2rec(r, theta)
        ctx.line_to(xi, yi)

    ctx.stroke()
    ctx.restore()


def eq_triangle(ctx, x, y, r, w, color=(1, 1, 1), alpha=1, phi=0):
    ctx.save()
    ctx.translate(x, y)
    ctx.set_line_width(w)
    ctx.rotate(phi)
    ctx.set_source_rgba(color[0], color[1], color[2], alpha)

    theta0 = 0
    x0, y0 = pol2rec(r, theta0)

    ctx.move_to(x0, y0)
    for i in range(3):
        theta = theta0 + (i + 1) * math.pi * 2 / 3
        xi, yi = pol2rec(r, theta)
        ctx.line_to(xi, yi)

    ctx.stroke()
    ctx.restore()


def cross(ctx, x, y, r, w, color=(1, 1, 1), alpha=1, fill=False):
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(math.pi / 4)
    ctx.set_source_rgba(color[0], color[1], color[2], alpha)

    arr = [
        (-w / 2, r),
        (-w / 2, w / 2),
        (-r, w / 2),
        (-r, -w / 2),
        (-w / 2, -w / 2),
        (-w / 2, -r),
        (w / 2, -r),
        (w / 2, -w / 2),
        (r, -w / 2),
        (r, w / 2),
        (w / 2, w / 2),
        (w / 2, r),
    ]

    x0, y0 = arr[-1]
    ctx.move_to(x0, y0)
    for i in arr:
        xi, yi = i
        ctx.line_to(xi, yi)

    if fill:
        ctx.fill()
    else:
        ctx.stroke()
    ctx.restore()
