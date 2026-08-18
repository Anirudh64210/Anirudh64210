"""Build assets/watching.gif -- stills that resolve out of heavy pixelation.

Reads every image in assets/watching/ in filename order and renders each one
"processing in": a few blocky frames that sharpen into the real still, a pause,
then on to the next image. Loops forever.

Name the sources so they sort in the order you want, e.g.
    assets/watching/1-psych.jpg
    assets/watching/2-sunny.jpg
"""

import glob
import os
import sys

from PIL import Image, ImageChops

WIDTH, HEIGHT = 480, 270
# how wide the image is downscaled to before being blown back up
STEPS = [6, 9, 13, 19, 27, 38, 54, 76, 108, 152, 214, WIDTH]
STEP_MS = 80
HOLD_MS = 1900

SOURCE_DIR = "assets/watching"
OUTPUT = "assets/watching.gif"
EXTENSIONS = ("*.jpg", "*.jpeg", "*.png", "*.webp")


def sources():
    found = []
    for pattern in EXTENSIONS:
        found.extend(glob.glob(os.path.join(SOURCE_DIR, pattern)))
    return sorted(found)


def fit(image):
    """Cover-crop to the target frame, centred."""
    image = image.convert("RGB")
    scale = max(WIDTH / image.width, HEIGHT / image.height)
    resized = image.resize(
        (max(1, round(image.width * scale)), max(1, round(image.height * scale))),
        Image.LANCZOS,
    )
    left = (resized.width - WIDTH) // 2
    top = (resized.height - HEIGHT) // 2
    return resized.crop((left, top, left + WIDTH, top + HEIGHT))


def scanline_mask():
    mask = Image.new("RGB", (WIDTH, HEIGHT), (255, 255, 255))
    dim = Image.new("RGB", (WIDTH, 1), (184, 184, 184))
    for y in range(0, HEIGHT, 3):
        mask.paste(dim, (0, y))
    return mask


def pixelate(image, blocks):
    small = image.resize((blocks, max(1, round(blocks * HEIGHT / WIDTH))), Image.BILINEAR)
    return small.resize((WIDTH, HEIGHT), Image.NEAREST)


def main():
    paths = sources()
    if not paths:
        sys.exit(
            "no images in %s -- add stills there (e.g. 1-psych.jpg, 2-sunny.jpg)"
            % SOURCE_DIR
        )

    mask = scanline_mask()
    frames, durations = [], []

    for path in paths:
        with Image.open(path) as raw:
            still = fit(raw)
        for blocks in STEPS:
            frames.append(ImageChops.multiply(pixelate(still, blocks), mask))
            durations.append(STEP_MS)
        durations[-1] = HOLD_MS

    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    frames[0].save(
        OUTPUT,
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=0,
        optimize=True,
        disposal=2,
    )
    print("wrote %s -- %d frames from %d stills" % (OUTPUT, len(frames), len(paths)))


if __name__ == "__main__":
    main()
