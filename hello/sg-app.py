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

def query(request):
    response = http.HttpResponse()
    response._headers['Content-Type'] = 'text/html'
    queryString = request.GET.__getitem__('queryString')
    index = search.Index(name="yesgShopIndex")
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

def refresh(request):
        response = http.HttpResponse()
        response._headers['Content-Type'] = 'text/json'
        response.write('YES G running!!')

        shopIndex = search.Index(name="yesgShopIndex")
        productIndex = search.Index(name="yesgProductIndex")
        mall = request.GET.__getitem__('mall');
        with open(mall+'/MallDirectory.csv', 'rU') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader :
                #print row
                if len(row) > 2 :
                    print row
                    entry = models.Shop(name=row[0], category=row[1], imageUrl=row[2], address=row[3])
                    shopDocument = search.Document(
                    # Setting the doc_id is optional. If omitted, the search service will create an identifier.
                    fields=[
                       search.TextField(name='name', value=row[0]),
                       search.TextField(name='category', value=row[1]),
                       search.TextField(name='address', value=row[3])
                       #search.GeoField(name='home_location', value=search.GeoPoint(37.619, -122.37))#z
                       ])
                    entry.put()
                    try:
                        shopIndex.put(shopDocument)
                    except search.Error:
                        print "error while indexing.."
        with open(mall+'/ProductListing.csv', 'rU') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader :
                if len(row) > 2 :
                    print row
                    entry = models.Product(name=row[0], category=row[1], imageUrl=row[2], price=row[3])
                    shopDocument = search.Document(
                    # Setting the doc_id is optional. If omitted, the search service will create an identifier.
                    fields=[
                       search.TextField(name='name', value=row[0]),
                       search.TextField(name='category', value=row[1]),
                       search.TextField(name='address', value=row[3])
                       #search.GeoField(name='home_location', value=search.GeoPoint(37.619, -122.37))#z
                       ])
                    entry.put()
                    try:
                        shopIndex.put(shopDocument)
                    except search.Error:
                        print "error while indexing.."
