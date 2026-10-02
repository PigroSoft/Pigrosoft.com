#!/usr/bin/env python3
"""Draws the Pigrosoft pig on a 32x32 grid and writes every logo asset.

Run from the repo root:  python3 tools/make_logo.py
Needs Pillow (pip install pillow). Edit the shapes below, rerun, commit the output.
"""
from pathlib import Path
from PIL import Image

N = 32
OUT = Path(__file__).resolve().parent.parent / "assets"

PAL = {
    "K": "#000000",  # outline
    "P": "#F7A8C4",  # skin
    "L": "#FFD9E6",  # highlight
    "D": "#D9668F",  # shade
    "S": "#EE86AB",  # snout
    "N": "#7A2848",  # nostrils, inner ear
    "W": "#FFFFFF",
}

grid = [["." for _ in range(N)] for _ in range(N)]


def put(x, y, c):
    if 0 <= x < N and 0 <= y < N:
        grid[y][x] = c


def ellipse(cx, cy, rx, ry, c):
    for y in range(N):
        for x in range(N):
            if ((x + 0.5 - cx) / rx) ** 2 + ((y + 0.5 - cy) / ry) ** 2 <= 1:
                put(x, y, c)


def rows(x0, y0, spans, c, mirror=True):
    """spans: list of (dx, width) per row, drawn from y0 down; mirrored across the centre."""
    for i, (dx, w) in enumerate(spans):
        for k in range(w):
            put(x0 + dx + k, y0 + i, c)
            if mirror:
                put(N - 1 - (x0 + dx + k), y0 + i, c)


# ears first, so the head overlaps their base
rows(4, 4, [(1, 4), (0, 6), (0, 7), (0, 8), (1, 8), (2, 7), (3, 6)], "P")
rows(4, 4, [(9, 0), (2, 2), (2, 3), (2, 3), (3, 3), (4, 2)], "N")

ellipse(16, 18, 12.4, 10.6, "P")

# shading: light from the top left
filled = lambda x, y: 0 <= x < N and 0 <= y < N and grid[y][x] != "."
for y in range(N):
    for x in range(N):
        if grid[y][x] != "P":
            continue
        if not filled(x + 1, y + 1) or (y > 22 and not filled(x, y + 2)):
            grid[y][x] = "D"
for x, y in ((7, 11), (8, 11), (6, 12), (7, 12), (6, 13), (5, 14), (5, 15)):
    put(x, y, "L")

# snout
ellipse(16, 21.5, 6.6, 4.4, "S")
for y in range(N):
    for x in range(N):
        if grid[y][x] == "S":
            near = [grid[y + dy][x + dx] for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))]
            if any(n in "PDL" for n in near):
                grid[y][x] = "K"
for x in (12, 13, 18, 19):
    for y in (21, 22):
        put(x, y, "N")
rows(11, 19, [(0, 3)], "L", mirror=False)

# closed, sleepy eyes
for x, y in ((8, 14), (9, 15), (10, 15), (11, 15), (12, 14)):
    put(x, y, "K")
    put(N - 1 - x, y, "K")

# blush
rows(6, 19, [(0, 2), (0, 2)], "D")

for x in range(14, 18):
    put(x, 26, "D")

# one pixel black outline around everything
outline = []
for y in range(N):
    for x in range(N):
        if grid[y][x] == "." and any(
            filled(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
        ):
            outline.append((x, y))
for x, y in outline:
    grid[y][x] = "K"


def rects(g, ox=0, oy=0):
    out = []
    for y, row in enumerate(g):
        x = 0
        while x < len(row):
            c = row[x]
            if c == ".":
                x += 1
                continue
            x0 = x
            while x < len(row) and row[x] == c:
                x += 1
            out.append(f'<rect x="{x0 + ox}" y="{y + oy}" width="{x - x0}" height="1" fill="{PAL[c]}"/>')
    return "".join(out)


def svg(body, w, h, title):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
        f'shape-rendering="crispEdges" role="img" aria-label="{title}">'
        f"<title>{title}</title>{body}</svg>\n"
    )


def png(g, scale, bg=None):
    h, w = len(g), len(g[0])
    im = Image.new("RGBA", (w, h), bg or (0, 0, 0, 0))
    for y in range(h):
        for x in range(w):
            if g[y][x] != ".":
                im.putpixel((x, y), tuple(int(PAL[g[y][x]][i : i + 2], 16) for i in (1, 3, 5)) + (255,))
    return im.resize((w * scale, h * scale), Image.NEAREST)


# the same pig with its eyes open, for the click on the home page
awake = [row[:] for row in grid]
for x, y in ((8, 14), (9, 15), (10, 15), (11, 15), (12, 14)):
    awake[y][x] = awake[y][N - 1 - x] = "P"
for ex in (9, 20):
    for y in (13, 14, 15):
        for x in range(ex, ex + 3):
            awake[y][x] = "K"
    awake[13][ex] = "W"

# ---------- the animated logo ----------
# A 40x40 canvas: the pig sits low and left so the Zs have room top right.
# Sixteen frames of a quarter second each make one four second loop.
C, OX, OY = 40, 2, 8
PAL["M"] = "#5A1F3A"

squash = [row[:] for row in grid]  # breathing out: the top half sinks one pixel
for y in range(16, 0, -1):
    squash[y] = grid[y - 1][:]
squash[0] = ["."] * N

twitch = [row[:] for row in grid]  # the right ear flicks
for y in (3, 4):
    for x in range(N - 1, 21, -1):
        twitch[y][x] = grid[y][x - 1]
    twitch[y][22] = "."
twitch[4][22] = "K"

ZS = {
    "z1": (30, 9, ["MMM", ".M.", "MMM"]),
    "z2": (33, 5, ["MMMM", "..M.", ".M..", "MMMM"]),
    "z3": (35, 0, ["MMMMM", "...M.", "..M..", ".M...", "MMMMM"]),
}
#            frame: 0123456789ABCDEF
TIMELINE = {
    "base":   "1111000011100000",
    "squash": "0000111100001111",
    "twitch": "0000000000010000",
    "z1":     "0111111000000000",
    "z2":     "0000111111000000",
    "z3":     "0000000111111000",
}
POSES = {"base": grid, "squash": squash, "twitch": twitch}


def on_canvas(pose, zs=()):
    g = [["."] * C for _ in range(C)]
    for y in range(N):
        for x in range(N):
            g[y + OY][x + OX] = pose[y][x]
    for name in zs:
        zx, zy, art = ZS[name]
        for dy, row in enumerate(art):
            for dx, ch in enumerate(row):
                if ch != ".":
                    g[zy + dy][zx + dx] = ch
    return g


def animated_svg():
    css = [".f{visibility:hidden;animation:4s step-end infinite}"]
    for name, track in TIMELINE.items():
        stops = "".join(
            f"{i * 6.25:g}%{{visibility:{'visible' if v == '1' else 'hidden'}}}" for i, v in enumerate(track)
        )
        css.append(f"#{name}{{animation-name:{name}}}@keyframes {name}{{{stops}}}")
    css.append(
        "@media (prefers-reduced-motion:reduce){.f{animation:none}#base,#z1,#z2,#z3{visibility:visible}}"
    )
    body = f"<style>{''.join(css)}</style>"
    for name, pose in POSES.items():
        body += f'<g class="f" id="{name}">{rects(pose, OX, OY)}</g>'
    for name, (zx, zy, art) in ZS.items():
        body += f'<g class="f" id="{name}">{rects([list(r) for r in art], zx, zy)}</g>'
    return svg(body, C, C, "Pigrosoft pig, snoozing")


def frames():
    for i in range(16):
        pose = next(POSES[n] for n in POSES if TIMELINE[n][i] == "1")
        yield on_canvas(pose, [z for z in ZS if TIMELINE[z][i] == "1"])


def gif(path, scale, bg=None):
    keys = list(PAL)
    flat = [0, 0, 0] if bg is None else [int(bg[i : i + 2], 16) for i in (1, 3, 5)]
    for k in keys:
        flat += [int(PAL[k][i : i + 2], 16) for i in (1, 3, 5)]
    ims = []
    for g in frames():
        im = Image.new("P", (C, C), 0)
        im.putpalette(flat + [0] * (768 - len(flat)))
        for y in range(C):
            for x in range(C):
                if g[y][x] != ".":
                    im.putpixel((x, y), keys.index(g[y][x]) + 1)
        ims.append(im.resize((C * scale, C * scale), Image.NEAREST))
    extra = {"transparency": 0, "disposal": 2} if bg is None else {}
    ims[0].save(path, save_all=True, append_images=ims[1:], duration=250, loop=0, **extra)


def profile(path, size=1024, bg="#F3A9C1"):
    """A square picture for round avatar crops: the pig centred with room to spare."""
    xs = [x for row in grid for x, c in enumerate(row) if c != "."]
    ys = [y for y, row in enumerate(grid) if any(c != "." for c in row)]
    scale = int(size * 0.8) // N
    im = Image.new("RGBA", (size, size), bg)
    pig = png(grid, scale)
    cx = (min(xs) + max(xs) + 1) * scale // 2
    cy = (min(ys) + max(ys) + 1) * scale // 2
    im.alpha_composite(pig, (size // 2 - cx, size // 2 - cy))
    im.convert("RGB").save(path)


PAL.update({"Y": "#F2C230", "B": "#8B5A2B", "G": "#2E9E4F", "R": "#D93025", "A": "#F2A93B", "E": "#BDB6A4"})

ICONS = {
    "icon-timer": """
..KKKKKKKKKKKK..
..KBBBBBBBBBBK..
..KKKKKKKKKKKK..
...KWYYYYYYWK...
...KWWYYYYWWK...
....KWWYYWWK....
.....KWYYWK.....
......KYYK......
.....KWWYWK.....
....KWWWYWWK....
...KWWWWYWWWK...
...KWWYYYYYWK...
..KKKKKKKKKKKK..
..KBBBBBBBBBBK..
..KKKKKKKKKKKK..
................""",
    "icon-lingo": """
................
..KKKKKKKKKKKK..
.KWWWWWWWWWWWWK.
.KWWWWWWWWWWWWK.
.KWWWWWWWWWWWWK.
.KWRRWWAAWWGGWK.
.KWRRWWAAWWGGWK.
.KWWWWWWWWWWWWK.
.KWWWWWWWWWWWWK.
..KKKKWWWKKKKK..
.....KWWK.......
.....KWK........
.....KK.........
................
................
................""",
}


def parse(art):
    g = [list(r) for r in art.strip("\n").split("\n")]
    assert all(len(r) == 16 for r in g) and len(g) == 16, [len(r) for r in g]
    return g


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    (OUT / "pig.svg").write_text(svg(rects(grid), N, N, "Pigrosoft pig, asleep"))
    (OUT / "pig-awake.svg").write_text(svg(rects(awake, OX, OY), C, C, "Pigrosoft pig, awake"))
    (OUT / "pig-animated.svg").write_text(animated_svg())
    gif(OUT / "pig-animated.gif", 8)
    profile(OUT / "pig-profile-pink.png")
    profile(OUT / "pig-profile-mulberry.png", bg="#5A1F3A")
    for name, art in ICONS.items():
        (OUT / f"{name}.svg").write_text(svg(rects(parse(art)), 16, 16, name))
    png(grid, 16).save(OUT / "pig-512.png")
    png(grid, 6).resize((180, 180), Image.NEAREST).save(OUT / "apple-touch-icon.png")
    png(grid, 1).save(OUT.parent / "favicon.ico", sizes=[(32, 32)])
    png(grid, 1).save(OUT / "favicon-32.png")
    print("wrote", sorted(p.name for p in OUT.iterdir()))
