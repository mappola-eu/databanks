import csv
import json
import xml.etree.ElementTree as ET
import click
from datetime import datetime as dt
from flask import Blueprint
from .models import db, get_enum, get_defn, Inscriptions, User, Publications
from .linkage.epidoc import full_parse_on_inscription
from .controllers.resource import apply_special_defn_to_item

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

        item = enum(title=name, enum_lod=lod,
                    parent_object_decoration_tag=reftbl[ok])
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
@click.argument("forcetitle")
def inscription(from_file, forcetitle):
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

        if value is None:
            continue

        if col == 'title' and forcetitle:
            value += " - " + forcetitle

        if "&amp;ndash;" in value or "&amp;amp;" in value or "&amp;quot;" in value \
            or "&amp;lt;" in value or "&amp;gt;" in value:
            value = value.replace("&amp;", "&") # first pass

            # second pass:
            value = value.replace("&ndash;", '–')
            value = value.replace("&amp;", '&')
            value = value.replace("&quot;", '"')
            value = value.replace("&lt;", '<')
            value = value.replace("&gt;", '>')

        outmap[col] = value

    if conflicts:
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
        if not val:
            continue

        if "@" in col:
            col, clspath = col.split("@")
            cls, attr = clspath.split(".")
            cls = get_enum(cls)

            val = cls(**{attr: val})

            getattr(i, col).append(val)

        else:
            setattr(i, col, val)

    # Determine, which user created this inscription
    who = User.query.first()
    who_node = root.find("./teiHeader/revisionDesc/change")

    if who_node is not None:
        who_name = who_node.attrib['who']
        who_name = who_name.strip().upper().strip('0123456789')

        who = User.query.filter(User.full_name.ilike(who_name)).one_or_none() or who

    defn = get_defn('Inscriptions')
    apply_special_defn_to_item(defn, i, True, who)

    source = root.find("./teiHeader/fileDesc/publicationStmt/authority").text.strip()
    source_id = root.find("./teiHeader/fileDesc/publicationStmt/idno[@type=\"localID\"]").text.strip()

    i.import_notice = f"Imported from {source} at {dt.now().isoformat()[:-7]}, ID there: {source_id}"

    db.session.add(i)
    db.session.commit()


def import_mods(col, mod, node, conflicts):
    if node is None:
        return None

    elif mod == 'text':
        if node.text is None:
            return None

        return node.text.strip()

    elif mod == 'minmaxmin':
        if node.text is None:
            return None

        return float(node.text.strip().split("-")[0].replace(",", "."))

    elif mod == 'minmaxmax':
        if node.text is None:
            return None

        return float(node.text.strip().split("-")[-1].replace(",", "."))

    elif mod == "childish.outerXML":
        result = ""
        for subnode in node:
            if subnode.tag == "head": continue
            result += ET.tostring(node, encoding="utf-8").decode("utf-8")

        return result

    elif mod == "stripXML":
        def stripXML(tag): return (tag.text or '') + ''.join(stripXML(e)
                                                             for e in tag) + (tag.tail or '')

        return stripXML(node).strip().replace("<br>", "\n")

    elif mod.startswith("ref:") or mod.startswith("ref.lod:"):
        if mod.startswith("ref:"):
            if node.text is None:
                return None

            ref = mod[len("ref:"):]
            value = node.text.strip()
            col = 'title'
            if ":" in ref:
                ref, col = ref.split(":")

        elif mod.startswith("ref.lod:"):
            ref = mod[len("ref.lod:"):]
            col = 'enum_lod'
            if 'ref' not in node.attrib:
                return None

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
        if attr not in node.attrib:
            return None

        return node.attrib[attr]

    return None



@import_.cli.command("biblfix")
@click.argument("from_file")
@click.argument("forcetitle")
def biblfix(from_file, forcetitle):
    inscription = Inscriptions.query.filter(Inscriptions.title.like(f'% - {forcetitle}')).one_or_none()

    if not inscription:
        print("No inscription found, aborting.")
        return

    with open("models/xmlmapping.txt", "r") as xmlmapfile:
        xmlmapraw = xmlmapfile.read()

    tree = ET.iterparse(from_file)
    for _, el in tree:
        el.tag = el.tag.split('}', 1)[1]  # strip all namespaces
    root = tree.root
    
    bibliography = root.findall('./text/body/div[@type="bibliography"]/listBibl/bibl')
    all_bibliography = []

    for bibl in bibliography:
        bibl = bibl.text.strip()
        all_bibliography.append(bibl)
    
    all_bibliography.append(forcetitle)

    for entry in all_bibliography[1:]:
        db.session.add(Publications(inscription=inscription, reference_comment=entry))

    db.session.commit()
    print(f"Fixed {forcetitle} bibliography")