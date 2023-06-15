import csv, json
import xml.etree.ElementTree as ET
import click
from flask import Blueprint
from .models import db, get_enum, get_defn, Inscriptions
from .linkage.epidoc import full_parse_on_inscription
from .controllers.resource import apply_defn_post_data_to_obj

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
        item = enum(title=entry[0])

        if entry[1]:
            item.enum_lod = entry[1]

        db.session.add(item)
    
    db.session.commit()
    print("IMPORT END, Success.")

@import_.cli.command("enum:complex")
@click.argument("enum_name")
@click.argument("from_file")
def enum_complex(enum_name, from_file):
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
        if i.text_interpretative_cached == "EPIDOC IS INVALID; UPDATE WITH WELL-FORMED XML":
            print(f"Inscription #{i.id} failed to render.")
    
    db.session.commit()
    print("Done.")

@import_.cli.command("inscription")
@click.argument("from_file")
def inscription(from_file):
    with open("models/xmlmapping.txt", "r") as xmlmapfile:
        xmlmapraw = xmlmapfile.read()
    
    tree = ET.iterparse(from_file)
    for _, el in tree:
        el.tag = el.tag.split('}', 1)[1]  # strip all namespaces
    root = tree.root
    
    xmlmap = {}
    for line in xmlmapraw.split("\n"):
        col, expr = line.split(":", 1)
        col, expr = col.strip(), expr.strip()

        mod = None
        path = expr

        if "->" in expr:
            path, mod = expr.rsplit("->", 1)
            path, mod = path.strip(), mod.strip()
        
        xmlmap[col] = (path, mod)
    
    outmap = {}
    conflicts = []

    for col, (path, mod) in xmlmap.items():
        node = root.find("." + path)
        value = import_mods(col, mod, node, conflicts)

        outmap[col] = value

    print("Conflicts found:\n---\n\nCannot associate the following values")
    for c in conflicts:
            print(f"{c[0]:24} = ({c[1]}) {c[2]}")
    
    print()

    if len(conflicts) >= 4:
        print("ATTENTION! There are more than four conflicts.")

        if input("Continue? (Yn) ").lower() == 'n':
            return

    i = Inscriptions()

    for col, val in outmap.items():
        if not val: continue
        print(col, repr(val))
        setattr(i, col, val)

    defn = get_defn('Inscriptions')
    apply_defn_post_data_to_obj(defn, i, True)

    print(i)
    
    #db.session.add(i)
    #db.session.commit()


def import_mods(col, mod, node, conflicts):
    if mod == 'text':
        return node.text
    
    elif mod == 'minmaxmin':
        return float(node.text.split("-")[0].replace(",", "."))
    
    elif mod == 'minmaxmax':
        return float(node.text.split("-")[-1].replace(",", "."))
    
    elif mod == "outerXML":
        return ET.tostring(node, encoding="utf-8").decode("utf-8")
    
    elif mod == "stripXML":
        stripXML = lambda tag: (tag.text or '') + ''.join(stripXML(e) for e in tag) + (tag.tail or '')

        return stripXML(node).strip().replace("<br>", "\n")
    
    elif mod.startswith("ref:") or mod.startswith("ref.lod:"):
        if mod.startswith("ref:"):
            ref = mod[len("ref:"):]
            value = node.text
            col = 'title'
            if ":" in ref:
                ref, col = ref.split(":")

        elif mod.startswith("ref.lod:"):
            ref = mod[len("ref.lod:"):]
            col = 'enum_lod'
            value = node.attrib['ref']

            if value.startswith("http:"):
                value = "https:" + value[len("http:"):]

        R = get_enum(ref)

        # Check for exact match
        match = R.query.filter_by(**{col: value}).all()
        if len(match) == 1:
            return match[0]

        # Check for rough match
        match = R.query.filter(getattr(R, col).like(f"%{value}%")).all()
        if len(match) == 1:
            return match[0]

        # Check for loose match
        matcher = '%' + '%'.join(value) + '%'
        match = R.query.filter(getattr(R, col).like(matcher)).all()
        if len(match) == 1:
            return match[0]
        
        conflicts.append([ref, col, value])
    
    elif mod.startswith("attr:@"):
        attr = mod[len("attr:@"):]
        return node.attrib[attr]
    
    return None