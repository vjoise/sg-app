import csv
from google.appengine.ext import db
import hello.models
from google.appengine.api import search


PRODUCT_INDEX = "ProductIndex"
SHOP_INDEX = "ShopIndex"
BLOCKTABLE_INDEX = "BlockTableIndex"
def query(searchRequest):
    index = search.Index(name=BLOCKTABLE_INDEX)
    result=index.search(searchRequest)
    if not result.results:
        index = search.Index(name=SHOP_INDEX)
        result=index.search(searchRequest)
    return result

def insert(data):
    pass

def delete(data):
    pass

def findBy(type, key):
    pass


def readLocation(file):
    with open(file, 'rU') as csvfile:
        reader = csv.reader(csvfile)
        gp=None
        for row in reader :
            gp = db.GeoPt(float(row[0]), float(row[1]))
    return gp

def insertMall(self, mallName):
    shopIndex = search.Index(name=SHOP_INDEX)
    productIndex = search.Index(name=PRODUCT_INDEX)
    shopDocument = []
    mall = "data/" + mallName;
    index=1
    location = self.readLocation(mall + '/file.loc')
    tempMall = mallName
    with open(mall+'/MallDirectory.csv', 'rU') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader :
            #print row
            if len(row) > 2 :
                entry = hello.models.Shop(name=row[0], category=row[1], imageUrl=row[2], address=tempMall + " " +row[3], location = location)
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
                entry = hello.models.Product(name=row[0], category=row[1], price=float(row[2]), address = str(tempMall).replace("-", " ") , location = location)
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

def insertBlock(self):
    #Creating the Index Table
     BlockTableData = []
     index=1
     BlockTableIndex = search.Index(name=BLOCKTABLE_INDEX)
     with open('data/PostalCode/BlockTable.csv', 'rU') as csvfile:
         reader = csv.reader(csvfile)
         for row in reader :
            entry = hello.models.Block_Table(Blk_PostalCode=int(row[0]), Blk_Name=row[1], Blk_BuildingType=row[2], Blk_Description=row[3], Blk_GeoLocation = db.GeoPt(float(row[4]), float(row[5])), Blk_Address = row[6], Blk_Phone = row[7], Blk_Email = row[8], Blk_Url=row[9], Blk_Image=row[10], Blk_Levels=row[11], Blk_Map=row[12], Blk_Size=row[13])
            entry.put()
            BlockTableData.append(search.Document(
            fields=[
                search.TextField(name='Blk_PostalCode', value=row[0]),
                search.TextField(name='Blk_Name', value=row[1]),
                search.TextField(name='Blk_Address', value=row[5]),
                search.TextField(name='Blk_Phone', value=row[6]),
                search.TextField(name='Blk_Email', value=row[7]),
                ]))
            try:
                if index % 200 == 0:
                   print str(index)
                   BlockTableIndex.put(BlockTableData)
                   BlockTableData = []
            except search.Error:
                print "error while indexing.."
            index += 1

def insertBusRoute(self):
    pass

def insertRestuarants(self):
    pass