from ..config import SETTINGS


class ZoteroLinker:

    def __init__(self):
        self.zotero_id = SETTINGS['ZOTERO_ID']

    def link(self, item):
        item_id = item.zotero_item_id

        if item_id:
            link_format = "https://www.zotero.org/groups/" + self.zotero_id + \
                "/-/items/" + item_id + "/item-details"

            return link_format, item.reference_comment
        
        elif item.reference_comment.startswith("http:") or item.reference_comment.startswith("https:") or item.reference_comment.startswith("ftp:"):
            if "|" in item.reference_comment:
                return item.reference_comment.split("|", 1)
            else:
                return item.reference_comment, item.reference_comment
