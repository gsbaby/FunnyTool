# -*- coding: utf-8 -*-
# @Author  : GaoSong
# @Time    : 2021/3/30 0030 上午 11:13
# @Function:

import os
from osgeo import gdal, gdalnumeric, gdal_array
import random


# dataset = gdal.Open(fileName)
# if dataset == None:
#     print(fileName + "文件无法打开")
#     return
# im_width = dataset.RasterXSize  # 栅格矩阵的列数
# im_height = dataset.RasterYSize  # 栅格矩阵的行数
# im_bands = dataset.RasterCount  # 波段数
# im_data = dataset.ReadAsArray(0, 0, im_width, im_height)  # 获取数据
# im_geotrans = dataset.GetGeoTransform()  # 获取仿射矩阵信息
# im_proj = dataset.GetProjection()  # 获取投影信息
# im_blueBand = im_data[0, 0:im_height, 0:im_width]  # 获取蓝波段
# im_greenBand = im_data[1, 0:im_height, 0:im_width]  # 获取绿波段
# im_redBand = im_data[2, 0:im_height, 0:im_width]  # 获取红波段
# im_nirBand = im_data[3, 0:im_height, 0:im_width]  # 获取近红外波段

def clip(in_ds, file_img, i, in_ds2, background_value, block_xsize, block_ysize):
    im_width = in_ds.RasterXSize  # 栅格矩阵的列数
    im_height = in_ds.RasterYSize  # 栅格矩阵的行数
    im_bands = in_ds.RasterCount  # 波段数
    # im_data = in_ds.ReadAsArray(0, 0, im_width, im_height)  # 获取数据
    im_geotrans = in_ds.GetGeoTransform()  # 获取仿射矩阵信息
    im_proj = in_ds.GetProjection()  # 获取投影信息

    singlefileForm = os.path.splitext(file_img)[0]
    # 读取原图中的每个波段
    in_bands = []
    for j in range(0, im_bands):
        in_band = in_ds.GetRasterBand(j + 1)
        in_bands.append(in_band)
    # 读取相对应的单波段中（标注）信息
    in_bands1 = in_ds2.GetRasterBand(1)

    # 定义切图的大小（矩形框）
    block_xsize = block_xsize  # 行
    block_ysize = block_ysize  # 列

    # 定义切图的起始点坐标(相比原点的横坐标和纵坐标偏移量)
    offset_x = random.randint(0, im_width)  # 这里是随便选取的，可根据自己的实际需要设置
    offset_y = random.randint(0, im_height)

    # 判断是否超出范围了，超出范围的话就重新定义起始坐标点位
    if offset_x + block_xsize > im_width:
        offset_x = im_width - block_xsize
    if offset_y + block_ysize > im_height:
        offset_y = im_height - block_ysize

    # 从每个波段中切需要的矩形框内的数据(注意读取的矩形框不能超过原图大小)
    out_bands = []
    for j in range(0, im_bands):
        out_band = in_bands[j].ReadAsArray(offset_x, offset_y, block_xsize, block_ysize)
        out_bands.append(out_band)

    ######################校验波段中是否全部为背景值##############################
    max = out_bands[0].max()
    if max == background_value:
        print('当前所裁剪区域为全背景，即为无效区域')
        i = i - 1
        return i

    # 同样，读取单波段中的信息
    out_bands1 = in_bands1.ReadAsArray(offset_x, offset_y, block_xsize, block_ysize)

    # 获取Tif的驱动，为创建切出来的图文件做准备
    gtif_driver = gdal.GetDriverByName("GTiff")

    # 创建切出来的要存的文件（im_bands波段数量，最后一个参数为数据类型，跟原文件一致）
    clip_file_name = singlefileForm + '_clip'
    if not os.path.exists(clip_file_name):
        os.mkdir(clip_file_name)
    #     dataset = driver.Create(path, im_width, im_height, im_bands, datatype)
    out_ds = gtif_driver.Create(clip_file_name + "\\clip_" + str(i) + '.tif', block_xsize, block_ysize, im_bands,
                                in_bands[0].DataType)

    # label标签
    clip_file_label = singlefileForm + '_label'
    if not os.path.exists(clip_file_label):
        os.mkdir(clip_file_label)
    out_ds_single = gtif_driver.Create(clip_file_label + "\\clip_" + str(i) + '.tif', block_xsize, block_ysize, 1,
                                       in_bands1.DataType)

    print("成功创建tif")

    # 获取原图的原点坐标信息
    ori_transform = in_ds.GetGeoTransform()
    if ori_transform:
        print(ori_transform)
        print("原点位置 = ({}, {})".format(ori_transform[0], ori_transform[3]))
        print("像素大小（分辨率） = ({}, {})".format(ori_transform[1], ori_transform[5]))

    # 读取原图仿射变换参数值
    top_left_x = ori_transform[0]  # 左上角x坐标
    w_e_pixel_resolution = ori_transform[1]  # 东西方向像素分辨率
    top_left_y = ori_transform[3]  # 左上角y坐标
    n_s_pixel_resolution = ori_transform[5]  # 南北方向像素分辨率

    # 根据反射变换参数计算新图的原点坐标
    top_left_x = top_left_x + offset_x * w_e_pixel_resolution
    top_left_y = top_left_y + offset_y * n_s_pixel_resolution

    # 将计算后的值组装为一个元组，以方便设置
    dst_transform = (top_left_x, ori_transform[1], ori_transform[2], top_left_y, ori_transform[4], ori_transform[5])

    # 设置裁剪出来图的原点坐标
    out_ds.SetGeoTransform(dst_transform)
    out_ds_single.SetGeoTransform(dst_transform)

    # 设置SRS属性（投影信息）
    out_ds.SetProjection(in_ds.GetProjection())
    out_ds_single.SetProjection(in_ds2.GetProjection())

    # 写入目标文件
    for j in range(im_bands):
        out_ds.GetRasterBand(j + 1).WriteArray(out_bands[j])

    out_ds_single.GetRasterBand(1).WriteArray(out_bands1)

    # 将缓存写入磁盘
    out_ds.FlushCache()
    out_ds_single.FlushCache()
    print("写入磁盘成功")

    # 计算统计值
    # for i in range(1, 3):
    #     out_ds.GetRasterBand(i).ComputeStatistics(False)
    # print("ComputeStatistics succeed")
    del out_ds
    del out_ds_single
    return i


if __name__ == '__main__':
    # 裁剪行列的像素个值
    block_xsize = 400  # 行
    block_ysize = 400  # 列
    # 背景值
    background_value = 0
    # 读取要切的原图
    file_img = "E:\\2017\\2021_03_30\\20200426.dat"
    # 分类结果数据
    class_img = "E:\\2017\\2021_03_30\\2020_class3.dat"
    # 裁剪循环次数
    clip_times = 100
    # *******************以上为数据变量****************************
    in_ds = gdal.Open(file_img)
    in_ds2 = gdal.Open(class_img)
    if in_ds == None:
        print(file_img + "文件无法打开")
    elif in_ds2 == None:
        print(class_img + "文件无法打开")
    else:
        print("影像打开成功")
        i = 1
        while i <= clip_times:
            print('clip前的i值：', i)
            i = clip(in_ds, file_img, i, in_ds2, background_value, block_xsize, block_ysize)
            print('clip后的i值：', i)
            i += 1
    print("结束！")