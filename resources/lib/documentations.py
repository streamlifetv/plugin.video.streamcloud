__author__ = 'ror'

import xbmcgui
from resources.lib import const, http
from resources.lib.items.directory_item import DirectoryItem
from resources.lib.items.video_item import VideoItem


class Documentations:
    def __init__(self):
        self.item_list = []
        pass

    def index(self, params):
        for letter in '#ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            self.item_list.append(
                DirectoryItem(
                    letter,
                    "?view=documentations&action=list&letter=%s" % letter)
            )
        return self.item_list
        pass

    def search(self, params):
        dialog = xbmcgui.Dialog()
        d = dialog.input('Search', type=xbmcgui.INPUT_ALPHANUM)

        obj = http.get("%s/search.php?type=documentations&title=%s&lang=%s" % (const.SERVICE_URL, d, const.LANG))

        for video in obj:
            self.item_list.append(
                VideoItem(
                    "%s [%s]" % (video['title'],
                                 const.LANG_CODES[video['lang']]),
                    "?view=play&title=" + video['urlTerm'],
                    "%s/thumbs/%s.jpg" % (const.SERVICE_URL, video['urlTerm'])
                )
            )
        return self.item_list

    def list(self, params):
        letter = params('letter')

        obj = http.get("%s/?type=documentations&letter=%s&lang=%s" % (const.SERVICE_URL, letter, const.LANG))

        for video in obj:
            self.item_list.append(
                VideoItem(
                    "%s [%s]" % (video['title'],
                                 const.LANG_CODES[video['lang']]),
                    "?view=play&title=" + video['urlTerm'],
                    "%s/thumbs/%s.jpg" % (const.SERVICE_URL, video['urlTerm'])
                )
            )
        return self.item_list