#!/usr/bin/env python3
import seal.seal
import os
import argparse
import glob
import pkg_resources


def insert_suffix(path, suffix):
    base, ext = os.path.splitext(os.path.basename(path))
    directory = os.path.dirname(path)
    return directory + ("" if len(directory) ==
                        0 else "/") + base + suffix + ext


def main():
    default_logo = "watermark/qed-logo.png"

    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=str,
                        help="input image filename")
    parser.add_argument("-s", "--suffix", type=str,
                        help="suffix for output image", default="_qed")
    parser.add_argument("-i", "--inverse", help="invert logo",
                        action="store_true")
    parser.add_argument("--byline", help="byline logo", action="store_true")
    parser.add_argument(
        "--monochrome", help="one color logo", action="store_true")
    parser.add_argument("--rectangular", help="use rectangular logo",
                        action="store_true")
    parser.add_argument("-o", "--output", type=str, help="output file name")
    parser.add_argument("--logo", type=str,
                        help="logo file name", default=default_logo)
    parser.add_argument("--position", type=str,
                        help="logo position (LR, LL, UR, UL)", default="LR")
    parser.add_argument("--opacity", type=float,
                        help="logo opacity (0.0 - 1.0)", default=1.0)
    parser.add_argument("--filter", type=str,
                        help="logo filter (positive, negative, dark, white)", default="positive")
    args = parser.parse_args()

    logo = args.logo

    if logo == default_logo:
        if not args.rectangular:
            logo = insert_suffix(logo, "-square")

        if args.byline:
            logo = insert_suffix(logo, "-byline")

        if args.monochrome:
            logo = insert_suffix(logo, "-1c")

        if args.inverse:
            logo = insert_suffix(logo, "-rev")
        
        logo = pkg_resources.resource_filename(__name__, logo)

    logos_dict = {args.position: logo}

    sealer = seal.seal.Seal()

    for filename in glob.glob(os.path.expandvars(os.path.expanduser(args.filename))):
        print(insert_suffix(filename, args.suffix))
        sealer.add_logos(filename, args.output if args.output else insert_suffix(
            filename, args.suffix), logos_dict, args.opacity, args.filter)
