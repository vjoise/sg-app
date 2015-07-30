#  *************************************************************************
#  *
#  * DisQour Pte Ltd, Singapore
#  * __________________
#  *
#  *  [2015] - [2015] DisQour Pte Ltd Incorporated
#  *  All Rights Reserved.
#  *
# @(#)File:           busdata.py$
# @(#)Version:        $1.0$
# @(#)Last changed:   $Date: 2015/07/27 21:30:00 $
# @(#)Purpose:        Initial revision
# @(#)Author:         Suneel N.G.
# @(#)Copyright:      (C) DisQour Pte Ltd 2015
# ----------------------------------------------------------------------------------------
# | Version Number   |  		User   			|    			Changes made 			|
# ----------------------------------------------------------------------------------------
# |                  |              			|                           			|
# ----------------------------------------------------------------------------------------
# | 2015/07/27, 1.0  | Suneel N. G.				| Initial Revision, 			        |
# |                  |              			| The file include related functions to |
# |                  |              			| add and retrieve bus data to the database.|
# ----------------------------------------------------------------------------------------
#  * DisQour Pte Ltd CONFIDENTIAL
#  * NOTICE:  All information contained herein is, and remains
#  * the property of DisQour Pte Ltd Incorporated and its suppliers,
#  * if any.  The intellectual and technical concepts contained
#  * herein are proprietary to DisQour Pte Ltd Incorporated
#  * and its suppliers and may be covered by Singapore and Foreign Patents,
#  * patents in process, and are protected by trade secret or copyright law.
#  * Dissemination of this information or reproduction of this material
#  * is strictly forbidden unless prior written permission is obtained
#  * from DisQour Pte Ltd Incorporated.
# ----------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------#
#Import defintions
#-----------------------------------------------------------------------------------------#

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
from google.appengine.ext import ndb



#-----------------------------------------------------------------------------------------#
#Symbol definitions
#-----------------------------------------------------------------------------------------#
BUSSTOPTABLE_INDEX = "BusstopTableIndex"


#-----------------------------------------------------------------------------------------#
# Routine Definitions
#-----------------------------------------------------------------------------------------#

# Bus Stop Update
# The routine "busstoptableupdate" is responsible to update the bus stop information to the
# database reading from the csv file from location "/data/BusData". This contains bus stop
# number, bus stop name and bus stop geo location.

def busstoptableupdate(request):
    #Variables Definition
    response = http.HttpResponse()
    BusStopTableData = []
    index=1
    bus_row_index = 0
    response.write('Database(Busstop_Table) Update in Progress...')

    #Creating the Index Table
    BusstopTableIndex = search.Index(name=BUSSTOPTABLE_INDEX)
    with open('data/BusData/busstopdata.csv', 'rU') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader :
            if bus_row_index > 0 :
                entry = models.Busstop_Table(Bst_Number=row[0], Bst_Name=row[3], Bst_Position = db.GeoPt(float(row[1]), float(row[2])))
                entry.put()
                BusStopTableData.append(search.Document(
                fields=[
                    search.TextField(name='Bst_Number', value=row[0]),
                    search.TextField(name='Bst_Name', value=row[3]),
                    ]))
                try:
                    if index % 200 == 0 :
                       print str(index)
                       BusstopTableIndex.put(BusStopTableData)
                       BusStopTableData = []
                except search.Error:
                    print "error while indexing.."
                index += 1
            bus_row_index += 1
        BusstopTableIndex.put(BusStopTableData)
        print str(bus_row_index)
    return http.HttpResponse();

# Bus Route Update
# The routine "busroutetableupdate" is responsible to update the bus stop information to the
# database reading from the json file from location "/data/BusData". This contains bus stop
# number, bus stop name and bus stop geo location.

def busroutetableupdate(request):
    #Variables Definition
    response = http.HttpResponse()
    busroutetabledata = []
    index=1
    row_index = 0
    route_items = 0
    response.write('Database(Busroute_Table) Update in Progress...')

    with open('data/BusData/1N.json', 'rU') as data_file:
        json_data = json.load(data_file)
        entry = models.Busroute_Table(Brt_Serviceno = '1N')
        route_items = len(json_data['1']['route'])
        if route_items > 0:
            #Route direction 1 is available
            for row_index in range(0,(route_items-1),1):
                geo = json_data['1']['route'][row_index]
                entry.Brt_Serviceroute1.append(ndb.GeoPt(float(geo.split(',')[0]), float(geo.split(',')[1])))
                entry.put()
                print str(row_index)
        row_index = 0
        route_items = len(json_data['2']['route'])
        if route_items > 0:
            #Route direction 1 is available
            for row_index in range(0,(route_items-1),1):
                entry.Brt_Serviceroute2 = json_data['2']['route'][row_index]
                entry.put()
        # for row in reader :
        #     if bus_row_index > 0 :
        #         entry = models.Busstop_Table(Bst_Number=row[0], Bst_Name=row[3], Bst_Position = db.GeoPt(float(row[1]), float(row[2])))
        #         entry.put()
        #         BusStopTableData.append(search.Document(
        #         fields=[
        #             search.TextField(name='Bst_Number', value=row[0]),
        #             search.TextField(name='Bst_Name', value=row[3]),
        #             ]))
        #         try:
        #             if index % 200 == 0 :
        #                print str(index)
        #                BusstopTableIndex.put(BusStopTableData)
        #                BusStopTableData = []
        #         except search.Error:
        #             print "error while indexing.."
        #         index += 1
        #     bus_row_index += 1
        # BusstopTableIndex.put(BusStopTableData)
        print json_data['1']['route'][0]
        print len(json_data)
        print len(json_data(0))
    return http.HttpResponse();
