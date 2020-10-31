import datetime

from peewee import *

db = SqliteDatabase('inventory.db')

class Product(Model):
    product_id = PrimaryKeyField()
    product_name = CharField(max_length=255, unique=True)
    product_qty = IntegerField(default=0)
    product_price = IntegerField(default=0)
    date_updated = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db

def initialize():
    """ create the database and the table if they dont exist"""

    db.connect()
    db.create_tables([Product], safe=True)

def add_product(inventory_product):
    """
    docstring
    """
    try:
        Product.create(product_name=inventory_product['product_name'],product_qty=inventory_product['product_qty'],product_price=inventory_product['product_price'],date_updated=inventory_product['date_updated'])
    except IntegrityError:
        test_product_get = Product.select().where(Product.product_name == inventory_product['product_name'])
        if test_product_get[0].date_updated < inventory_product['date_updated']:
            Product.update(product_qty=inventory_product['product_qty'],product_price=inventory_product['product_price'],date_updated=inventory_product['date_updated']).where(Product.product_name == inventory_product['product_name']).execute()

