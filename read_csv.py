import csv
import datetime

def read_file():
    """
    docstring
    """

    file = open('inventory.csv')
    csv_reader = csv.reader(file)
    next(csv_reader)

    database_products = []
    temp_product = {
        'product_name':None,
        'product_qty': None,
        'product_price': None,
        'date_updated': None
    }

    for csv_line in csv_reader:
        for index, entry_info in enumerate(csv_line):
            if index == 0:
                temp_product['product_name'] = entry_info
            elif index == 1:
                temp_product['product_price'] = fix_price(entry_info)
            elif index == 2:
                temp_product['product_qty'] = entry_info
            elif index == 3:
                temp_product['date_updated'] = datetime.datetime.strptime(datetime.datetime.strptime(entry_info,"%m/%d/%Y").strftime('%Y-%m-%d %H:%M:%S'),'%Y-%m-%d %H:%M:%S')
        database_products.append(temp_product)
        temp_product = {}

    return database_products

def fix_price(price):
    try:
        fixed_price = float(price[1:])
        return int(fixed_price*100)
    except ValueError:
        print("Experience error converting price to cents")
    
    
    