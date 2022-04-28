import cupy as np


def mask2screen(mask, screensize):
    mask = np.minimum(1, np.maximum(0, mask))
    ones = np.ones(screensize[::-1])
    mask = 255 * (ones - mask)
    return np.dstack([mask] * 3)


def zero_mask(screensize):
    return np.zeros(screensize[::-1])


def Linf_modified(x):
    x[:, :, 0] *= 4
    return np.linalg.norm(x, axis=2, ord=np.inf)


def Linf(x):
    return np.linalg.norm(x, axis=2, ord=np.inf)


def L2(x):
    return np.linalg.norm(x, axis=2, ord=2)


def L1(x):
    return np.linalg.norm(x, axis=2, ord=1)


def opaque(mask, opacity):
    return mask * opacity


def map_range(r1, r2, x):
    (x1, x2) = r1
    (y1, y2) = r2
    return y1 + (x - x1) * (y2 - y1) / (x2 - x1)


def circle_mask(screensize, center, radius, blur=2, norm=L2):
    offset = 1.0 * (radius - blur) / radius
    w, h = screensize

    color = np.array(0).astype(float)
    bg_color = np.array(1).astype(float)

    center = np.array(center[::-1]).astype(float)
    M = np.dstack(np.meshgrid(np.arange(w), np.arange(h))[::-1]).astype(float)
    d = norm(M - center)
    arr = d - offset * radius
    arr = arr / ((1 - offset) * radius)
    arr = np.minimum(1.0, np.maximum(0, arr))

    return (1 - arr) * bg_color + arr * color


def ring_mask(screensize, center, outer_radius, inner_radius, blur=2, norm=L2):
    if outer_radius <= inner_radius:
        return np.zeros(screensize[::-1])
    co = circle_mask(screensize, center, outer_radius, blur, norm)
    ci = circle_mask(screensize, center, inner_radius, blur, norm)
    return co - ci