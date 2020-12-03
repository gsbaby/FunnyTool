# coding=utf-8
# 批量处理文件夹内的所有shp数据的坐标转换
import os
import arcpy
import sys

baseFile = 'F:/GaoSong/tansLatShp'
inputDirName = 'shp'
outputDirName = 'prj_Trans'


def transfrom(input_file, output_file):
    print('正在处理：', input_file)
    out_coordinate_system = arcpy.SpatialReference(4490)
    arcpy.Project_management(input_file, output_file, out_coordinate_system)
    print('输出文件：', output_file)


def oswalk(file_dir):
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            (filename, extension) = os.path.splitext(file)  # 将文件名拆分为文件名与后缀
            if (extension == '.shp'):
                path_filedir = '/'.join(root.split('\\'))
                path_array = path_filedir.split(inputDirName)
                output_file_name = path_array[0] + outputDirName + path_array[1].decode('gb2312')
                if not os.path.exists(output_file_name):
                    os.mkdir(output_file_name)
                output_file_shp = output_file_name + '/' + file
                input_file_shp = path_filedir.decode('gb2312') + '/' + file
                transfrom(input_file_shp, output_file_shp)


if __name__ == '__main__':
    oswalk(baseFile)
