#!/usr/bin/env python
# William Wu, 2013-08-12
# <william.wu@themathpath.com>

import Image, ImageDraw, ImageFont, ImageEnhance
import sys, os, subprocess, getopt, hashlib, time, numpy

# usage
def usage():
    print('Usage:\n\t%s -i [input_filename] -o [output_filename]' % sys.argv[0])
    print('Optional:')
    print('\t%-30s %-30s' % ("-i [input_filename]", "input filename"))
    print('\t%-30s %-30s' % ("-o [output_filename]", "output filename"))
    print('\t%-30s %-30s' % ("-f [format]", "format of output image"))
    print('\t%-30s %-30s' % ("-w [watermark_image]", "watermark image"))
    print('\t%-30s %-30s' % ("-p [position]", "position of watermark"))
    print('\t%-30s %-30s' % ("-c [opacity]", "opacity of textual watermark"))
    print('\t%-30s %-30s' % ("-t [text]", "text to be added as watermark"))
    
if len(sys.argv) < 2:
    usage()
    sys.exit()

def reduce_opacity(im, opacity):
    """Returns an image with reduced opacity."""
    assert opacity >= 0 and opacity <= 1
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    else:
        im = im.copy()
    alpha = im.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    im.putalpha(alpha)
    return im

def add_watermark_image(im, mark, position_x, position_y, mode=None, opacity=1):
    """Adds a watermark to an image."""
    if opacity < 1:
        mark = reduce_opacity(mark, opacity)
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    # create a transparent layer the size of the image and draw the
    # watermark in that layer.
    layer = Image.new('RGBA', im.size, (0,0,0,0))
    if mode == 'tile':
        for y in range(0, im.size[1], mark.size[1]):
            for x in range(0, im.size[0], mark.size[0]):
                layer.paste(mark, (x, y))
    elif mode == 'scale':
        # scale, but preserve the aspect ratio
        ratio = min(
            float(im.size[0]) / mark.size[0], float(im.size[1]) / mark.size[1])
        w = int(mark.size[0] * ratio)
        h = int(mark.size[1] * ratio)
        mark = mark.resize((w, h))
        layer.paste(mark, ((im.size[0] - w) / 2, (im.size[1] - h) / 2))
    else:
        layer.paste(mark, (position_x, position_y))
    # composite the watermark with the layer
    return Image.composite(layer, im, layer)

def add_watermark_text(im, text, angle=23, opacity=0.25, font='/Library/Fonts/Copperplate.ttc'):
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    watermark = Image.new('RGBA', im.size, (0,0,0,0))
    size = 2
    n_font = ImageFont.truetype(font, size)
    n_width, n_height = n_font.getsize(text)
    # grow size until the limit is reached
    while n_width+n_height < watermark.size[0]:
        size += 2
        n_font = ImageFont.truetype(font, size)
        n_width, n_height = n_font.getsize(text)
    draw = ImageDraw.Draw(watermark, 'RGBA')
    draw.text(((watermark.size[0] - n_width) / 2,
              (watermark.size[1] - n_height) / 2),
              text, (0,0,0), font=n_font)
    watermark = watermark.rotate(angle,Image.BICUBIC)
    alpha = watermark.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    watermark.putalpha(alpha)
    return Image.composite(watermark, im, watermark)
 

# main method
def main(argv):

    # defaults
    input_filename = None
    output_filename = None
    watermark_filename = None
    mode = None
    position_x = 100
    position_y = 100
    text = None
    opacity = 0.15
    show_flag = False
    format = 'PNG'
    format_flag = False
    angle = 0.0

    # command-line arguments
    try:
        opts, args = getopt.gnu_getopt(argv, "hi:o:f:w:p:c:t:a:s:x:y:m:", ["help", "input=","output=","format=","watermark_image","position=","opacity=","text=","angle=","show","position_x=","position_y=","mode="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-i", "--input"):
            input_filename = arg
        elif opt in ("-o", "--output"):
            output_filename = arg
        elif opt in ("-f", "--format"):
            format = arg
            format_flag = True
        elif opt in ("-w", "--watermark_image"):
            watermark_filename = arg
        elif opt in ("-c", "--opacity"):
            opacity = float(arg)
        elif opt in ("-t", "--text"):
            text = arg
        elif opt in ("-a", "--angle"):
            angle = float(arg)
        elif opt in ("-x", "--position_x"):
            position_x = float(arg)
        elif opt in ("-y", "--position_y"):
            position_y = float(arg)
        elif opt in ("-s", "--show"):
            show_flag = True
        elif opt in ("-m", "--mode"):
            mode = arg
    
    # argument checking
    if not os.path.exists(input_filename):
        sys.exit('ERROR: File %s was not found!' % input_filename)
    if None in [input_filename,output_filename]:
        sys.exit('ERROR: Please provide both input and output filenames.')
    if None == watermark_filename and None == text:
        sys.exit('No watermark image or text provided. Exiting.')

    # parse input filename
    basename, ext = os.path.splitext(input_filename)

    # default output image name
    if None == output_filename:
        output_filename = input_filename + "_marked" + ext

    # default output image format == input image format
    if not format_flag:
        format = ext[1:]

    # open input image
    im = Image.open(input_filename)
    
    # image watermark
    if None != watermark_filename:
        mark = Image.open(watermark_filename)
        # watermark(im, mark, 'tile', 0.5).show()
        # watermark(im, mark, 'scale', 1.0).show()
        # watermark(im, mark, (100, 100), 0.5).show()
        im_marked = add_watermark_image(im, mark, position_x, position_y, opacity)
        if show_flag:
            im_marked.show()

    # text watermark
    if None != text:
        im_marked = add_watermark_text(im, text, angle, opacity, font='/Library/Fonts/Copperplate.ttc')

    im_marked.save(output_filename, format)


# invoke main
if __name__ == "__main__":
    main(sys.argv[1:])
