# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# 2.py
# Created on: 2021-01-19 17:04:05.00000
#   (generated by GaoSong)
# Description:批量导出tif
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy


# Local variables:
# 此处为待处理影像
dats = ["G:\\阜阳\\Data\\Result\\数据组使用\\Raster\\3bands_321\\20190311_MASK_3bands.dat","G:\\阜阳\\Data\\Result\\数据组使用\\Raster\\3bands_321\\20190311_MASK_3bands.dat"]
go_info = dats.join(";")
# 此处为输出文件夹
v84_50 = "G:\\阜阳\\Data\\Result\\数据组使用\\Raster\\10M\\84_50"
v84_50__2_ = v84_50

# Process: Raster To Other Format (multiple)
arcpy.RasterToOtherFormat_conversion("G:\\阜阳\\Data\\Result\\数据组使用\\Raster\\3bands_321\\20190311_MASK_3bands.dat", v84_50, "TIFF")

