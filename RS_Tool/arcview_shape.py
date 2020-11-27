#!/usr/bin/env python
# coding: utf-8
# Autor GaoSong
# 读取shp数据

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


if __name__ == '__name__':
    activeShp = ARCVIEW_SHAPE()
    activeShp.read_shp()