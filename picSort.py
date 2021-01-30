#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
import argparse
import os
import exifread
from shutil import copy, rmtree

def main():
    parser = argparse.ArgumentParser(
        description=
        'A Script to sort JPG picutures based on their exif metadatas DateTimeOriginal tag'
    )
    parser.add_argument('-sf', required=True, help='This folder needs to be sorted')
    parser.add_argument('-df', required=True, help='Destination folder for sorted pictures')

    global args
    args = parser.parse_args()

    ### Actual copy or move Job bellow ###

    picDateMapping = map_PicDate()
    access_rights = 0o755

    for pic, time in picDateMapping.items():
        folder_dst_yearly = str(time[0:4])
        folder_dst_monthly = str(time[5:7])
        folder_dst_combined = os.path.join(folder_dst_yearly, folder_dst_monthly)
        if not args.df:
            osPath = os.path.join(args.sf, folder_dst_combined) # relativ year/month
        else:
            osPath = os.path.join(args.df, folder_dst_combined)
        if not os.path.exists(osPath):
            os.makedirs(osPath, access_rights, exist_ok=True)
            try:
                print('Copy image', pic, 'to', osPath)
                copy(pic, osPath)
            except IOError as e:
                print("Unable to copy file. %s" % e)
        else:
            try:
                print('Copy image', pic, 'to', osPath)
                copy(pic, osPath)
            except IOError as e:
                print("Unable to copy file. %s" % e)

    renamePictures = 'N'
    renamePictures = input('Do you want to rename the files based on their timestamp? - [y|N]')
    
    if renamePictures == 'y':
        renameFiles(args.df)
    else:
        print('[INFO] Skip file renaming')
    
    # deleteSourceFolder = 'N'
    # deleteSourceFolder = input('[!!!CAUTION!!!] Do you want to delete all original files in {} - [y|N]'.format(args.sf))

  
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

def renameFiles(src):
    fileList = []
    for root, dirs, files in os.walk(src):
        fileList = fileList + [os.path.join(root,x) for x in files if x.endswith(('.jpg','.JPG'))]
    for file in fileList:
        f =  open(file, 'rb')
        dateTime = exifread.process_file(f, details=False, stop_tag='EXIF DateTimeOriginal')
        f.close()
        tag = str(dateTime['EXIF DateTimeOriginal'])
        filename = (tag.replace(' ', '').replace(':', '') + '.JPG')
        dst = os.path.join(os.path.dirname(file), filename)
        os.rename(file, dst)

if __name__ == "__main__":
    main()
