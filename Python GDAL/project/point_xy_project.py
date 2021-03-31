from osgeo import gdal
from osgeo import osr
from osgeo import ogr

#输入为待操作shp的路径，和一组待转换的投影坐标
def prj2geo(path,x,y):
    # 为了支持中文路径，请添加下面这句代码
    gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "NO")
    # 为了使属性表字段支持中文，请添加下面这句
    gdal.SetConfigOption("SHAPE_ENCODING", "")
    # 注册所有的驱动
    ogr.RegisterAll()
    # 数据格式的驱动
    driver = ogr.GetDriverByName('ESRI Shapefile')
    ds = driver.Open(path);
    layer0 = ds.GetLayerByIndex(0);

    #或取到shp的投影坐标系信息
    prosrs = layer0.GetSpatialRef()
    geosrs = osr.SpatialReference()
    #设置输出坐标系为WGS84
    geosrs.SetWellKnownGeogCS("WGS84")

    ct = osr.CoordinateTransformation(prosrs, geosrs)
    coords = ct.TransformPoint(x, y)
    #输出为转换好的经纬度
    return coords[:2]