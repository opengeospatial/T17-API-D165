import rioxarray as rxr
import shapely.wkt
import shapely.geometry
from shapely.ops import transform
import rasterio.crs
from openapi_server.backend.dataquery_transformers.dataquery_transformer import DataQueryTransformer
import time
from flask import Response
from datetime import datetime
from dateutil.parser import parse
import pyproj

class NetCDFDataQueryTransformer(DataQueryTransformer):


    sel_tolerance = 10000000  # tolerance for position selection (nearest)
    destination_srs_number = 4326  # convert everything to WGS84
    destination_srs_epsg = "EPSG:4326"
    web_mercator_epsg = "EPSG:3857"
    datetime_format = "%Y-%m-%d%H %M:%S:%fZ"

    def __init__(self, netCDFConfig: dict):
        self.netCDFConfig = netCDFConfig

    def transformPositionQuery(self, collection_id, instance_id, coords, datetime=None):
        pos_geom = shapely.wkt.loads(coords)  # parse wkt
        print(pos_geom)

        # load data correctly
        da = self.readDataArrayFromNetCDF(collection_id, instance_id) #get netCDF as dataarray
        print(da)

        if datetime is not None:
            da = self.applyDatetimeFilter(da, datetime) #apply datetime filter first to reduce data

        #reproject to wgs84
        da_reproj = self.reprojectDataArrayToDestinationSrs(da)
        # get data at position (with tolerance)
        da_sel = da_reproj.sel(x=pos_geom.x, y=pos_geom.y,
                        method="nearest", tolerance=self.sel_tolerance)
        da_sel.rio.write_crs(input_crs = self.destination_srs_epsg, inplace = True)

        self.joinListAttributes(da_sel.attrs) #join list attributes in order to be compliant with netCDF3 (scipy engine only supports netCDF3)
        da_sel_netCDF = da_sel.to_netcdf(engine="scipy")  # convert from dataarray to netCDF

        print(da_sel)

        return Response(da_sel_netCDF,
                        mimetype="application/x-netcdf",
                        headers={"Content-Disposition":
                                 "attachment;filename=position_query_"+str(time.time())+".nc"})

    def transformRadiusQuery(self, collection_id, instance_id, within, within_units, radius_coords,  datetime=None):
        center_geom = shapely.wkt.loads(radius_coords)  # parse wkt
        print(center_geom)
        circle_geom = self.createCircle(center_geom, within, within_units) #buffer around center

        # load data correctly
        da = self.readDataArrayFromNetCDF(collection_id, instance_id)

        if datetime is not None:
            da = self.applyDatetimeFilter(da, datetime) #apply datetime filter first to reduce data

        #reproject to wgs84
        da_reproj = self.reprojectDataArrayToDestinationSrs(da)
        #clip to area
        da_clipped = da_reproj.rio.clip([circle_geom], from_disk=True)
        da_clipped.rio.write_crs(input_crs = self.destination_srs_epsg, inplace = True)

        self.joinListAttributes(da_clipped.attrs) #join list attributes in order to be compliant with netCDF3 (scipy engine only supports netCDF3)
        da_clipped_netCDF = da_clipped.to_netcdf(engine="scipy")  # convert from dataarray to netCDF

        return Response(da_clipped_netCDF,
                        mimetype="application/x-netcdf",
                        headers={"Content-Disposition":
                                 "attachment;filename=radius_query_"+str(time.time())+".nc"})

    def transformAreaQuery(self, collection_id, instance_id, coords, datetime=None):
        area_geom = shapely.wkt.loads(coords)  # parse wkt
        print(area_geom)

        # load data correctly
        da = self.readDataArrayFromNetCDF(collection_id, instance_id)

        if datetime is not None:
            da = self.applyDatetimeFilter(da, datetime) #apply datetime filter first to reduce data

        #reproject to wgs84
        da_reproj = self.reprojectDataArrayToDestinationSrs(da)
        #clip to area
        da_clipped = da_reproj.rio.clip([area_geom], from_disk=True)
        da_clipped.rio.write_crs(input_crs = self.destination_srs_epsg, inplace = True)

        self.joinListAttributes(da_clipped.attrs)   #join list attributes in order to be compliant with netCDF3 (scipy engine only supports netCDF3)
        da_clipped_netCDF = da_clipped.to_netcdf(engine="scipy")  # convert from dataarray to netCDF

        return Response(da_clipped_netCDF,
                        mimetype="application/x-netcdf",
                        headers={"Content-Disposition":
                                 "attachment;filename=area_query_"+str(time.time())+".nc"})

    def reprojectDataArrayToDestinationSrs(self, dataarray):
        dataarray_reproj = dataarray.rio.reproject(
            dst_crs=rasterio.crs.CRS.from_epsg(self.destination_srs_number))

        return dataarray_reproj

    def readDataArrayFromNetCDF(self, collectionId, instanceId):
        instConfig = self.getInstanceConfig(collectionId, instanceId)
        filePath = instConfig["filePath"]
        da = rxr.open_rasterio(filePath) #get netCDF as dataarray

        return da

    def applyDatetimeFilter(self, da, datetime):
        datetimeSplit = datetime.split(sep="/")  # can be datetime or interval

        if(len(datetimeSplit) == 1):  # datetime
            # no equals range filter in elasticsearch
            return da.loc[dict(time=self.formatDatetime(datetimeSplit[0]))]
        else:
            if datetimeSplit[0] == "..":  # earlier
                return da.loc[dict(time=slice(None, self.formatDatetime(datetimeSplit[1])))]
            elif datetimeSplit[1] == "..":  # later
                return da.loc[dict(time=slice(self.formatDatetime(datetimeSplit[0]), None))]
            else:  # between
                return da.loc[dict(time=slice(self.formatDatetime(datetimeSplit[0]), self.formatDatetime(datetimeSplit[1])))]


    def formatDatetime(self, datetime_str):
        out = datetime.isoformat(parse(datetime_str)) #get datetime in iso format
        return out

    def createCircle(self, center_wgs84, within, within_units):
        #transform center to metric, projected srs in order to handle metric radius correctly
        wgs84 = pyproj.CRS(self.destination_srs_epsg)
        webmercator = pyproj.CRS(self.web_mercator_epsg)

        project = pyproj.Transformer.from_crs(wgs84, webmercator, always_xy=True).transform
        center_metric = transform(project, center_wgs84)

        #create circle by buffering center coord
        if(within_units.upper() == "M"):
            circle_metric = center_metric.buffer(within)
        elif(within_units.upper() == "KM"):
            circle_metric = center_metric.buffer((within*1000))
        else:
            raise ValueError("unknown unit" + within_units + ", unit must be M or KM")

        #transform circle back to wgs84
        project_back = pyproj.Transformer.from_crs(webmercator, wgs84, always_xy=True).transform
        circle_wgs84 = transform(project_back, circle_metric)

        return circle_wgs84

    def joinListAttributes(self, attrs_dict):
        for key in attrs_dict:
            if isinstance(attrs_dict[key], list) or isinstance(attrs_dict[key], tuple):
                attrs_dict[key] = ','.join(str(i) for i in attrs_dict[key])

    def getCollectionConfig(self, collectionId):
        return self.netCDFConfig["collections"][collectionId]

    def getInstanceConfig(self, collectionId, instanceId):
        return self.getCollectionConfig(collectionId=collectionId)["instances"][instanceId]