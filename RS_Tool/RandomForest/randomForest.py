# -*- coding: utf-8 -*-
import os, sys, time
import gdal
from osgeo import ogr
from osgeo import gdal
from osgeo import gdal_array as ga
from gdalconst import *
from skimage import morphology, filters
import numpy as np
from numba import jit, vectorize, int64
import warnings
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier
from sklearn.ensemble import ExtraTreesClassifier


# 读遥感影像
def read_img(filename):
    dataset = gdal.Open(filename)

    im_width = dataset.RasterXSize
    im_height = dataset.RasterYSize

    im_geotrans = dataset.GetGeoTransform()
    im_proj = dataset.GetProjection()
    im_data = dataset.ReadAsArray(0, 0, im_width, im_height)

    del dataset
    return im_proj, im_geotrans, im_width, im_height, im_data


# 写出图像
def write_img(filename, im_proj, im_geotrans, im_data):
    if 'int8' in im_data.dtype.name:
        datatype = gdal.GDT_Byte
    elif 'int16' in im_data.dtype.name:
        datatype = gdal.GDT_UInt16
    else:
        datatype = gdal.GDT_Float32

    if len(im_data.shape) == 3:
        im_bands, im_height, im_width = im_data.shape
    else:
        im_bands, (im_height, im_width) = 1, im_data.shape

    driver = gdal.GetDriverByName("GTiff")
    dataset = driver.Create(filename, im_width, im_height, im_bands, datatype)

    dataset.SetGeoTransform(im_geotrans)
    dataset.SetProjection(im_proj)

    if im_bands == 1:
        dataset.GetRasterBand(1).WriteArray(im_data)
    else:
        for i in range(im_bands):
            dataset.GetRasterBand(i + 1).WriteArray(im_data[i])

    del dataset


# 根据矢量点获取点对应的像素值，并把点先放入列表中
def getPixels(shp, img):
    driver = ogr.GetDriverByName('ESRI Shapefile')
    ds = driver.Open(shp, 0)
    if ds is None:
        print('Could not open ' + shp)
        sys.exit(1)

    layer = ds.GetLayer()

    xValues = []
    yValues = []
    feature = layer.GetNextFeature()
    while feature:
        geometry = feature.GetGeometryRef()
        x = geometry.GetX()
        y = geometry.GetY()
        xValues.append(x)
        yValues.append(y)
        feature = layer.GetNextFeature()

    gdal.AllRegister()

    ds = gdal.Open(img, GA_ReadOnly)
    if ds is None:
        print('Could not open image')
        sys.exit(1)

    rows = ds.RasterYSize
    cols = ds.RasterXSize
    bands = ds.RasterCount

    transform = ds.GetGeoTransform()
    xOrigin = transform[0]
    yOrigin = transform[3]
    pixelWidth = transform[1]
    pixelHeight = transform[5]

    values = []
    for i in range(len(xValues)):
        x = xValues[i]
        y = yValues[i]

        xOffset = int((x - xOrigin) / pixelWidth)
        yOffset = int((y - yOrigin) / pixelHeight)

        s = str(int(x)) + ' ' + str(int(y)) + ' ' + str(xOffset) + ' ' + str(yOffset) + ' '

        dt = ds.ReadAsArray(xOffset, yOffset, 1, 1)
        values.append(dt.flatten())
    return values


if __name__ == "__main__":
    img_path = "E:/20200210/forest/gf2/dys_gf2.tif"  # 原始大图，在这上面选点
    img_path2 = "E:/20200210/forest/gf2/dys_gf2_test.tif"  # 测试小图，测试用
    shp_false = "E:/20200210/forest/point/1.shp"  # 负样本，丰富一点
    shp_true = "E:/20200210/forest/point/2.shp"  # 正样本，越多越好，不要和负样本混淆
    temp_path = "E:/20200210/forest/temp/"  # 存放临时文件

    point_false = getPixels(shp_false, img_path)
    num1 = len(point_false)
    lab_false = np.zeros((num1))

    point_true = getPixels(shp_true, img_path)
    num2 = len(point_true)
    lab_true = np.ones((num2))

    data = point_false + point_true
    label = list(lab_false) + list(lab_true)
    data = np.array(data)
    label = np.array(label)

    clf = RandomForestClassifier(n_estimators=100, max_depth=2, random_state=0)
    clf.fit(data, label)
    # print(clf.feature_importances_)

    im_proj2, im_geotrans2, im_width2, im_height2, im_data2 = read_img(img_path2)
    seg = np.zeros((im_data2.shape[1], im_data2.shape[2]))
    for i in xrange(im_width2 - 1):
        for j in xrange(im_height2 - 1):
            point = im_data2[0:4, j, i]
            point = np.expand_dims(point, 0)
            seg[j, i] = clf.predict(point)[0]

    seg = np.int8(seg)
    seg_path = os.path.join(temp_path, 'random.tif')
    write_img(seg_path, im_proj2, im_geotrans2, seg)