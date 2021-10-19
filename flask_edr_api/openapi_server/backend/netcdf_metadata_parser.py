import rioxarray as rxr
from shapely.geometry import box
from openapi_server.models.extent_spatial import ExtentSpatial
from openapi_server.models.extent_temporal import ExtentTemporal
import pyproj
from shapely.ops import transform
from dateutil.parser import parse

class NetCDFMetadataParser:

    def __init__(self, dataarray):
        self.da = dataarray
        self.wgs84_epsg = "EPSG:4326"


    def getSpatialExtent(self):
        bbox = self.da.rio.bounds();
        bbox_shapely = box(bbox[0], bbox[1], bbox[2], bbox[3])    
        bbox_wgs84 = self.transformBBoxToWGS84(bbox_shapely)

        return ExtentSpatial(bbox=[[bbox_wgs84[0],bbox_wgs84[1]],[bbox_wgs84[2], bbox_wgs84[3]]])

    def getTemporalExtent(self):
        min = self.da.idxmin("time")
        max = self.da.idxmax("time")

        print(min)

    def transformBBoxToWGS84(self, bbox_shapely):
        wgs84 = pyproj.CRS(self.wgs84_epsg)
        originSRS = pyproj.CRS(self.da.rio.crs.to_epsg())

        project = pyproj.Transformer.from_crs(originSRS, wgs84, always_xy=True).transform
        bbox_wgs84_shapely = transform(project, bbox_shapely)

        return bbox_wgs84_shapely.bounds