from collections import OrderedDict
import datetime
import os
import sys

from peewee import *

db = SqliteDatabase('inventory.db')

