#!/usr/bin/env python3
import seal
import os
import argparse
import glob


def insert_suffix(path, suffix):
    base, ext = os.path.splitext(os.path.basename(path))
    directory = os.path.dirname(path)
    return directory + ("" if len(directory) ==
                        0 else "/") + base + suffix + ext


parser = argparse.ArgumentParser()
parser.add_argument("filename", type=str,
                    help="input image filename")
parser.add_argument("-s", "--suffix", type=str,
                    help="suffix for output image", default="_qed")
parser.add_argument("-i", "--inverse", help="invert logo",
                    action="store_true")
parser.add_argument("-o", "--output", type=str, help="output file name")
parser.add_argument("--logo", type=str,
                    help="logo file name", default="qed-logo.png")
parser.add_argument("--position", type=str,
                    help="logo position (LR, LL, UR, UL)", default="LR")
args = parser.parse_args()

if args.inverse:
    logos_dict = {args.position: insert_suffix(args.logo, "-rev")}
else:
    logos_dict = {args.position: args.logo}

sealer = seal.Seal()

for filename in glob.glob(os.path.expandvars(os.path.expanduser(args.filename))):
    print(insert_suffix(filename, args.suffix))
    sealer.add_logos(filename, args.output if args.output else insert_suffix(
        filename, args.suffix), logos_dict)
