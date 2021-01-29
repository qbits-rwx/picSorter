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
    parser.add_argument('-sf', required=True, help='This folder needs to be sorted')
    parser.add_argument('-df', required=False, help='Destination folder for sorted pictures')

    global args
    args = parser.parse_args()
    
    
def get_Files():
    fileList = []
    for root, dirs, files in os.walk(args.sf):
        fileList = fileList + [os.path.join(root,x) for x in files if x.endswith(('.jpg','.JPG'))]
    return fileList

def map_PicDate():
    #  
    fileList = get_Files()
    DateTimeList = []
    for pic in fileList:
        f =  open(pic, 'rb')
        dateTime = exifread.process_file(f, details=False, stop_tag='EXIF DateTimeOriginal')
        tag = str(dateTime['EXIF DateTimeOriginal'])
        DateTimeList.append(tag)
    return dict(zip(fileList, DateTimeList))
    
    

if __name__ == "__main__":
    main()
    

# >>> print(date_string.replace(':', '_').replace(' ', ''))
# 2020_02_2215_47_19

