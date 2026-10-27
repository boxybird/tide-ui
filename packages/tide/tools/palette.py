"""OKLCH theme compiler and WCAG 2 contrast gate; Python standard library only.

Theme inputs are OKLCH triples (L 0..1, C >=0, H degrees). Foregrounds are
resolved against actual surfaces, never inferred from a theme's name or mode.
Chroma is reduced to fit sRGB before contrast is measured or CSS is emitted.
"""
from __future__ import annotations

import math


def linear_rgb(color):
    light, chroma, hue = color
    a, b = chroma * math.cos(math.radians(hue)), chroma * math.sin(math.radians(hue))
    ll = (light + .3963377774 * a + .2158037573 * b) ** 3
    mm = (light - .1055613458 * a - .0638541728 * b) ** 3
    ss = (light - .0894841775 * a - 1.291485548 * b) ** 3
    return [4.0767416621 * ll - 3.3077115913 * mm + .2309699292 * ss,
            -1.2684380046 * ll + 2.6097574011 * mm - .3413193965 * ss,
            -.0041960863 * ll - .7034186147 * mm + 1.707614701 * ss]


def gamut(color):
    """Keep lightness/hue; find the largest chroma inside the sRGB gamut."""
    light, chroma, hue = color
    if not 0 <= light <= 1 or chroma < 0 or not all(math.isfinite(x) for x in color):
        raise ValueError(f'Invalid OKLCH input: {color}')
    if all(-.0000001 <= n <= 1.0000001 for n in linear_rgb(color)):
        return [round(light, 6), round(chroma, 6), round(hue % 360, 4)]
    low, high = 0., chroma
    for _ in range(32):
        mid = (low + high) / 2
        if all(0 <= n <= 1 for n in linear_rgb([light, mid, hue])):
            low = mid
        else:
            high = mid
    return [round(light, 6), max(0, math.floor(low * 1e6) / 1e6), round(hue % 360, 4)]


def luminance(color):
    r, g, b = linear_rgb(color)
    return .2126 * max(0, r) + .7152 * max(0, g) + .0722 * max(0, b)


def contrast(foreground, background):
    a, b = sorted((luminance(foreground), luminance(background)))
    return (b + .05) / (a + .05)


def from_hex(value):
    """One-time import of the approved reference, not a public CSS format."""
    rgb = [int(value[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    r, g, b = [n / 12.92 if n <= .04045 else ((n + .055) / 1.055) ** 2.4 for n in rgb]
    ll = (.4122214708 * r + .5363325363 * g + .0514459929 * b) ** (1 / 3)
    mm = (.2119034982 * r + .6806995451 * g + .1073969566 * b) ** (1 / 3)
    ss = (.0883024619 * r + .2817188376 * g + .6299787005 * b) ** (1 / 3)
    light = .2104542553 * ll + .793617785 * mm - .0040720468 * ss
    a = 1.9779984951 * ll - 2.428592205 * mm + .4505937099 * ss
    bb = .0259040371 * ll + .7827717662 * mm - .808675766 * ss
    return gamut([light, math.hypot(a, bb), math.degrees(math.atan2(bb, a)) % 360])


def css(color):
    return f'oklch({color[0]:.6f} {color[1]:.6f} {color[2]:.4f})'


def fit(seed, backgrounds, minimum=4.65):
    """Closest passing lightness to seed; test both directions and every surface."""
    seed = gamut(seed)
    if all(contrast(seed, bg) >= minimum for bg in backgrounds):
        return seed
    candidates = []
    for i in range(1001):
        color = gamut([i / 1000, seed[1], seed[2]])
        if all(contrast(color, bg) >= minimum for bg in backgrounds):
            candidates.append(color)
    if not candidates:
        raise ValueError('No common accessible foreground. Split the surface into a new context.')
    return min(candidates, key=lambda c: abs(c[0] - seed[0]))


def mix(a, b, amount):
    """OKLab interpolation, matching color-mix(in oklab, ...)."""
    def lab(c):
        return [c[0], c[1] * math.cos(math.radians(c[2])), c[1] * math.sin(math.radians(c[2]))]
    aa, bb = lab(a), lab(b)
    light, x, y = [(1 - amount) * aa[i] + amount * bb[i] for i in range(3)]
    return gamut([light, math.hypot(x, y), math.degrees(math.atan2(y, x)) % 360])


def resolve(mode):
    canvas, accent_seed = gamut(mode['canvas']), gamut(mode['accent'])
    light_surface = luminance(canvas) > .3
    l, c, h = canvas
    roles = {
        'canvas': canvas,
        'surface': gamut([min(.995, l + .035) if light_surface else min(.97, l + .055), c * .7, h]),
        'raised': gamut([min(.998, l + .06) if light_surface else min(.98, l + .11), c * .45, h]),
        'field': gamut([min(.998, l + .06) if light_surface else min(.98, l + .025), c * .55, h]),
    }
    for key, value in mode.get('overrides', {}).items():
        roles[key] = gamut(value)
    backgrounds = [roles[k] for k in ('canvas', 'surface', 'raised', 'field')]
    fg_l = .20 if light_surface else .96
    for key, value in {
        'text-primary': [fg_l, min(c, .018), h],
        'text-secondary': [.40 if light_surface else .79, min(c, .025), h],
        'text-muted': [.47 if light_surface else .70, min(c, .025), h],
        'text-label': [.44 if light_surface else .75, min(c, .025), h],
        'accent': accent_seed,
    }.items():
        roles[key] = fit(roles.get(key, value), backgrounds)
    roles['on-accent'] = fit(roles.get('on-accent', [0.98 if luminance(roles['accent']) < .3 else .15, .01, h]), [roles['accent']])
    # Move the background away from its foreground so hover cannot erase a
    # just-passing label. A fixed "mix with foreground" recipe fails near 4.5:1.
    roles['accent-state-target'] = [0.,0.,0.] if luminance(roles['on-accent']) > luminance(roles['accent']) else [1.,0.,0.]
    hover = mix(roles['accent'], roles['accent-state-target'], .08)
    roles['on-accent'] = fit(roles['on-accent'], [roles['accent'], hover])
    roles['accent-hover'] = hover
    roles['accent-active'] = mix(roles['accent'], roles['accent-state-target'], .16)
    roles['border-subtle'] = roles.get('border-subtle', gamut([l + (-.14 if light_surface else .14), c * .6, h]))
    roles['border-strong'] = roles.get('border-strong', gamut([l + (-.25 if light_surface else .25), c * .65, h]))
    roles['border-control'] = fit(roles.get('border-control', [.5 if light_surface else .65, min(c, .035), h]), backgrounds, 3.15)
    roles['selected-surface'] = roles.get('selected-surface', mix(roles['surface'], roles['accent'], .12))
    roles['selected-text'] = fit(roles.get('selected-text', roles['accent']), [roles['selected-surface']])
    roles['selected-border'] = fit(roles.get('selected-border', roles['accent']), [roles['selected-surface'], *backgrounds], 3.15)
    roles['focus'] = fit(roles['accent'], [*backgrounds, roles['selected-surface']], 3.15)
    for status, hue in [('success', 150), ('warning', 80), ('danger', 20)]:
        bg_key, text_key, line_key = [f'status-{status}-{suffix}' for suffix in ('surface', 'text', 'border')]
        roles[bg_key] = roles.get(bg_key, gamut([.92 if light_surface else .28, .027, hue]))
        roles[text_key] = fit(roles.get(text_key, [.38 if light_surface else .84, .095, hue]), [roles[bg_key], *backgrounds])
        roles[line_key] = roles.get(line_key, gamut([.67 if light_surface else .48, .06, hue]))
    # A photograph remains a dark reading context even in light mode. Its action
    # retains the theme hue, but uses a separately checked lightness/on-color pair.
    roles['photo-canvas'] = from_hex('#111517')
    roles['photo-text-primary'] = from_hex('#f0f1ed')
    roles['photo-text-secondary'] = from_hex('#b8bfc6')
    roles['photo-text-muted'] = from_hex('#a4bdc0')
    roles['photo-accent'] = fit([max(.817203, accent_seed[0]), accent_seed[1], accent_seed[2]], [roles['photo-canvas']])
    roles['on-photo-accent'] = fit([.229171,.022842,200.5214], [roles['photo-accent']])
    roles['photo-state-target'] = [0.,0.,0.] if luminance(roles['on-photo-accent']) > luminance(roles['photo-accent']) else [1.,0.,0.]
    roles['photo-accent-hover'] = mix(roles['photo-accent'], roles['photo-state-target'], .08)
    roles['photo-accent-active'] = mix(roles['photo-accent'], roles['photo-state-target'], .16)
    roles['on-photo-accent'] = fit(roles['on-photo-accent'], [roles['photo-accent'],roles['photo-accent-hover']])
    roles['texture-opacity'] = mode.get('texture', .025 if light_surface else .2)
    return roles


def checks(roles):
    rows = []
    def add(fg, bg, minimum, purpose):
        ratio = contrast(roles[fg], roles[bg])
        rows.append({'foreground': fg, 'background': bg, 'ratio': round(ratio, 4), 'minimum': minimum, 'pass': ratio >= minimum, 'purpose': purpose})
    for bg in ('canvas', 'surface', 'raised', 'field'):
        for fg in ('text-primary', 'text-secondary', 'text-muted', 'text-label', 'accent', 'accent-hover'):
            add(fg, bg, 4.5, 'Normal-size text')
        add('border-control', bg, 3, 'Control boundary')
        add('focus', bg, 3, 'Focus outline, with a surface-colored gap')
        for status in ('success', 'warning', 'danger'):
            add(f'status-{status}-text', bg, 4.5, 'Status / validation text')
    add('on-accent', 'accent', 4.5, 'Primary button label')
    add('on-accent', 'accent-hover', 4.5, 'Hovered primary button label')
    add('on-accent', 'accent-active', 4.5, 'Active primary button label')
    add('selected-text', 'selected-surface', 4.5, 'Selected option label')
    add('selected-border', 'selected-surface', 3, 'Selected option boundary')
    add('focus', 'selected-surface', 3, 'Selected option focus')
    for status in ('success', 'warning', 'danger'):
        add(f'status-{status}-text', f'status-{status}-surface', 4.5, 'Status badge label')
    for fg in ('photo-text-primary','photo-text-secondary','photo-text-muted','photo-accent'):
        add(fg,'photo-canvas',4.5,'Photo context, opaque base (scrim requires image review)')
    add('on-photo-accent','photo-accent',4.5,'Photo primary button')
    add('on-photo-accent','photo-accent-hover',4.5,'Photo button hover')
    add('on-photo-accent','photo-accent-active',4.5,'Photo button active')
    return rows
