# nuitka-project: --standalone
# nuitka-project: --onefile
# nuitka-project: --disable-console
# nuitka-project: --enable-plugin=tk-inter
# nuitka-project: --lto=yes
# nuitka-project: --output-dir=.\bin

from typing import List
import tkinter as tk
from tkinter import filedialog

from PIL import Image, ImageTk

PREVIEW_WIDTH = 550
PREVIEW_HEIGHT = 850

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


def save_image(image: Image.Image):
    filename = filedialog.asksaveasfilename(
        initialfile="out", defaultextension=".png", filetypes=[("PNG", "*.png")]
    )
    image.save(filename)


def preview(image: Image.Image):
    window = tk.Tk()
    w = window.winfo_screenwidth()
    h = window.winfo_screenheight()
    x = (w / 2) - (PREVIEW_WIDTH / 2)
    y = (h / 2) - (PREVIEW_HEIGHT / 2)
    window.geometry(f"{PREVIEW_WIDTH}x{PREVIEW_HEIGHT+35}+{int(x)}+{int(y-40)}")

    aspect_ratio = image.width / image.height
    preview_image = None
    if aspect_ratio >= 1:
        preview_image = image.resize((PREVIEW_WIDTH, int(PREVIEW_WIDTH / aspect_ratio)))
    else:
        preview_image = image.resize(
            (int(PREVIEW_HEIGHT * aspect_ratio), PREVIEW_HEIGHT)
        )

    img = ImageTk.PhotoImage(preview_image)
    img_label = tk.Label(window, image=img, width=PREVIEW_WIDTH, height=PREVIEW_HEIGHT)
    img_label.pack()
    save_button = tk.Button(
        window, text="Save Image", command=lambda: save_image(image)
    )
    save_button.pack()

    window.mainloop()


def main():
    files = filedialog.askopenfilenames(
        title="Select Images", initialdir=".", filetypes=supported_extensions
    )
    try:
        images = [Image.open(file) for file in files]
        out = combine_images_vertically(images)
        preview(out)
    except:
        pass


if __name__ == "__main__":
    main()
