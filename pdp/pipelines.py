import json
import hashlib
import datetime as dt
from pathlib import Path


FOLDER = Path("data")


def datetime_encoder(obj):
    if isinstance(obj, (dt.date, dt.datetime)):
        return obj.isoformat(timespec="seconds")


def dict_hash(obj):
    dict_str = json.dumps(
        obj, sort_keys=True, ensure_ascii=False, default=datetime_encoder
    )
    hasher = hashlib.sha256()
    hasher.update(dict_str.encode("utf8"))
    return hasher.hexdigest()


class Check:
    def process_item(self, item, spider):
        if "url" not in item:
            raise ValueError('Item should have a "url" field')
        return item


class IncludeFields:
    def open_spider(self, spider):
        self.crawl = dt.datetime.utcnow()
        self.version = ""

    def process_item(self, item, spider):
        new_item = {
            "raw": item,
            "timestamp": dt.datetime.utcnow(),
            "hash": dict_hash(item),
            "spider": spider.name,
            "version": self.version,
            "crawl": self.crawl,
        }
        return new_item


class Save:
    def process_item(self, item, spider):
        filename = FOLDER / spider.name
        item_str = json.dumps(
            item, sort_keys=True, ensure_ascii=False, default=datetime_encoder
        )
        item_str += "\n"
        with open(filename, "a") as f:
            f.write(item_str)

        return item
