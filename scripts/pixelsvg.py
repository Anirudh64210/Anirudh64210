"""Generate the pixel-font SVGs for the README: nameplate, typing line,
section titles (dark + light variants) and the inventory panel.

Everything is drawn as <rect> pixels from a 5x7 bitmap font, so there are no
font dependencies and it renders identically everywhere GitHub shows an <img>.
Run: python3 pixelsvg.py  (writes into ./assets)
"""
import os

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")

BG, BORDER, AMBER, SAGE, RUST, TEXT, DIM = (
    "#14110E", "#3D3428", "#E8B44A", "#7F9172", "#C1633C", "#D9CDB8", "#8C7A5E")
AMBER_LIGHT, LINE_LIGHT = "#9A6B12", "#D8CCB6"

F = {
 "A": [".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"],
 "B": ["####.", "#...#", "#...#", "####.", "#...#", "#...#", "####."],
 "C": [".###.", "#...#", "#....", "#....", "#....", "#...#", ".###."],
 "D": ["####.", "#...#", "#...#", "#...#", "#...#", "#...#", "####."],
 "E": ["#####", "#....", "#....", "####.", "#....", "#....", "#####"],
 "F": ["#####", "#....", "#....", "####.", "#....", "#....", "#...."],
 "G": [".###.", "#...#", "#....", "#.###", "#...#", "#...#", ".####"],
 "H": ["#...#", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"],
 "I": [".###.", "..#..", "..#..", "..#..", "..#..", "..#..", ".###."],
 "J": ["..###", "...#.", "...#.", "...#.", "...#.", "#..#.", ".##.."],
 "K": ["#...#", "#..#.", "#.#..", "##...", "#.#..", "#..#.", "#...#"],
 "L": ["#....", "#....", "#....", "#....", "#....", "#....", "#####"],
 "M": ["#...#", "##.##", "#.#.#", "#.#.#", "#...#", "#...#", "#...#"],
 "N": ["#...#", "#...#", "##..#", "#.#.#", "#..##", "#...#", "#...#"],
 "O": [".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
 "P": ["####.", "#...#", "#...#", "####.", "#....", "#....", "#...."],
 "Q": [".###.", "#...#", "#...#", "#...#", "#.#.#", "#..#.", ".##.#"],
 "R": ["####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"],
 "S": [".####", "#....", "#....", ".###.", "....#", "....#", "####."],
 "T": ["#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."],
 "U": ["#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
 "V": ["#...#", "#...#", "#...#", "#...#", "#...#", ".#.#.", "..#.."],
 "W": ["#...#", "#...#", "#...#", "#.#.#", "#.#.#", "#.#.#", ".#.#."],
 "X": ["#...#", "#...#", ".#.#.", "..#..", ".#.#.", "#...#", "#...#"],
 "Y": ["#...#", "#...#", ".#.#.", "..#..", "..#..", "..#..", "..#.."],
 "Z": ["#####", "....#", "...#.", "..#..", ".#...", "#....", "#####"],
 "0": [".###.", "#...#", "#..##", "#.#.#", "##..#", "#...#", ".###."],
 "1": ["..#..", ".##..", "..#..", "..#..", "..#..", "..#..", ".###."],
 "2": [".###.", "#...#", "....#", "...#.", "..#..", ".#...", "#####"],
 "3": ["####.", "....#", "....#", ".###.", "....#", "....#", "####."],
 "4": ["...#.", "..##.", ".#.#.", "#..#.", "#####", "...#.", "...#."],
 "5": ["#####", "#....", "####.", "....#", "....#", "#...#", ".###."],
 "6": [".###.", "#....", "#....", "####.", "#...#", "#...#", ".###."],
 "7": ["#####", "....#", "...#.", "..#..", ".#...", ".#...", ".#..."],
 "8": [".###.", "#...#", "#...#", ".###.", "#...#", "#...#", ".###."],
 "9": [".###.", "#...#", "#...#", ".####", "....#", "....#", ".###."],
 ".": [".....", ".....", ".....", ".....", ".....", "..#..", "..#.."],
 ",": [".....", ".....", ".....", ".....", "..#..", "..#..", ".#..."],
 "'": ["..#..", "..#..", ".....", ".....", ".....", ".....", "....."],
 "-": [".....", ".....", ".....", ".###.", ".....", ".....", "....."],
 "+": [".....", "..#..", "..#..", "#####", "..#..", "..#..", "....."],
 "/": ["....#", "...#.", "...#.", "..#..", ".#...", ".#...", "#...."],
 ":": [".....", "..#..", "..#..", ".....", "..#..", "..#..", "....."],
 "!": ["..#..", "..#..", "..#..", "..#..", "..#..", ".....", "..#.."],
 "?": [".###.", "#...#", "....#", "...#.", "..#..", ".....", "..#.."],
 ">": [".#...", "..#..", "...#.", "....#", "...#.", "..#..", ".#..."],
 "*": [".....", ".....", "..#..", ".###.", "..#..", ".....", "....."],
 " ": ["....."] * 7,
}
ADV = 6  # 5px glyph + 1px gap


def width(s, scale):
    return (len(s) * ADV - 1) * scale


def text(s, x, y, scale, fill):
    """Pixel text as merged horizontal runs of <rect>."""
    out = []
    for i, ch in enumerate(s.upper()):
        g = F[ch]
        for r, row in enumerate(g):
            c = 0
            while c < 5:
                if row[c] == "#":
                    start = c
                    while c < 5 and row[c] == "#":
                        c += 1
                    out.append('<rect x="%d" y="%d" width="%d" height="%d"/>' % (
                        x + (i * ADV + start) * scale, y + r * scale, (c - start) * scale, scale))
                else:
                    c += 1
    return '<g fill="%s">%s</g>' % (fill, "".join(out))


def svg(w, h, body, label):
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" '
            'shape-rendering="crispEdges" role="img" aria-label="%s">%s</svg>\n') % (w, h, w, h, label, body)


def scanlines(w, h):
    return ('<defs><pattern id="scan" width="1" height="3" patternUnits="userSpaceOnUse">'
            '<rect width="1" height="1" fill="#000" opacity="0.28"/></pattern></defs>'
            '<rect width="%d" height="%d" fill="url(#scan)"/>') % (w, h)


def write(name, content):
    with open(os.path.join(OUT, name), "w") as f:
        f.write(content)


# ── nameplate: the name types itself in, then a blinking cursor ───────────
def nameplate():
    W, H, S = 760, 150, 5
    name = "SAI ANIRUDH SIDDI"
    nw = width(name, S)
    x0, y0 = (W - nw) // 2, 42
    n = len(name)
    step = 0.09
    total = 0.3 + n * step
    kt = ["0"] + ["%.4f" % ((0.3 + k * step) / total) for k in range(1, n + 1)]
    vals = ["0"] + [str((k * ADV) * S) for k in range(1, n + 1)]
    sub = "LAS VEGAS, NV  *  AI ENGINEER  *  PRODUCT BUILDER"
    sw = width(sub, 2)
    body = (
        '<rect width="%d" height="%d" fill="%s"/>' % (W, H, BG) +
        '<rect x="0.5" y="0.5" width="%d" height="%d" fill="none" stroke="%s" shape-rendering="auto"/>' % (W - 1, H - 1, BORDER) +
        # pixel "floor" along the top edge, the sprite stands on this
        "".join('<rect x="%d" y="0" width="8" height="4" fill="%s"/>' % (x, BORDER if (x // 8) % 2 else "#2A241C") for x in range(0, W, 8)) +
        '<clipPath id="reveal"><rect x="%d" y="0" height="%d" width="0">'
        '<animate attributeName="width" calcMode="discrete" dur="%.2fs" fill="freeze" keyTimes="%s" values="%s"/>'
        '</rect></clipPath>' % (x0, H, total, ";".join(kt), ";".join(vals)) +
        '<g clip-path="url(#reveal)">' + text(name, x0, y0, S, AMBER) + '</g>' +
        '<rect x="%d" y="%d" width="%d" height="%d" fill="%s">'
        '<animate attributeName="opacity" values="1;0" calcMode="discrete" dur="1s" begin="%.2fs" repeatCount="indefinite"/>'
        '</rect>' % (x0 + nw + S * 2, y0, S * 4, 7 * S, AMBER, total) +
        '<g opacity="0">' + text(sub, (W - sw) // 2, 104, 2, DIM) +
        '<animate attributeName="opacity" from="0" to="1" dur="0.5s" begin="%.2fs" fill="freeze"/></g>' % (total + 0.2) +
        scanlines(W, H)
    )
    write("nameplate.svg", svg(W, H, body, "Sai Anirudh Siddi, Las Vegas NV, AI engineer"))


# ── typing line: cycles through four one-liners ─────────────────────────────
LINES = [
    "now building toki, a notetaker that never phones home",
    "i taught a fish farm to run itself",
    "we hunted exoplanets in nasa data and won",
    "i take language models apart to see what they think",
]


def typing(color, fname):
    W, H, S = 760, 40, 2
    slot, step, hold = 6.0, 0.055, 2.2
    T = slot * len(LINES)
    y = (H - 7 * S) // 2
    parts = []
    for i, line in enumerate(LINES):
        lw = width(line, S)
        x = (W - lw) // 2
        t0 = i * slot
        times, vals = [0.0], [0]
        for k in range(1, len(line) + 1):
            times.append(t0 + 0.2 + k * step)
            vals.append(k * ADV * S)
        times.append(t0 + 0.2 + len(line) * step + hold)
        vals.append(0)
        if times[1] <= 0:
            times[1] = 0.001
        kt = ";".join("%.5f" % (t / T) for t in times) + ";1"
        vs = ";".join(map(str, vals)) + ";0"
        cid = "t%d" % i
        parts.append(
            '<clipPath id="%s"><rect x="%d" y="0" height="%d" width="0">'
            '<animate attributeName="width" calcMode="discrete" dur="%.1fs" repeatCount="indefinite" keyTimes="%s" values="%s"/>'
            '</rect></clipPath>' % (cid, x, H, T, kt, vs) +
            '<g clip-path="url(#%s)">%s</g>' % (cid, text(line, x, y, S, color)))
    write(fname, svg(W, H, "".join(parts), " / ".join(LINES)))


# ── section titles: same height, same arrow, same dotted rule ───────────────
SECTIONS = ["hello", "abilities", "inventory", "quest log", "xp log", "pizza break", "say hi"]


def title(label, fg, rule, suffix):
    W, H, S = 760, 34, 3
    y = (H - 7 * S) // 2
    t = "> " + label
    tw = width(t, S)
    dots = "".join('<rect x="%d" y="%d" width="3" height="3"/>' % (x, H // 2 - 1)
                   for x in range(tw + 18, W, 9))
    body = text(t, 0, y, S, fg) + '<g fill="%s">%s</g>' % (rule, dots)
    write("title-%s%s.svg" % (label.replace(" ", "-"), suffix), svg(W, H, body, label))


# ── inventory: three shelves of pixel item slots ────────────────────────────
SHELVES = [
    ("LANG", AMBER, ["python", "rust", "go", "scala", "sql", "c"]),
    ("ML", SAGE, ["pytorch", "transformers", "langchain", "fastapi"]),
    ("INFRA", RUST, ["docker", "k8s", "spark", "snowflake", "aws", "linux"]),
]


def inventory():
    W, S = 760, 2
    rowh, pad, top = 40, 18, 16
    H = top * 2 + rowh * len(SHELVES) + 8 * (len(SHELVES) - 1)
    body = ['<rect width="%d" height="%d" fill="%s"/>' % (W, H, BG),
            '<rect x="0.5" y="0.5" width="%d" height="%d" fill="none" stroke="%s" shape-rendering="auto"/>' % (W - 1, H - 1, BORDER)]
    for r, (lab, col, items) in enumerate(SHELVES):
        y = top + r * (rowh + 8)
        body.append(text(lab, 20, y + (rowh - 14) // 2, S, DIM))
        x = 110
        for it in items:
            w = width(it, S) + 2 * 14
            body.append('<rect x="%d" y="%d" width="%d" height="%d" fill="#1C1814" stroke="%s" stroke-width="2"/>' % (x, y + 4, w, rowh - 8, col))
            # corner notches for the pixel-slot look
            for cx, cy in ((x - 1, y + 3), (x + w - 1, y + 3), (x - 1, y + rowh - 7), (x + w - 1, y + rowh - 7)):
                body.append('<rect x="%d" y="%d" width="2" height="2" fill="%s"/>' % (cx, cy, BG))
            body.append(text(it, x + 14, y + (rowh - 14) // 2, S, TEXT))
            x += w + 10
    write("inventory.svg", svg(W, H, "".join(body), "tools: " + ", ".join(i for _, _, its in SHELVES for i in its)))


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    nameplate()
    typing(AMBER, "typing.svg")
    typing(AMBER_LIGHT, "typing-light.svg")
    for s in SECTIONS:
        title(s, AMBER, BORDER, "")
        title(s, AMBER_LIGHT, LINE_LIGHT, "-light")
    inventory()
    print("ok")
