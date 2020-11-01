from collections import OrderedDict
import datetime
import os
import sys
import re

import product
import csv_control

regex_money_input = re.compile('^\$(?!0,?\d)([0-9]{1}[0-9]{0,}(\.[0-9]{2}))')
regex_date_input = re.compile('^(0?[1-9]|1[012])/([012][0-9]|[1-9]|3[01])/([12][0-9]{3})$')

def main():
    # Initialize product database
    product.initialize()

    # Obtain the products from the csv as a list of dictionaries
    products_from_csv = csv_control.read_file()

    # Loop through the list and add each product to the database
    for product_to_add in products_from_csv:
        product.add_product(product_to_add)

    # Start the menu loop for the user to interface with the database information
    menu_loop()

def clear():
    """
    clears the terminal for the user at convenient times to make the content displayed easier to read
    """

    # Clear terminal screen
    os.system('cls' if os.name == 'nt' else 'clear')

def menu_loop():
    """
    show the menu
    """

    # Initialize choice
    choice = None

    # While the user does not select to quit the application
    while choice != 'q':

        # clear the screen and display the menu
        clear()
        print("Enter 'q' to quit.")
        for key, value in menu.items():
            print('{}) {}'.format(key,value.__doc__))

        # ask for the menu choice from the user
        choice = input('Action: ').lower().strip()

        # if the choice is in the menu, call that function
        # else if the choice is q, do nothing with screen clearing
        # else let the user know that their input was not valid
        if choice in menu:
            clear()
            menu[choice]()
        elif choice == 'q':
            pass
        else:
            input("\nSorry that is not a valid input. Please enter a valid option from the menu(v/a/b). Please press enter to continue... ")

def add_product():
    """ Add a new product to the database """

    # Print instructions for the add_product section
    print("\n" + "*"*100)
    print("\nWelcome to the add product section! In this section we are going to ask you for the product information:\n")
    print("Product Name - the name of the product you would like to add.")
    print("Product Price - the price of the product you would like to add (must be in the form of $###.##).")
    print("Product Quantity - the quantity of the product you would like to add.\n")
    print("*"*100 + "\n")

    # get user input for product name
    user_product_name = input("Please enter the name of the product: ")

    # get input from the user for the product price. making sure they follow the requested input
    user_product_price = input("Please enter the price of the product ($###.##): ")

    while regex_money_input.match(user_product_price) == None:
        user_product_price = input("Sorry that was not a valid input. Please enter the price of the product ($###.##): ")

    # convert the user input to appropriate format for storing in the database
    user_product_price = csv_control.fix_price(user_product_price)

    # initialize user_input = 0 and display message to initial message
    user_product_qty = -1
    display_message = "Please enter the quantity of the product: "

    # loop until the user enters a valid input (must be greater than or equal to 0)
    while user_product_qty < 0:
        try:
            # get the input from the user and check to see if it is greater than or equal to 0
            user_product_qty = int(input(display_message))
            if user_product_qty < 0:
                display_message = "Sorry that was not a valid entry. Please enter a value greater than 0: "
        except ValueError:
            # if user enters anthing outside of an (letter, special character, etc.) let the user know it was not a valid input
            user_product_qty = -1
            display_message = "Sorry that was not a valid entry. Please enter a value greater than 0: "

    # after all fields are ok, get the date timestamp in the format we are using to store on sqlite db
    user_product_updated_date = datetime.datetime.strptime(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'%Y-%m-%d %H:%M:%S')

    temp_product = {
        'product_name' : user_product_name,
        'product_price' : user_product_price,
        'product_qty' : user_product_qty,
        'date_updated' : user_product_updated_date
    }

    product.add_product(temp_product)

    input("\nPlease press enter to continue... ")

def view_product():
    """ View a single product's inventory """
    
    # initialize user_input = 0 and display message to initial message
    user_input = 0
    display_message = "Please enter a product ID you would like to view: "

    # loop until the user enters a valid input (must be greater than 0)
    while user_input <= 0:
        try:
            # get the input from the user and check to see if it is greater than 0
            user_input = int(input(display_message))
            if user_input <= 0:
                display_message = "Sorry that was not a valid selection. Please try again: "
        except ValueError:
            # if user enters anthing outside of an (letter, special character, etc.) let the user know it was not a valid input
            user_input = 0
            display_message = "Sorry that was not a valid selection. Please try again: "

    # Once a valid input is recieved call for the database to try to retrieve that product id and display information
    product.view_product(user_input)
    user_input = input("Press enter to continue.")

def backup_database():
    """ Backup the store inventory """
    pass

# Define menu options
menu = OrderedDict([
    ('v', view_product),
    ('a', add_product),
    ('b', backup_database),
])

# Create your Dunder Main statement.

if __name__ == '__main__':
    main()