from ..config import SETTINGS


class SmartLinker:

    def link(self, item):
        if item.link_to_published_translation.startswith("http:") or item.link_to_published_translation.startswith("https:") or item.link_to_published_translation.startswith("ftp:"):
            return item.link_to_published_translation
