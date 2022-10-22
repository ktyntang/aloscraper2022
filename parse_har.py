from haralyzer import HarParser, HarPage
import json
import os


def find_url_in_har(file):
    with open(file, 'r', encoding="utf-8") as f:
        har_parser = HarParser(json.loads(f.read()))
    har_page = HarPage("unknown", har_parser=har_parser)

    for entry in har_page.entries:
        if 'video.m3u8' in entry.url:
            videourl = entry.url
            os.remove(file)
            return(videourl)
