import csv, json
import click
from flask import Blueprint
from .models import db, get_enum
from .linkage.epidoc import full_parse_on_inscription

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

@import_.cli.command("complex")
@click.argument("enum_name")
@click.argument("from_file")
def complex(enum_name, from_file):
    print("IMPORT BEGIN:", enum_name)
    enum = get_enum(enum_name)
    with open(from_file, "r") as complex_data_file:
        data = json.loads(complex_data_file.read())
    
    reftbl = {'': None}

    _load_complex_data('', data, reftbl, enum)
    db.session.commit()
    print("IMPORT END, Success.")

def _load_complex_data(ok, odata, reftbl, enum):
    for k, data in odata.items():
        lk = f"{ok}.{k}"

        name, lod = data['name'], data['lod']
        print("Importing:", name)

        item = enum(title=name, enum_lod=lod, parent_object_decoration_tag=reftbl[ok])
        db.session.add(item)

        reftbl[lk] = item

        _load_complex_data(lk, data['children'], reftbl, enum)

@import_.cli.command("cleanup_bom")
def cleanup_bom():
    with open("models/definition.json", "r") as f:
        defn = json.load(f)
    
    enums = defn['enums']

    for enum in enums:
        print(f"Processing: {enum}")
        for item in get_enum(enum).query.all():
            item.title = item.title.strip()
            item.title = item.title.encode("utf-8").decode("utf-8-sig")
            print(f"  {item.title}")
    
    db.session.commit()
    print("Done.")


@import_.cli.command("rerender_ínscription_text")
def rerender_insc_text():
    insc = get_enum('Inscriptions')

    for i in insc.query.all():
        full_parse_on_inscription(i)
        if inscription.text_interpretative_cached == "EPIDOC IS INVALID; UPDATE WITH WELL-FORMED XML":
            print(f"Inscription #{i.id} failed to render.")
    
    db.session.commit()
    print("Done.")