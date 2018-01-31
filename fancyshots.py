import sys
import argparse
from PIL import Image

# Pass arguments
parser = argparse.ArgumentParser(description='Generate tilted images with depth')
parser.add_argument("src_path", type=str, help='The source image file path')
parser.add_argument("dst_path", type=str, help='The output image file path')
parser.add_argument("-t", "--tilt", type=float, default=0.5, help='Tilt amount offset (0.5 is a good amount)')
parser.add_argument("-a", "--shadowalpha", type=float, default=0.75, help='The alpha of the shawod (depth). Float between 0-1')
parser.add_argument("-d", "--depth", type=int, default=10, help='How deep the image should be')
parser.add_argument("-s", "--depthstep", type=int, default=5, help='How many pixels the depth should step each loop')
parser.add_argument("-v", "--verbose", action="store_true", help='Increase output verbosity')

args = parser.parse_args()
if(args.verbose):
    print("Input file: " + args.src_path)
    print("Output file: " + args.dst_path)
    print("Tilt: " + str(args.tilt))
    print("Shadow alpha: " + str(args.shadowalpha))
    print("Depth: " + str(args.depth))
    print("Depth step: " + str(args.depthstep))

img = Image.open(args.src_path).convert("RGBA")
if(args.verbose):
    print(img.format, img.size, img.mode)
width, height = img.size
m = -args.tilt
xshift = abs(m) * width

if(args.verbose):
    print("")
    print("Image Info:")
    print("abs(m): " + str(abs(m)))
    print("Width: " + str(width))
    print("Result: " + str(xshift))

new_width = width + (int(round(xshift))*2)

# Tilt image
img = img.transform((new_width, height+200), Image.AFFINE,
        (1, m, -xshift if m > 0 else 0, 0, 1, 0), Image.BICUBIC)

top_img = img.copy()
bg_img = img.point(lambda p: p * args.shadowalpha)

output_img = Image.new("RGBA",(new_width, height+200))

startypos = args.depth * args.depthstep
for x in range(0,args.depth):
    ypos = startypos - (x*args.depthstep)
    output_img.paste(bg_img, (0, ypos), bg_img)

output_img.paste(top_img, (0, ypos), top_img)
output_img.save(args.dst_path)

print('Image processing complete: ' + args.dst_path)
