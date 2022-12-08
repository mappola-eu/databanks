from .zotero import ZoteroLinker
from .smart import SmartLinker

class NullLinker:
    def link(self, item): return None

LINKERS = {
    "zotero": ZoteroLinker(),
    "smart": SmartLinker(),
    "null": NullLinker()
}