from collections import OrderedDict
import datetime
import os
import sys

import product
import read_csv


# Create your Dunder Main statement.

def main():
    product.initialize()
    products_from_csv = read_csv.read_file()
    print(products_from_csv)
    for product_to_add in products_from_csv:
        product.add_product(product_to_add)

if __name__ == '__main__':
    main()