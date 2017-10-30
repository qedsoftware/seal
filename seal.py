#!/usr/bin/env python3
from PIL import Image


class Seal:

    def __init__(self):
        return

    def invert(self, color):
        return [(-i + 255) % 255 for i in color]

    def greyscale(self, color):
        return [int(color[0] * 299 / 1000 + color[1] * 587 / 1000 + color[2] * 114 / 1000) for i in range(4)]

    def add_logos(self, main_fname, out_fname, logos_dict, opacity=1.0, filter="positive"):
        """
        Add logos to an image.
        Logos are expected to be in PNG format to support transparency masks.
        """
        if len(set(logos_dict.keys()) - set(["LR", "LL", "UR", "UL"])) > 0:
            raise Exception(
                "Only LR, LL, UR, UL are supported as keys to the logos dict.")
        if any(map(lambda x: not x.endswith('png'), map(lambda y: y.lower(), logos_dict.values()))):
            raise Exception("Only PNG files are supported.")
        if filter not in ["positive", "negative", "black", "white"]:
            raise Exception(
                "Only positive, negative, black, white filters are available.")

        main = Image.open(main_fname)
        main_w, main_h = main.size
        padding = 50

        for pos, logo_fname in logos_dict.items():
            logo = Image.open(logo_fname)

            # height is resized to a fraction of the main image's height
            ratio = 0.15
            logo_w, logo_h = logo.size
            logo_h_new = int(ratio * main_h)
            logo_w_new = int((float(logo_h_new) / logo_h) * logo_w)
            logo = logo.resize((logo_w_new, logo_h_new))
            if logo_h_new > logo_h:
                print("\tWarning: resized logo height to {} beyond original height of {}".format(
                    logo_h_new, logo_h))
            if logo_w_new > logo_w:
                print("\tWarning: resized logo width to {} beyond original width of {}".format(
                    logo_w_new, logo_w))

            # superimpose logo
            if pos == "LR":
                offset = (main_w - logo_w_new - padding,
                          main_h - logo_h_new - padding)
            elif pos == "LL":
                offset = (padding, main_h - logo_h_new - padding)
            elif pos == "UL":
                offset = (padding, padding)
            elif pos == "UR":
                offset = (main_w - logo_w_new - padding, padding)
            logo = Image.blend(Image.new(logo.mode, logo.size), logo, opacity)

            for x in range(logo_w_new):
                for y in range(logo_h_new):
                    color = list(logo.getpixel((x, y)))
                    alpha = color[3]
                    if alpha != 0:
                        if filter == "negative":
                            color = self.invert(color)
                        elif filter == "white":
                            color = self.greyscale(color)
                        elif filter == "black":
                            color = self.invert(self.greyscale(color))
                    logo.putpixel(
                        (x, y), (color[0], color[1], color[2], alpha))
            main.paste(logo, offset, logo)

        main.save(out_fname)
