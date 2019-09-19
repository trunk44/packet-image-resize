#!/usr/bin/python3
# -*- coding: utf-8 -*-
# thumbnail /w exiftags creator
#

import os
from PIL import Image, ExifTags
import glob 

size = 128, 128
dir_path = os.path.dirname(os.path.realpath(__file__))

files = glob.glob(dir_path + '/**/*.*', recursive=True)

for infile in files:
    if Image:
       
        outfile = os.path.splitext(infile)[0] + ".thumbnail"
        if infile != outfile:
            try:
                im = Image.open(infile)
                exif = im.info['exif']
                im.thumbnail(size, Image.ANTIALIAS)
                im.save(outfile, "JPEG",  exif=exif)
                print("thumb", infile, "created")
            except IOError:
                print("cannot create thumbnail for '%s'" % infile)        
            