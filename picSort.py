#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
import argparse
import os
import exifread
from shutil import copy, rmtree
from sys import exit
from tqdm import tqdm

def main():
    parser = argparse.ArgumentParser(
        description=
        'A Script to sort JPG picutures based on their exif metadatas DateTimeOriginal tag'
    )
    parser.add_argument('-sf', required=True, help='This folder needs to be sorted')
    parser.add_argument('-df', required=True, help='Destination folder for sorted pictures')

    global args
    args = parser.parse_args()

    sourceFiles = get_Files()
    
    picDateMapping = map_PicDate()
    access_rights = 0o755
    
    sortNow = input('Found {} pictures...sort now? - [Y|n]'.format(len(sourceFiles))) or 'Y'

    if sortNow == 'Y' or sortNow == 'y':
        ### Actual copy Job ###
        for pic, time in tqdm(picDateMapping.items()):
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
                    copy(pic, osPath)
                except IOError as e:
                    print("Unable to copy file. %s" % e)
            else:
                try:
                    copy(pic, osPath)
                except IOError as e:
                    print("Unable to copy file. %s" % e)
    else:
        print('[INFO] Have a nice day')
        exit(0)

    renamePictures = input('Do you want to rename the files based on their timestamp? - [y|N]') or 'N'
    
    if renamePictures == 'y' or renamePictures == 'Y':
        renameFiles(args.df)
    else:
        print('[INFO] Skip file renaming')
    
    deleteSourceFiles = input('[CAUTION] Do you want to delete all original files in {} - [y|N]'.format(args.sf)) or 'N'

    if deleteSourceFiles == 'y' or deleteSourceFiles == 'Y':
        deleteFiles(sourceFiles)
    else:
        print('[INFO] Skip file renaming')
        exit(0)

  
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

def deleteFiles(files):
    try:
        for file in files:
            os.remove(file)
    except:
        raise
    print('[INFO] Successfully removed {} files.'.format(len(files)))

if __name__ == "__main__":
    main()
