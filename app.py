# nuitka-project: --standalone
# nuitka-project: --onefile
# nuitka-project: --disable-console
# nuitka-project: --enable-plugin=tk-inter
# nuitka-project: --lto=yes
# nuitka-project: --output-dir=.\bin

from typing import List

import tkinter as tk
from tkinter import filedialog

from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

exts = Image.registered_extensions()
supported_extensions = {
    ("Image", f"*{ex}") for ex, f in exts.items() if f in Image.OPEN
}


def combine_images_vertically(images: List[Image.Image]) -> Image.Image:
    widths, heights = zip(*(img.size for img in images))

    width = max(widths)
    height = sum(heights)

    out_image = Image.new(images[0].mode, (width, height))

    y_offset = 0
    for img in images:
        out_image.paste(img, (0, y_offset))
        y_offset += img.height

    return out_image


def preview(image: Image.Image):
    fig, ax = plt.subplots()
    ax.imshow(np.asarray(image))
    plt.show()


def main():
    files = filedialog.askopenfilenames(
        title="Select Images", initialdir=".", filetypes=supported_extensions
    )
    try:
        images = [Image.open(file) for file in files]
        out = combine_images_vertically(images)

        while True:
            cmd = input("1. Preview\n2. Save\n3. Quit\n1,2,3: ")
            if cmd == "1":
                preview(out)
            elif cmd == "2":
                out.save("out.png")
            elif cmd == "3":
                break
    except:
        pass


if __name__ == "__main__":
    main()
