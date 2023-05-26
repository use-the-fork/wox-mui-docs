# encoding=utf8

import requests
import webbrowser
from wox import Wox, WoxAPI
import urllib.parse
import html
import re
from algoliasearch.search_client import SearchClient

client = SearchClient.create("TZGZ85B9TB", "8177dfb3e2be72b241ffb8c5abafa899")
index = client.init_index("material-ui")
docs = "https://mui.com/material-ui/"


class MUIDocs(Wox):

    def getTitle(self, hierarchy):
        if hierarchy["lvl6"] is not None:
            return hierarchy["lvl6"]

        if hierarchy["lvl5"] is not None:
            return hierarchy["lvl5"]

        if hierarchy["lvl4"] is not None:
            return hierarchy["lvl4"]

        if hierarchy["lvl3"] is not None:
            return hierarchy["lvl3"]

        if hierarchy["lvl2"] is not None:
            return hierarchy["lvl2"]

        if hierarchy["lvl1"] is not None:
            return hierarchy["lvl1"]

        if hierarchy["lvl0"] is not None:
            return hierarchy["lvl0"]

        return None

    def getSubtitle(self, hierarchy):
        if hierarchy["lvl6"] is not None:
            return hierarchy["lvl5"]

        if hierarchy["lvl5"] is not None:
            return hierarchy["lvl4"]

        if hierarchy["lvl4"] is not None:
            return hierarchy["lvl3"]

        if hierarchy["lvl3"] is not None:
            return hierarchy["lvl2"]

        if hierarchy["lvl2"] is not None:
            return hierarchy["lvl1"]

        if hierarchy["lvl1"] is not None:
            return hierarchy["lvl0"]

        return None

    def query(self, key):
        items = []

        if key.strip():

            search = index.search(
                key, {"facetFilters": "product:material-ui", "hitsPerPage": 5}
            )

            for hit in search["hits"]:

                title = self.getTitle(hit['hierarchy'])
                subtitle = self.getSubtitle(hit['hierarchy'])
                url = hit["url"]

                text = False
                try:
                    # strip the hightlight tags from the result
                    text = re.sub('<[^<]+?>', '', hit["_highlightResult"]["content"]["value"])
                except KeyError:
                    pass

                if text and subtitle:
                    title = "{} - {}".format(title, subtitle)
                    subtitle = text

                items.append(
                    {
                        "Title": html.unescape(title),
                        "SubTitle": html.unescape(subtitle if subtitle is not None else ""),
                        "IcoPath": "Images/icon.png",
                        "JsonRPCAction":
                            {
                                "method": "openUrl",
                                "parameters": [url],
                                "dontHideAfterAction": False
                            }
                    }
                )

            if len(items) == 0:
                term = "laravel {}".format(key)

                google = "https://www.google.com/search?q={}".format(
                    urllib.parse.quote(term)
                )

                items.append(
                    {
                        "Title": "Search Google",
                        "SubTitle": 'No match found. Search Google for: "{}"'.format(term),
                        "IcoPath": "Images/icon.png",
                        "JsonRPCAction":
                            {
                                "method": "openUrl",
                                "parameters": [google],
                                "dontHideAfterAction": False
                            }
                    }
                )

                items.append(
                    {
                        "Title": "Open MUI Docs",
                        "SubTitle": "No match found. Open mui.com/material-ui...",
                        "IcoPath": "Images/icon.png",
                        "JsonRPCAction":
                            {
                                "method": "openUrl",
                                "parameters": [docs],
                                "dontHideAfterAction": False
                            }
                    }
                )

        return items

    def openUrl(self, url):
        webbrowser.open(url)
        # todo:doesn't work when move this line up
        WoxAPI.change_query(url)


if __name__ == "__main__":
    MUIDocs()
