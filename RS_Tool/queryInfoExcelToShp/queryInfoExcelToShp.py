# coding:utf-8

# 获取excel数据，匹配企业名称后更新shp数据中的整改类型
import sys
import xlrd
import arcpy
import time, datetime
import logging

defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)

# 基本地理位置
basePath = 'J:/ArcGIS_Data/sss/'

workbook = xlrd.open_workbook(basePath + 'ssssss.xls')
# 获取sheets1中的表格内容
sheet = workbook.sheet_by_index(0)
# 一共有多少行数据
nrows = sheet.nrows

rowValue = sheet.row_values(0)

# 获取表格中的所有数据后拼接成json格式
# {
#    'name':'企业名称',
#    'zglx':'整改类型值'
# }
info_table_sheet = []
# 获取第二行开始至最后一行数据
for i in range(1, nrows):
    row_list = sheet.row_values(i)
    row_name = row_list[0].encode('utf-8')
    row_zglx = row_list[1].encode('utf-8')
    info_table_sheet.append({
        'name': row_list[0],
        'zglx': row_list[1]
    })


LOG_FILE_NAME = "./event.log"
logging.basicConfig(filename=LOG_FILE_NAME, level=logging.INFO)
logging.basicConfig(filename=LOG_FILE_NAME, level=logging.ERROR)

# 创造工作空间
arcpy.env.workspace = basePath + "Geoodatabase.gdb"
startTime = time.localtime(time.time())
logging.info(time.strftime('%Y-%m-%d %H:%M:%S', startTime))

# 先进行空间坐标转换，对GPS数据---WGS To GCS2000
# arcpy.Project_management("polygon", "polygon2", "PROJCS['CGCS2000_3_Degree_GK_CM_117E',GEOGCS['GCS_China_Geodetic_Coordinate_System_2000',DATUM['D_China_2000',SPHEROID['CGCS2000',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Gauss_Kruger'],PARAMETER['False_Easting',500000.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',117.0],PARAMETER['Scale_Factor',1.0],PARAMETER['Latitude_Of_Origin',0.0],UNIT['Meter',1.0]]", "CGC2000_WGS84", "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]", "NO_PRESERVE_SHAPE", "", "NO_VERTICAL")
QYData = arcpy.MakeFeatureLayer_management("GPSData", "GPSData_layer")
QYData2 = r"J:\ArcGIS_Data\sss\qy.shp"

# 属性查询
def sattributQuery(obj):
    name = obj['name']
    zglx = obj['zglx']

    Time = time.localtime(time.time())
    logging.info("spaceQuery 开始!")

    split_name = name.split('铜陵')
    if len(split_name) > 1:
        query_name = name[2:12]
    else:
        query_name = name.split('有限公司')[0]

    try:
        # 循环进行数据查询，因为是按照图斑进行计算，所以需要进行每条polygon2数据进行查询
        # 先进行属性查询，获取单个图斑
        flayer_result_name = ''
        # query = '"QYMC LIKE " \'%' + query_name.encode('utf-8') + '%\''
        query = '"QYMC"  LIKE\'%' + query_name + '%\''
        print(query)
        arcpy.SelectLayerByAttribute_management(QYData, "NEW_SELECTION", query)
        cntAttribute = arcpy.GetCount_management(QYData)
        cursor_poygon = arcpy.SearchCursor(QYData)
        for row_d in cursor_poygon:
            flayer_result_name = row_d.qymc
            print('flayer_result_name', flayer_result_name)
        # 更新数据
        if (cntAttribute > 0):
            cursor = arcpy.da.UpdateCursor(QYData, ["OBJECTID_1","zglx"])
            print(cursor)
            logging.info(cursor)
            for row in cursor:
                row[1] = zglx
                cursor.updateRow(row)
                print "更新{}完成".format(row[0])
                logging.info("更新{}完成".format(row[1]))

        Time = time.localtime(time.time())
        logging.info(time.strftime('%Y-%m-%d %H:%M:%S', Time))

    except Exception, err:
        print "An error occurred during slection"
        print(err)
        logging.info(err)


for i in info_table_sheet:
    sattributQuery(i)

# sattributQuery(info_table_sheet[0])


Time = time.localtime(time.time())
logging.info(time.strftime('%Y-%m-%d %H:%M:%S', Time) + '全部完成！')
