from openapi_server.backend.query_transformers.query_transformer import QueryTransformer

# default schema mapping of elasticsearch create keyword field for exact match (datatype keyword)
ID_ATTRIBUTE = 'id.keyword'
GEOM_ATTRIBUTE = 'geometry'


class ElasticsearchQueryTransformer(QueryTransformer):
    """
    transforms API - Features getItems queries into Elasticsearch DSL
    """

    def transformLimit(self, limit: "int"):
        return {"from": 0, "size": limit}

    def transformBBox(self, bbox: "list[int]"):
        print(bbox)
        bboxFilter = {
            "geo_shape": {
                GEOM_ATTRIBUTE: {
                    "shape": {
                        "type": "envelope",
                        # [[minLon, maxLat], [maxLon, minLat]]
                        "coordinates": [[bbox[1], bbox[2]], [bbox[3], bbox[0]]]
                    },
                    "relation": "INTERSECTS"
                }
            }
        }

        return bboxFilter

    def transformID(self, identifier: "str"):
        idFilter = {"term":  {ID_ATTRIBUTE: identifier}}
        return idFilter

    def transformDateTime(self, datetime: "str", temporalProperty: str):
        dtFilter = None
        datetimeSplit = datetime.split(sep="/")  # can be datetime or interval

        if(len(datetimeSplit) == 1):  # datetime
            # no equals range filter in elasticsearch
            dtFilter = {"range": {temporalProperty: {
                "gte": datetimeSplit[0], "lte":  datetimeSplit[0]}}}
        else:
            if datetimeSplit[0] == "..":  # earlier
                dtFilter = {"bool": {"must_not": [{"range": {temporalProperty: {
                    "gt":  datetimeSplit[1]}}}]}}
            elif datetimeSplit[1] == "..":  # later
                dtFilter = {"bool": {"must_not": [{"range": {temporalProperty: {
                    "lt":  datetimeSplit[0]}}}]}}
            else:  # between
                dtFilter = {"bool": {"must_not": [{"range": {temporalProperty: {
                    "lt":  datetimeSplit[0]}}}, {"range": {temporalProperty: {
                        "gt":  datetimeSplit[1]}}}]}}
                        
        return dtFilter
