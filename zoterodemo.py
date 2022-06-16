from pyzotero import zotero
from tabulate import tabulate
from pprint import pprint

from config import SETTINGS

api_key = None

with open(".zotero-api", "r") as f:
    api_key = f.read().strip()

zot = zotero.Zotero(SETTINGS['ZOTERO_ID'], 'group', api_key)

def datamap(item):
    more_authors = " et al." if len(item['data']['creators']) > 1 else ""
    if len(item['data']['creators']) != 0:
        authors = item['data']['creators'][0]['firstName'] + ' ' + item['data']['creators'][0]['lastName'] + more_authors
    else:
        authors = ""
    return [
        item['key'],
        item['data']['title'],
        authors,
        item['links']['self']['href'],
    ]

while True:
    cmd = input("[Zotero Demo]> ")
    if cmd == "q" or cmd == "quit" or cmd == "exit": break

    if cmd.startswith("?? "):
        queryword = cmd[3:]

        items = zot.items(q=queryword, qmode='everything')
        
        print(f"Found {len(items)} items.")

        items = map(datamap, items)
        print(tabulate(items, headers=['Key', 'Title', 'Author', 'Link'], tablefmt="psql"))

    elif cmd.startswith("= "):
        key = cmd[2:]

        item = zot.item(key)

        pprint(item)

    elif cmd.startswith("+ "):
        title = cmd[2:]

        print("Creating new item.")
        print("You must choose an item type.")

        avail_item_types = zot.item_types()
        avail_item_types = [i['itemType'] for i in avail_item_types]

        print("Available: " + ", ".join(avail_item_types))

        while True:
            itemtype = input("Item Type (empty to abort): ")

            if itemtype == "" or itemtype in avail_item_types:
                break
            else:
                print("type not found, retry.")

        if itemtype == "":
            continue
        
        template = zot.item_template(itemtype, None)

        template['title'] = title

        resp = zot.create_items([template])

        if len(resp['success'].keys()) == 1:
            print("Success.")
            print(f"New Item ID: {resp['success']['0']}")
        else:
            print("Something went wrong. Check in the online view and retry.")

    elif cmd == '-ityp':
        print(zot.item_types())

    elif cmd == '-itpl':
        it = input("item type: ")
        print(zot.item_template(it, None))