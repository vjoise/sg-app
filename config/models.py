#  *************************************************************************
#  *
#  * DisQour Pte Ltd, Singapore
#  * __________________
#  *
#  *  [2015] - [2015] DisQour Pte Ltd Incorporated
#  *  All Rights Reserved.
#  *
# @(#)File:           $models.py$
# @(#)Version:        $4.0$
# @(#)Last changed:   $Date: 2015/07/26 01:33:00 $
# @(#)Purpose:        Update of Header section
# @(#)Author:         Suneel N.G.
# @(#)Copyright:      (C) DisQour Pte Ltd 2015
# ----------------------------------------------------------------------------------------
# | Version Number   |  		User   			|    			Changes made 			|
# ----------------------------------------------------------------------------------------
# |                  |              			|                           			|
# ----------------------------------------------------------------------------------------
# | 2015/07/26, 4.0  | Suneel N. G.				| Update of Header section				|
# ----------------------------------------------------------------------------------------
# | 2015/07/26, 3.0  | Suneel N. G.				| Addition of Block_Table Model			|
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
