# coding:utf-8

import logging
import datetime,time
import multiprocessing as mp
import gdal2tiles

def gdal_generate_tiles(input_file, output_dir, option):
    # 参数：
    # input_file （str）：输入文件的路径。
    # output_folder （str）：输出文件夹的路径。
    # options：图块生成选项。
    gdal2tiles.generate_tiles(input_file, output_dir, **option)


if __name__ == '__main__':
    # 日志
    LOG_FILE_NAME = "./info.log"
    logging.basicConfig(filename=LOG_FILE_NAME, level=logging.INFO)
    logging.basicConfig(filename=LOG_FILE_NAME, level=logging.ERROR)
    startTime = time.localtime(time.time())
    logging.info(time.strftime('%Y-%m-%d %H:%M:%S', startTime))

    # 计算核心数
    num_cores = int(mp.cpu_count())
    print("本地计算机有: " + str(num_cores) + " 核心")

    input_file = './Test/input/WH_BT_DEM_12_5.tif'
    # input_file = './Test/input/FuYangShi_Download_WGS84.shp'   #shp不支持
    output_file_dir = './Test/output/WH_BT_DEM_12_5'
    option = {
        'zoom': (10, 21),
        'resume': True,
        'verbose': True,
        'nb_processes': num_cores
    }
    gdal_generate_tiles(input_file, output_file_dir, option)