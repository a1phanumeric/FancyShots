import sys
import argparse
from PIL import Image

# Crop the transparent pixels around the image
# Credit: https://gist.github.com/odyniec/3470977
def autocrop_image(image, border = 0):
    bbox = image.getbbox()
    image = image.crop(bbox)
    (width, height) = image.size
    width += border * 2
    height += border * 2
    cropped_image = Image.new("RGBA", (width, height), (0,0,0,0))
    cropped_image.paste(image, (border, border))
    return cropped_image

# Pass 'n' parse arguments
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
img = img.transform((new_width,
                    height+200),
                    Image.AFFINE,
                    (1, m, -xshift if m > 0 else 0, 0, 1, 0),
                    Image.BICUBIC)

top_img = img.copy()
bg_img = img.point(lambda p: p * args.shadowalpha)

output_img = Image.new("RGBA",(new_width, height+200))

# Add shadow copies
startypos = args.depth * args.depthstep
for x in range(0,args.depth):
    ypos = startypos - (x*args.depthstep)
    output_img.paste(bg_img, (0, ypos), bg_img)

# Add top (main) image, clean the image and save
output_img.paste(top_img, (0, ypos), top_img)
output_img = autocrop_image(output_img)

# Should calculate this properly, but for now (and using the
# default settings) this works fine. What we're doing is
# cropping a few pixles off the bottom - otherwise it looks
# a bit weird on the final release
(width, height) = output_img.size
crop_area = (0, 0, width, height-(args.depth*2))
output_img.crop(crop_area).save(args.dst_path)

print('Image processing complete: ' + args.dst_path)
