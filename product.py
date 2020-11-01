import datetime

from peewee import *

# Define Product

db = SqliteDatabase('inventory.db')

# Define Product

class Product(Model):
    product_id = PrimaryKeyField()
    product_name = CharField(max_length=255, unique=True)
    product_qty = IntegerField(default=0)
    product_price = IntegerField(default=0)
    date_updated = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db

def initialize():
    """ create the database and the table if they dont exist """

    # Connect to the database and create table if they are not created yet

    db.connect()
    db.create_tables([Product], safe=True)

def add_product(inventory_product):
    """ 
    Takes a product and tries to add it to the database. When entering products into the database, if a 
    duplicate product name is found, the app will check to see which product entry was most recently updated 
    and only save that data.
    """

    # Try to add product to the database
    
    try:
        Product.create(product_name=inventory_product['product_name'],product_qty=inventory_product['product_qty'],product_price=inventory_product['product_price'],date_updated=inventory_product['date_updated'])
    except IntegrityError:

        # If integrityError occurs, get the product from database and compare which information is newer. 
        # If the new product is more up to date than the database, then update the database with new information

        product_get = Product.select().where(Product.product_name == inventory_product['product_name'])
        if product_get[0].date_updated < inventory_product['date_updated']:
            Product.update(product_qty=inventory_product['product_qty'],product_price=inventory_product['product_price'],date_updated=inventory_product['date_updated']).where(Product.product_name == inventory_product['product_name']).execute()

def view_product(product_id):
    """
    View product takes a product_id from the user (must be > 0) and querys the database for that product_id. If they query
    returns no results, then a message is displayed to help the user know what is the range for the product_ids.
    """

    # Query database for the product_id
    product_get = Product.select().where(Product.product_id == product_id)
    
    # If we get a product, display the information in a readable format
    # Else display message giving the user the range of valid inputs
    if product_get:
        print("\n" + "*"*100)
        print("        Product Name: {}".format(product_get[0].product_name))
        print("       Product Price: ${}".format(float(product_get[0].product_price)/100))
        print("    Product Quantity: {}".format(product_get[0].product_qty))
        print("Product Last Updated: {}".format(product_get[0].date_updated.strftime('%m-%d-%Y')))
        print("*"*100 + "\n")
    else:
        product_get = Product.select()
        print("Sorry that selection is not valid. Please try a number within range 1 - {}.".format(len(product_get)))