#!/usr/bin/python3
# coding = utf-8
# 通过EPSG获取GDAL中坐标参数
from osgeo import gdal, osr

srs = osr.SpatialReference()
srs.ImportFromEPSG(3857)
print(srs)

# strPrjLibFullPath = (r'./projd.dll')
# gdal.SetConfigOption("PROJSO",'./projd.dll')