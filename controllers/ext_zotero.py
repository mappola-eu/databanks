from flask import *
from ..models import db, get_enum, defn, get_defn, defn_parse, render_column, defn_parse_raw, defn_snippet, get_rel, get_rel_defn
from flask_security import login_required
from pyzotero import zotero
from ..config import SETTINGS

with open(".zotero-api", "r") as f:
    API_KEY = f.read().strip()

ext_zotero = Blueprint('ext_zotero', __name__)

@ext_zotero.before_request
def initialize_connection():
    g.zot = zotero.Zotero(SETTINGS['ZOTERO_ID'], 'group', API_KEY)

@ext_zotero.route("/query", methods=["GET"])
@login_required
def query():
    query_string = request.args.get("for", None)
    if query_string is None:
        abort(400)
    
    items = g.zot.items(q=query_string, qmode='everything')
    items_found = len(items)
    items = map(_datamap, items)

    return {
        "found": items_found,
        "items": [*items]
    }

@ext_zotero.route("/fetch/<key>", methods=["GET"])
@login_required
def fetch(key):    
    item = g.zot.item(key)

    return {
        "found": 1,
        "items": [item]
    }

@ext_zotero.route("/quickadd/types", methods=["GET"])
@login_required
def qadd_types():    
    types = g.zot.item_types()

    return {
        "found": len(types),
        "items": types
    }

@ext_zotero.route("/quickadd/of/type/<type>", methods=["POST"])
@login_required
def qadd(type):    
    title = request.form.get("title", None)
    
    avail_item_types = g.zot.item_types()
    avail_item_types = [i['itemType'] for i in avail_item_types]

    if type not in avail_item_types:
        abort(400)
    
    if title is None:
        abort(400)

    template = g.zot.item_template(type, None)
    template['title'] = title
    resp = g.zot.create_items([template])

    if len(resp['success'].keys()) == 1:
        return {
            "found": 1,
            "items": [
                {
                    "key": resp['success']['0']
                }
            ]
        }
    else:
        abort(500)

def _datamap(item):
    more_authors = " et al." if len(item['data']['creators']) > 1 else ""
    if len(item['data']['creators']) != 0:
        authors = item['data']['creators'][0]['firstName'] + ' ' + item['data']['creators'][0]['lastName'] + more_authors
    else:
        authors = ""
    return {
        "key": item['key'],
        "title": item['data']['title'],
        "authors": authors,
        "link": item['links']['self']['href']
    }