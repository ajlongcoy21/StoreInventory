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

def create_csv_backup(headers, products):
    """
    creates a backup of the products to a csv file
    """

    with open('backup.csv', 'w', newline='') as csvfile:

        backupwriter = csv.writer(csvfile, delimiter=',')
        header_array = []

        for each_header in headers:
            header_array.append(each_header.name)

        backupwriter.writerow(header_array)
        
        for each_product in products:
            backupwriter.writerow([each_product.product_id, each_product.product_name, each_product.product_price, each_product.product_qty, each_product.date_updated])

def fix_price(entry_price):
    """
    fix the price of the item to be an intenger in cents
    """
    try:
        fixed_price = float(entry_price[1:])
        return int(round(fixed_price*100))
    except ValueError:
        print("Experience error converting price to cents")
    
def fix_date(entry_date):
    """
    fix the date to be able to loaded into the database
    """
    modified_date_format = datetime.datetime.strptime(entry_date,"%m/%d/%Y").strftime('%Y-%m-%d %H:%M:%S')
    return datetime.datetime.strptime(modified_date_format,'%Y-%m-%d %H:%M:%S')
    