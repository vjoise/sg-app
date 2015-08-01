import csv
from google.appengine.ext import db
import hello.models
from google.appengine.api import search
import json
from django import http
from hello.com.disqour.data import DataStore as dataStore

def query(request):
    response = http.HttpResponse()
    response._headers['Content-Type'] = 'text/html'
    queryString = request.GET.__getitem__('queryString')
    result = dataStore.query(queryString)
    root = {};
    returnResult = [];
    for r in result.results :
        fields = []
        for s in r.fields :
            value = s.value
            if type(s.value) is search.GeoPoint :
                 value = s.value.latitude + "," + s.value.longitude
            fields.append({'name' : s.name, 'value' : value});
        returnResult.append({'fields' : fields})
    root = {
        'data' : returnResult
    };
    data= json.dumps(root)
    return http.HttpResponse(data);

def refresh(request):
        response = http.HttpResponse()
        response._headers['Content-Type'] = 'text/json'
        response.write('YES G running!!')
        dataStore.insertMall(request.GET.__getitem__("mall"))
        return http.HttpResponse();

def blocktableupdate(request):
    #Variables Definition
     response = http.HttpResponse()
     response.write('Database Update in Progress...')
     dataStore.insertBlock()
     return http.HttpResponse();

def searchByDistance(user_location):

    index = search.Index("Distance-Index")

    #user_location = (-33.857, 151.215)
    query = "distance(location, geopoint(%f, %f)) < %f" % (
        user_location[0], user_location[1], 5000)

    loc_expr = "distance(location, geopoint(%f, %f))" % (
        user_location[0], user_location[1])

    sortexpr = search.SortExpression(
        expression=loc_expr,
        direction=search.SortExpression.ASCENDING, default_value=5001)

    search_query = search.Query(
        query_string=query,
        options=search.QueryOptions(
            sort_options=search.SortOptions(expressions=[sortexpr])))

    results = index.search(search_query)

    return results