# -*- coding: utf-8 -*-
"""
Created on Thu Aug 24 13:30:31 2017
@author: AmosHawk WHU LIESMARS
"""

from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
import sys
import os
# import threading
import cv2

# from PIL import Image
print(("shell name："), sys.argv[0])
print('params list:', str(sys.argv))

if (len(sys.argv) != 5):
    print(
        'the input params should be equal to 4, namely the content, the picture format(eg jpg),the susbsize image height, the subsize image width')
    sys.exit(1)

for i in range(1, len(sys.argv)):
    print("param", i, sys.argv[i])

rootContent = sys.argv[1];
suffixFile = sys.argv[2];
heightsubImage = int(sys.argv[3]);
widthsubImage = int(sys.argv[4]);


def resize(dirFile, suffix):
    # for rootpath, topdown, files in os.walk(dirFile):
    for file in os.listdir(dirFile):
        # singlefileName = os.path.join(rootpath,file)
        singlefileName = dirFile + "\\" + file
        singlefileForm = os.path.splitext(singlefileName)[1][1:]
        if (singlefileForm == suffix):
            print('loading................ : ', singlefileName)
            #               oriImage = Image.open(singlefileName)
            #               oriHei = oriImage.size[0]
            #               oriWid = oriImage.size[1]
            oriImage = cv2.imread(singlefileName)
            oriHei = oriImage.shape[0]
            oriWid = oriImage.shape[1]
            if (oriHei <= heightsubImage | oriWid <= widthsubImage):
                print('image :', singlefileName, 'is smaller than the specified shape')
                sys.exit(1)

            # creat a new subcontent to store the subimages and place it to the upper content
            newSubContent = os.path.splitext(singlefileName)[0][0:]
            if (os.path.exists(newSubContent) == False):
                os.mkdir(newSubContent)

            # calculate the numbers by row and coloum by the specific width and heigh
            nRowNums = oriHei // heightsubImage
            nColNums = oriHei // widthsubImage

            # build a list to store the subimage data for the moment
            subImages = []

            # begin to crop the image
            for i in range(0, nRowNums):
                for j in range(0, nColNums):
                    subImage = oriImage[i * heightsubImage:(i + 1) * heightsubImage,
                               j * widthsubImage:(j + 1) * widthsubImage]
                    subImages.append(subImage)

            # wirte the image to the new created subcontent
            for j in range(1, len(subImages) + 1):
                print('begin to write :', j, 'th subimage of', file)
                savefile = newSubContent + "//" + os.path.splitext(file)[0][0:] + '_' + str(i + j) + '.' + suffix
                cv2.imwrite(savefile, subImages[j - 1])
                print('finish writting')


resize(rootContent, suffixFile)