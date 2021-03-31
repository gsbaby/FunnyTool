# -*- coding: utf-8 -*-
"""
Created on Thu Aug 24 13:30:31 2017
@author: AmosHawk,WHU,LIESMARS
"""

from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
import sys
import os
# import threading
from osgeo import gdal, gdalnumeric, gdal_array
from PIL import Image
from functools import reduce
from numpy import *

gdal.UseExceptions()

print(("shell name："), sys.argv[0])
print('params list:', str(sys.argv))

if (len(sys.argv) != 5):
    print(
        'the input params should be equal to 4, namely the content, the picture format(eg jpg),the susbsize image height, the subsize image width')
    sys.exit(1)

for i in range(1, len(sys.argv)):
    print("param", i, sys.argv[i])

rootContent = sys.argv[1]
suffixFile = sys.argv[2]
heightsubImage = int(sys.argv[3])
widthsubImage = int(sys.argv[4])


#  EDIT: this is basically an overloaded
#  version of the gdal_array.OpenArray passing in xoff, yoff explicitly
#  so we can pass these params off to CopyDatasetInfo
#
def OpenArray(array, prototype_ds=None, xoff=0, yoff=0):
    ds = gdal_array.OpenArray((array))

    if ds is not None and prototype_ds is not None:
        if type(prototype_ds).__name__ == 'str':
            prototype_ds = gdal.Open(prototype_ds)
        if prototype_ds is not None:
            gdalnumeric.CopyDatasetInfo(prototype_ds, ds, xoff=xoff, yoff=yoff)
    return ds


def resize(dirFile, suffix):
    # for rootpath, topdown, files in os.walk(dirFile):
    for file in os.listdir(dirFile):
        # singlefileName = os.path.join(rootpath,file)
        singlefileName = dirFile + "\\" + file
        singlefileForm = os.path.splitext(singlefileName)[1][1:]
        if (singlefileForm == suffix):
            print('loading................ : ', singlefileName)
            # Load the source data as a gdalnumeric array
            srcArray = gdalnumeric.LoadFile(singlefileName)

            # Also load as a gdal image to get geotransform
            # (world file) info
            srcImage = gdal.Open(singlefileName)
            # geoTrans = srcImage.GetGeoTransform()

            if srcImage is None:
                print('can not open', singlefileName, 'with gdal')
                sys.exit(1)

            oriHei = srcImage.RasterYSize
            oriWid = srcImage.RasterXSize
            oriBandNum = srcImage.RasterCount

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
            subImagesPos = []
            # begin to crop the image

            if oriBandNum == 1:
                for i in range(0, nRowNums):
                    for j in range(0, nColNums):
                        # subImage = oriImage[i*heightsubImage:(i+1)*heightsubImage,j*widthsubImage:(j+1)*widthsubImage]
                        clip = srcArray[i * heightsubImage:(i + 1) * heightsubImage,
                               j * widthsubImage:(j + 1) * widthsubImage]
                        subImages.append(clip)
                        subImagesPos.append([i * heightsubImage, j * widthsubImage])

            else:
                for i in range(0, nRowNums):
                    for j in range(0, nColNums):
                        # subImage = oriImage[i*heightsubImage:(i+1)*heightsubImage,j*widthsubImage:(j+1)*widthsubImage]
                        clip = srcArray[:, i * heightsubImage:(i + 1) * heightsubImage,
                               j * widthsubImage:(j + 1) * widthsubImage]
                        subImages.append(clip)
                        subImagesPos.append([i * heightsubImage, j * widthsubImage])

            # wirte the image to the new created subcontent
            for j in range(1, len(subImages) + 1):
                print('begin to write :', j, 'th subimage of', file)
                print(type(subImages[j - 1]))
                savefile = newSubContent + "//" + os.path.splitext(file)[0][0:] + '_' + str(j) + '.' + suffix
                gtiffDriver = gdal.GetDriverByName('GTiff')
                if gtiffDriver is None:
                    raise ValueError("Can't find GeoTiff Driver")
                gtiffDriver.CreateCopy(savefile, OpenArray(subImages[j - 1], prototype_ds=singlefileName,
                                                           xoff=subImagesPos[j - 1][1], yoff=subImagesPos[j - 1][0]))
                print('finish writting')


resize(rootContent, suffixFile)