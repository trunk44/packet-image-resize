#!/usr/bin/python3
# -*- coding: utf-8 -*-
# thumbnail creator
#

import os
from PIL import Image, ExifTags, ImageFile
import glob 
from datetime import datetime


ImageFile.LOAD_TRUNCATED_IMAGES = True

size = 128, 128
dir_path = os.path.dirname(os.path.realpath(__file__))

files = glob.glob(dir_path + '/**/*.*', recursive=True)

startTime = datetime.now().replace(microsecond=0)

for infile in files:
    if Image:
        try:
            im = Image.open(infile)
            outfile = os.path.splitext(infile)[0] + ".thumbnail"
            try:
                im.info['exif']
                im.thumbnail(size, Image.ANTIALIAS)
                im.save(outfile, "JPEG", exif=im.info['exif'])
                print("thumb", infile, "created: jpg")
            except:
                im.thumbnail(size, Image.ANTIALIAS)
                im.save(outfile, "PNG")
                print("thumb", infile, "created: png")
        except IOError:
            print("cannot create thumbnail for '%s'" % infile) 
                
                
endTime = datetime.now().replace(microsecond=0) 
print ('\nTime used: ', endTime - startTime)