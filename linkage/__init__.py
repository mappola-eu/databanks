from .zotero import ZoteroLinker

class NullLinker:
    def link(self, item): return None

LINKERS = {
    "zotero": ZoteroLinker(),
    "null": NullLinker()
}