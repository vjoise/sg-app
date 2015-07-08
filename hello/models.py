from google.appengine.ext import ndb
import datetime
from google.appengine.ext import db
from google.appengine.api import users

# Create your models here.

class Mall (db.Model) :
	pinCode = db.StringProperty(required=True)
	location = db.GeoPtProperty()
	address = db.StringProperty(multiline=True)
	contactInfo = db.StringProperty();
	blockType = db.StringProperty(multiline=True)
	category = db.StringProperty()
	products = db.StructuredProperty(Product, repeated = True)

class Shop(db.Model):
	  name = db.StringProperty(required=True)
	  category = db.StringProperty(required=False)
	  imageUrl = db.StringProperty()
	  address = db.StringProperty(multiline=True)
	  location = db.GeoPtProperty()
	  products = db.StructuredProperty()

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
