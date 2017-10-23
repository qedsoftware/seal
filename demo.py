#!/usr/bin/env python
import seal
import os
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("filename", type=str,
                    help="input image filename")
parser.add_argument("-i", "--inverse", help="invert logo",
                    action="store_true")
parser.add_argument("-s", "--suffix", type=str,
                    help="suffix for output image", default="_qed")
args = parser.parse_args()


if args.inverse:
    logos_dict = {"LR": "qed-logo-rev.png"}
else:
    logos_dict = {"LR": "qed-logo.png"}

sealer = seal.Seal()
base, ext = os.path.splitext(os.path.basename(args.filename))
out_fname = base + args.suffix + ext
sealer.add_logos(args.filename, out_fname, logos_dict)
