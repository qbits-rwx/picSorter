#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

import os
import glob
from datetime import datetime
import exifread
from shutil import copy

# set the folder to look for pictures
picture_dir = 'C:/Users/C5282243/Pictures'
# create a list of pictures found in this directory using glob module
picture_list = glob.glob1(picture_dir, '*.jpg')

# create a list to store the timestamps
timestamp_list = []
timestamp_human_list = []
#
for pic in picture_list:
    os.chdir(picture_dir)
    # Open image file for reading (binary mode)
    f = open(pic, 'rb')
    # create a dict containing DateTimeOriginal aka org creation date
    exif_tags = exifread.process_file(f, details=False, stop_tag='DateTimeOriginal')
    for key, value in exif_tags.items():
        if key.startswith('Image DateTime'):
            date = str(value).split()
            timestamp_human_list.append(date[0])
#create a dict were key = picture_list and value is timestamp_human_list 
picture_timestamp_dict = dict(zip(picture_list, timestamp_human_list))
# iter over dict
for pic, time in picture_timestamp_dict.items():
    #print(pic, time)
    access_rights = 0o755
    os.chdir(picture_dir)
    pic_folder_dst = str(time).replace(':', '-')
    if not os.path.exists(pic_folder_dst):
        print('Folder', time, 'not found - Create it')
        os.mkdir(pic_folder_dst, access_rights)
        print('copy file', pic, 'to', pic_folder_dst)
        try:
            print('Copy image', pic, 'to', pic_folder_dst)
            copy(pic, pic_folder_dst)
        except IOError as e:
            print("Unable to copy file. %s" % e)
    else:
        print('Folder', time, 'exists ... copy file', pic, 'to folder', pic_folder_dst)
        try:
            print('Copy image', pic, 'to', pic_folder_dst)
            copy(pic, pic_folder_dst)
        except IOError as e:
            print("Unable to copy file. %s" % e)