from openapi_server.backend.query_transformers.query_transformer import QueryTransformer
from urllib.parse import urlencode, quote

datetimeEqual_template = "\"<Filter><PropertyIsEqualTo><PropertyName>{temporalProperty}</PropertyName><Literal>{datetime}</Literal></PropertyIsEqualTo><Filter>\""

datetimeLater_template = """
\"<ogc:Filter>
  <ogc:PropertyIsGreaterThanOrEqualTo>
    <ogc:PropertyName>{temporalProperty}</ogc:PropertyName>
    <ogc:Function name="dateParse"><ogc:Literal>{datetime}</ogc:Literal></ogc:Function>
  </ogc:PropertyIsGreaterThanOrEqualTo></ogc:Filter>\""""

datetimeEarlier_template = """
\"<ogc:Filter>
  <ogc:PropertyIsLessThanOrEqualTo>
    <ogc:PropertyName>{temporalProperty}</ogc:PropertyName>
    <ogc:Function name="dateParse"><ogc:Literal>{datetime}</ogc:Literal></ogc:Function>
  </ogc:PropertyIsLessThanOrEqualTo></ogc:Filter>\"
"""
datetimeBetween_template = "\"<ogc:Filter><ogc:PropertyIsBetween><ogc:PropertyName>{temporalProperty}</ogc:PropertyName><ogc:Function name=\"dateParse\"><ogc:LowerBoundary>{lower}</ogc:LowerBoundary></ogc:Function><ogc:Function name=\"dateParse\"><ogc:UpperBoundary>{upper}</ogc:UpperBoundary></ogc:Function></ogc:PropertyIsBetween></ogc:Filter>\""

class WFSQueryTransformer(QueryTransformer):

    def transformLimit(self, limit: "int"):
        return {"count": str(limit)}

    def transformBBox(self, bbox: "list[int]"):
        return {"bbox": "{0},{1},{2},{3}".format(bbox[0], bbox[1], bbox[2], bbox[3])}

    def transformID(self, identifier: "str"):
        return {"featureID": identifier}

    def transformDateTime(self, datetime: "str", temporalProperty: str):
        filter = {"filter": None}
        datetimeSplit = datetime.split(sep= "/") #can be datetime or interval

        if(len(datetimeSplit) == 1): #datetime
            filter["filter"] = datetimeEqual_template.format(temporalProperty = temporalProperty, datetime = datetimeSplit[0])
        else:
            if datetimeSplit[0] == "..": #earlier
                filter["filter"] = datetimeEarlier_template.format(temporalProperty = temporalProperty, datetime = datetimeSplit[1])
            elif datetimeSplit[1] == "..": #later
                filter["filter"] = datetimeLater_template.format(temporalProperty = temporalProperty, datetime = datetimeSplit[0])
            else: #between
                filter["filter"] = datetimeBetween_template.format(temporalProperty = temporalProperty, lower = datetimeSplit[0], upper = datetimeSplit[1])                       

        filter["filter"] = filter["filter"].replace('\r', '').replace('\n', '') #remove linebrakes
        return filter