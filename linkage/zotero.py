from ..config import SETTINGS


class ZoteroLinker:

    def __init__(self):
        self.zotero_id = SETTINGS['ZOTERO_ID']

    def link(self, item):
        item_id = item.zotero_item_id

        link_format = "https://www.zotero.org/groups/" + self.zotero_id + \
            "/-/items/" + item_id + "/item-details"

        return link_format
