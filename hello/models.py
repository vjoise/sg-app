# /*************************************************************************
#  *
#  * SEVA BUDDY CONFIDENTIAL
#  * __________________
#  *
#  *  [2015] - [2015] Seva Buddy Pte Ltd Incorporated
#  *  All Rights Reserved.
#  *
#  * NOTICE:  All information contained herein is, and remains
#  * the property of Seva Buddy Pte Ltd Incorporated and its suppliers,
#  * if any.  The intellectual and technical concepts contained
#  * herein are proprietary to Seva Buddy Pte Ltd Incorporated
#  * and its suppliers and may be covered by Singapore and Foreign Patents,
#  * patents in process, and are protected by trade secret or copyright law.
#  * Dissemination of this information or reproduction of this material
#  * is strictly forbidden unless prior written permission is obtained
#  * from Seva Buddy Pte Ltd Incorporated.
#  */
#  /*
# @(#)File:           $RCSfile: stderr.c,v $
# @(#)Version:        $Revision: 8.29 $
# @(#)Last changed:   $Date: 2008/06/02 13:00:00 $
# @(#)Purpose:        Error reporting routines
# @(#)Author:         abc
# @(#)Copyright:      (C) SB Pte Ltd 2015
# */


from google.appengine.ext import ndb
import datetime
from google.appengine.ext import db
from google.appengine.api import users

# Create your models here.
# Primary Table for Block Details based on Pincode
class Block_Table (db.Model) :
	Blk_PostalCode = db.IntegerProperty(required=True)
	Blk_Name = db.StringProperty()
	Blk_BuildingType = db.StringProperty()
	Blk_Description = db.StringProperty(required=True, multiline=True)
	Blk_GeoLocation = db.GeoPtProperty(required=True)
	Blk_Address = db.StringProperty(multiline=True)
	Blk_Phone = db.StringProperty()
	Blk_Email = db.StringProperty()
	Blk_Url = db.StringProperty()
	Blk_Image = db.BlobProperty()
	Blk_Levels = db.StringProperty()
	Blk_Map = db.BlobProperty()
	Blk_Size = db.StringProperty()


class Mall (db.Model) :
	pinCode = db.StringProperty(required=True)
	location = db.GeoPtProperty()
	address = db.StringProperty(multiline=True)
	contactInfo = db.StringProperty();
	blockType = db.StringProperty(multiline=True)
	category = db.StringProperty()
	#products = db.StructuredProperty(Product, repeated = True)

class Shop(db.Model):
	  name = db.StringProperty(required=True)
	  category = db.StringProperty(required=False)
	  imageUrl = db.StringProperty()
	  address = db.StringProperty(multiline=True)
	  location = db.GeoPtProperty()
	  #products = db.StructuredProperty()

class Product(db.Model):
	  name = db.StringProperty(required=True)
	  category = db.StringProperty(required=False)
	  price = db.FloatProperty()
	  address = db.StringProperty()
	  location = db.GeoPtProperty()

#Create a dummy instance now.
#e = Employee(name="John", role="manager")
#e.hire_date = datetime.datetime.now().date()
#e.put()
