import csv
import click
from flask import Blueprint
from .models import db, get_enum

import_ = Blueprint('import', __name__)

@import_.cli.command("prepare")
def prepare():
    db.create_all()
    print("Success.")

@import_.cli.command("enum")
@click.argument("enum_name")
@click.argument("from_file")
def enum(enum_name, from_file):
    print("IMPORT BEGIN:", enum_name)
    enum = get_enum(enum_name)
    with open(from_file, "r") as enum_data_file:
        data = csv.reader(enum_data_file, delimiter=";")
        data = [col for col in data]
    
    for entry in data:
        print("Importing:", entry[0])
        item = enum(title=entry[0], enum_lod=entry[1])
        db.session.add(item)
    
    db.session.commit()
    print("IMPORT END, Success.")
    