#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
import argparse
import os
import exifread
from shutil import copy

def main():
    parser = argparse.ArgumentParser(
        description=
        'A Script to sort JPG picutures based on their exif metadatas DateTimeOriginal tag'
    )
    parser.add_argument('-sf', required=True)
    parser.add_argument('-df', required=False)

    global args
    args = parser.parse_args()
    DateTime()

    
def get_Files():
    fileList = []
    for root, dirs, files in os.walk(args.sf):
        fileList = fileList + [os.path.join(root,x) for x in files if x.endswith(('.jpg','.JPG'))]
    return fileList

def DateTime():
    fileList = get_Files()
    PictureDate = []
    for pic in fileList:
        f =  open(pic, 'rb')
        dateTime = exifread.process_file(f, details=False, stop_tag='EXIF DateTimeOriginal')
        PictureDate.append(dateTime['EXIF DateTimeOriginal'])


if __name__ == "__main__":
    main()
    

# >>> print(date_string.replace(':', '_').replace(' ', ''))
# 2020_02_2215_47_19
