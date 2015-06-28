from google.appengine.ext import ndb
import datetime
from google.appengine.ext import db
from google.appengine.api import users

# Create your models here.

class Shop(db.Model):
	  name = db.StringProperty(required=True)
	  category = db.StringProperty(required=False)
	  imageUrl = db.StringProperty()
	  address = db.StringProperty(multiline=True)

class Product(db.Model):
	  name = db.StringProperty(required=True)
	  category = db.StringProperty(required=False)
	  imageUrl = db.StringProperty()
	  price = db.IntegerProperty()
	  shop = db.StringProperty(required=True)

#Create a dummy instance now.
#e = Employee(name="John", role="manager")
#e.hire_date = datetime.datetime.now().date()
#e.put()
