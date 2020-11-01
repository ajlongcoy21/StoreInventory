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
    temp_product = {}

    for csv_line in csv_reader:
        for index, entry_info in enumerate(csv_line):
            if index == 0:
                temp_product['product_name'] = entry_info
            elif index == 1:
                temp_product['product_price'] = fix_price(entry_info)
            elif index == 2:
                temp_product['product_qty'] = entry_info
            elif index == 3:
                temp_product['date_updated'] = fix_date(entry_info)
        database_products.append(temp_product)
        temp_product = {}

    return database_products

def fix_price(entry_price):
    """
    docstring
    """
    try:
        fixed_price = float(entry_price[1:])
        return int(round(fixed_price*100))
    except ValueError:
        print("Experience error converting price to cents")
    
def fix_date(entry_date):
    """
    docstring
    """
    modified_date_format = datetime.datetime.strptime(entry_date,"%m/%d/%Y").strftime('%Y-%m-%d %H:%M:%S')
    return datetime.datetime.strptime(modified_date_format,'%Y-%m-%d %H:%M:%S')
    