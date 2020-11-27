#!/usr/bin/env python
# coding: utf-8
# Autor GaoSong
# 将矢量数据转换为栅格数据
import os
import tkinter
import tkinter.messagebox
import tkinter.filedialog
from osgeo import gdal
from osgeo import osr
from osgeo import ogr
from osgeo import gdalconst


class ARCVIEW_SHAPE:
    #------------------------------
    #read shape file
    #------------------------------
    def read_shp(self,file):
        #open
        ds = ogr.Open(file,False) #False - read only, True - read/write
        layer = ds.GetLayer(0)
        #layer = ds.GetLayerByName(file[:-4])
        #fields
        lydefn = layer.GetLayerDefn()
        spatialref = layer.GetSpatialRef()
        #spatialref.ExportToProj4()
        #spatialref.ExportToWkt()
        geomtype = lydefn.GetGeomType()
        fieldlist = []
        for i in range(lydefn.GetFieldCount()):
            fddefn = lydefn.GetFieldDefn(i)
            fddict = {'name':fddefn.GetName(),'type':fddefn.GetType(),
                      'width':fddefn.GetWidth(),'decimal':fddefn.GetPrecision()}
            fieldlist += [fddict]
        #records
        geomlist = []
        reclist = []
        feature = layer.GetNextFeature()
        while feature is not None:
            geom = feature.GetGeometryRef()
            geomlist += [geom.ExportToWkt()]
            rec = {}
            for fd in fieldlist:
                rec[fd['name']] = feature.GetField(fd['name'])
            reclist += [rec]
            feature = layer.GetNextFeature()
        #close
        ds.Destroy()
        return (spatialref,geomtype,geomlist,fieldlist,reclist)

    #------------------------------
    #write shape file
    #------------------------------
    def write_shp(self,file,data):
        gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8","YES")
        gdal.SetConfigOption("SHAPE_ENCODING","UTF-8")
        spatialref,geomtype,geomlist,fieldlist,reclist = data
        #create
        driver = ogr.GetDriverByName("ESRI Shapefile")
        if os.access(file, os.F_OK ):
            driver.DeleteDataSource(file)
        ds = driver.CreateDataSource(file)
        #spatialref = osr.SpatialReference( 'LOCAL_CS["arbitrary"]' )
        #spatialref = osr.SpatialReference().ImportFromProj4('+proj=tmerc ...')
        layer = ds.CreateLayer(file[:-4],srs=spatialref,geom_type=geomtype)
        # print type(layer)
        #fields
        for fd in fieldlist:
            field = ogr.FieldDefn(fd['name'],fd['type'])
            if fd.has_key('width'):
                field.SetWidth(fd['width'])
            if fd.has_key('decimal'):
                field.SetPrecision(fd['decimal'])
            layer.CreateField(field)
        #records
        for i in range(len(reclist)):
            geom = ogr.CreateGeometryFromWkt(geomlist[i])
            feat = ogr.Feature(layer.GetLayerDefn())
            feat.SetGeometry(geom)
            for fd in fieldlist:
                # print(fd['name'],reclist[i][fd['name']])
                feat.SetField(fd['name'],reclist[i][fd['name']])
            layer.CreateFeature(feat)
        #close
        ds.Destroy()

# templateTifFileName为模板影像，用于获取像素大小，区域范围，投影坐标

def img_to_vector(templateTifFileName, shpFileName, outputFileName):
    # ####读取矢量数据
    # test = ARCVIEW_SHAPE()
    # data3 = test.read_shp(shpFileName)
    # spatialref, geomtype, geomlist, fieldlist, reclist = data3
    # ####

    data = gdal.Open(templateTifFileName, gdalconst.GA_ReadOnly)
    geo_transform = data.GetGeoTransform()
    x_min = geo_transform[0]
    y_min = geo_transform[3]
    x_res = data.RasterXSize
    y_res = data.RasterYSize
    mb_v = ogr.Open(shpFileName)
    mb_l = mb_v.GetLayer()
    pixel_width = geo_transform[1]
    # pixel_width = float(entryPixsize)
    target_ds = gdal.GetDriverByName('GTiff').Create(outputFileName, x_res, y_res, 1, gdal.GDT_Byte)
    target_ds.SetGeoTransform((x_min, pixel_width, 0, y_min, 0, -1 * pixel_width))
    band = target_ds.GetRasterBand(1)
    NoData_value = -999
    band.SetNoDataValue(NoData_value)
    band.FlushCache()
    # options=["ATTRIBUTE=" + field]   可以定义栅格数据信息，掩模文件则不设置
    gdal.RasterizeLayer(target_ds, [1], mb_l, options=[])
    target_ds = None


def Start():
    shpFileName = entry_input_link.get()
    outputFileName = entry_output_link.get()
    templateTifFileName = entry_template_link.get()
    # templateTifFileName = 'D:/gaosong/Work_Demo/修改服务配置信息/DealTools/Image/base_img/fy_base.tiff'
    img_to_vector(templateTifFileName, shpFileName, outputFileName)


def fileInputSelect():
    file_path = tkinter.filedialog.askopenfilename(title=u'选择矢量文件', initialdir=(os.path.expanduser(default_dir)))
    input_text.set(file_path)


def fileTemplateSelect():
    file_path = tkinter.filedialog.askopenfilename(title=u'选择模板文件', initialdir=(os.path.expanduser(default_dir)))
    template_text.set(file_path)

def fileOutputSelect():
    file_path = tkinter.filedialog.asksaveasfilename(title=u'保存文件', initialdir=(os.path.expanduser(default_dir)))
    output_text.set(file_path)


if __name__ == '__main__':
    default_dir = r"J:/ArcGIS_Data/阜阳/shp"
    root = tkinter.Tk()
    root.title("矢量转栅格")
    root['width'] = 500
    root['height'] = 300

    input_text = tkinter.StringVar()
    input_text.set('')

    template_text = tkinter.StringVar()
    template_text.set('')

    output_text = tkinter.StringVar()
    output_text.set('')

    lab_input_link = tkinter.Label(root, text='矢量文件位置')
    lab_input_link.place(x=20, y=10, width=100, height=20)
    entry_input_link = tkinter.Entry(root, textvariable=input_text)
    entry_input_link.place(x=130, y=10, width=300, height=20)
    button_input_select = tkinter.Button(root, text="...", command=fileInputSelect)
    button_input_select.place(x=440, y=10, width=20, height=20)

    lab_template_link = tkinter.Label(root, text='模板文件位置')
    lab_template_link.place(x=20, y=40, width=100, height=20)
    entry_template_link = tkinter.Entry(root, textvariable=template_text)
    entry_template_link.place(x=130, y=40, width=300, height=20)
    button_template_select = tkinter.Button(root, text="...", command=fileTemplateSelect)
    button_template_select.place(x=440, y=40, width=20, height=20)

    lab_output_link = tkinter.Label(root, text='输出栅格文件位置')
    lab_output_link.place(x=20, y=70, width=100, height=20)
    entry_output_link = tkinter.Entry(root, textvariable=output_text)
    entry_output_link.place(x=130, y=70, width=300, height=20)
    button_output_select = tkinter.Button(root, text="...", command=fileOutputSelect)
    button_output_select.place(x=440, y=70, width=20, height=20)

    button_start = tkinter.Button(root, text="开始转换", command=Start)
    button_start.place(x=140, y=150, width=200, height=40)

    root.mainloop()
