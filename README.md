# FancyShots
Python script to create fancy screenshots (mainly for apps / websites)

## What does this do?
It turns this:

![Source Image](https://github.com/a1phanumeric/FancyShots/blob/master/input-1.png?raw=true | width=200)

Into this:

![Converted Image](https://raw.githubusercontent.com/a1phanumeric/FancyShots/master/output-1.png | width=200)

## How?
The most basic usage is as follows:

`python fancyshots.py input.png output.png`

Where `input.png` is your original image, and `output.png` is where you'd like the image saved (NOTE: this will overwrite the destination image **without warning**).

### Options
The following options are available to use to configure your output image:

```usage: fancyshots.py [-h] [-t TILT] [-a SHADOWALPHA] [-d DEPTH] [-s DEPTHSTEP]
                     [-v]
                     src_path dst_path

Generate tilted images with depth

positional arguments:
  src_path              The source image file path
  dst_path              The output image file path

optional arguments:
  -h, --help            show this help message and exit
  -t, --tilt            Tilt amount offset (0.5 is a good amount)
  -a, --shadowalpha     The alpha of the shawod (depth). Float between 0-1
  -d, --depth           How deep the image should be
  -s, --depthstep       How many pixels the depth should step each loop
  -v, --verbose         Increase output verbosity```
