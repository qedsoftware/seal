#!/usr/bin/env python3
import seal
import os
import argparse
import glob


parser = argparse.ArgumentParser()
parser.add_argument("filename", type=str,
                    help="input image filename")
parser.add_argument("-s", "--suffix", type=str,
                    help="suffix for output image", default="_qed")
parser.add_argument("-i", "--inverse", help="invert logo",
                    action="store_true")
parser.add_argument("-o", "--output", type=str, help="output file name")
args = parser.parse_args()


if args.inverse:
    logos_dict = {"LR": "qed-logo-rev.png"}
else:
    logos_dict = {"LR": "qed-logo.png"}

sealer = seal.Seal()

for filename in glob.glob(args.filename):
    base, ext = os.path.splitext(os.path.basename(filename))
    directory = os.path.dirname(filename)
    out_fname = directory + ("" if len(directory) ==
                             0 else "/") + base + args.suffix + ext
    if args.output:
        out_fname = args.output

    sealer.add_logos(filename, out_fname, logos_dict)
