import webapp2
from google.appengine.ext.webapp.util import run_wsgi_app
import csv
from google.appengine.ext import db
import models
from google.appengine.api import search
from datetime import datetime
import json
from django.shortcuts import render_to_response
from django import http
import pickle

PRODUCT_INDEX = "yesgProductIndex"
SHOP_INDEX = "yesgShopIndex"

def query(request):
    response = http.HttpResponse()
    response._headers['Content-Type'] = 'text/html'
    queryString = request.GET.__getitem__('queryString')
    index = search.Index(name=PRODUCT_INDEX)
    result=index.search(queryString)
    if not result.results:
        index = search.Index(name=SHOP_INDEX)
        result=index.search(queryString)
    root = {};

    returnResult = [];
    for r in result.results :
        fields = []
        for s in r.fields :
                fields.append({'name' : s.name, 'value' : s.value});
        returnResult.append({'fields' : fields})
    root = {
        'data' : returnResult
    };
    data= json.dumps(root)
    return http.HttpResponse(data);


def readLocation(file):
    with open(file, 'rU') as csvfile:
        reader = csv.reader(csvfile)
        gp=None
        for row in reader :
            gp = db.GeoPt(float(row[0]), float(row[1]))
    return gp

def refresh(request):
        response = http.HttpResponse()
        response._headers['Content-Type'] = 'text/json'
        response.write('YES G running!!')

        shopIndex = search.Index(name=SHOP_INDEX)
        productIndex = search.Index(name=PRODUCT_INDEX)
        shopDocument = []
        mall = "data/" + request.GET.__getitem__('mall');
        index=1
        location = readLocation(mall + '/file.loc')
        tempMall = request.GET.__getitem__('mall')
        with open(mall+'/MallDirectory.csv', 'rU') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader :
                #print row
                if len(row) > 2 :
                    entry = models.Shop(name=row[0], category=row[1], imageUrl=row[2], address=tempMall + " " +row[3], location = location)
                    shopDocument.append(search.Document(
                    fields=[
                       search.TextField(name='name', value=row[0]),
                       search.TextField(name='category', value=row[1]),
                       search.TextField(name='address', value=entry.address),
                       search.GeoField(name='location', value=search.GeoPoint(location.lat, location.lon))#z
                       ]))
                    entry.put()
                    try:
                        if index % 200 == 0:
                            shopIndex.put(shopDocument)
                            shopDocument = []
                    except search.Error:
                        print "error while indexing.."
                index += 1
        index = 0
        productDocument = []
        file = open(mall+'/ProductListing.csv')
        with open(mall+'/ProductListing.csv', 'rU') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader :
                if len(row) > 2 :
                    entry = models.Product(name=row[0], category=row[1], price=float(row[2]), address = str(tempMall).replace("-", " ") , location = location)
                    productDocument = search.Document(
                    fields=[
                       search.TextField(name='name', value=row[0]),
                       search.TextField(name='category', value=row[1]),
                       search.TextField(name='address', value=entry.address),
                       search.GeoField(name='location', value=search.GeoPoint(location.lat, location.lon))#z
                       ])
                    entry.put()
                    try:
                        if index % 200 == 0:
                            productIndex.put(productDocument)
                            productDocument = []
                    except search.Error:
                        print "error while indexing.."
                index += 1
        return http.HttpResponse();

def refreshRoute(request):
     r = [];
     with open('data/route2.csv', 'rU') as csvfile:
         reader = csv.reader(csvfile)
         for row in reader :
            r.append({'lat': row[0], 'long' : row[1]});
     root = {
        'data' : r
     };
     data= json.dumps(root)
     return http.HttpResponse(data);

def searchByDistance(user_location):

    index = search.Index(PRODUCT_INDEX)

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