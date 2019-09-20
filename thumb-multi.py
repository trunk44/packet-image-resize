#!/usr/bin/python3
# -*- coding: utf-8 -*-
#  multiprocess thumbnail creator
#

import os
from datetime import datetime
from PIL import Image, ExifTags, ImageFile
import glob 
import multiprocessing
from multiprocessing import Pool

ImageFile.LOAD_TRUNCATED_IMAGES = True

size = 128, 128
dir_path = os.path.dirname(os.path.realpath(__file__))


def fn(infile):
    if Image:
            try:
                im = Image.open(infile)
                outfile = os.path.splitext(infile)[0] + ".thumbnail"
                try:
                    im.info['exif']
                    im.thumbnail(size, Image.ANTIALIAS)
                    im.save(outfile, "JPEG", exif=im.info['exif'])
                    print("thumb", infile, "created:j")
                except:
                    im.thumbnail(size, Image.ANTIALIAS)
                    im.save(outfile, "PNG")
                    print("thumb", infile, "created: png")
            except IOError:
                print("cannot create thumbnail for '%s'" % infile)   
    else:
        pass
                
             
if __name__ == '__main__':
    cpucores = multiprocessing.cpu_count()
    files = glob.glob(dir_path + '/**/*.*', recursive=True)
    startTime = datetime.now().replace(microsecond=0)
    pool = Pool(processes=cpucores + 1)
    pool.map(fn, files)
    endTime = datetime.now().replace(microsecond=0) 

    print ('\nTime used: ', endTime - startTime)
    print('\nCPU Cores: ', cpucores)
    print('\nFlows used: ', cpucores + 1 )