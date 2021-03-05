import json
import hashlib
import subprocess
import datetime as dt
from pathlib import Path


FOLDER = Path("data")


def datetime_encoder(obj):
    if isinstance(obj, (dt.date, dt.datetime)):
        return obj.isoformat(timespec="seconds")


def dict_hash(obj):
    dict_str = json.dumps(
        item, sort_keys=True, ensure_ascii=False, default=datetime_encoder
    )
    hasher = hashlib.sha256()
    hasher.update(dict_str.encode("utf8"))
    return hasher.hexdigest()


class Check:
    def process_item(self, item, spider):
        if "url" not in item:
            raise ValueError(f'Item should have a "url" field')
        return item


class IncludeFields:
    def open_spider(self, spider):
        self.crawl = dt.datetime.utcnow()
        self.version = ""

    def process_item(self, item, spider):
        new_item = {
            "raw": item,
            "timestamp": self.datetime.utcnow(),
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
        with open(filename, "a") as f:
            f.write(item_str + "\n")

        return item


```
{
    "raw": {
        "url": "https://some.domain.com/some/path",
    },
    "timestamp": "2021-03-05T05:14:30.301258",
    "hash": "0123456789ABCDEF",
    "spider": "some spider name",
    "version": "0123456789ABCDEF",
    "crawl": "2021-03-05T05:14:30.301258",
}
```

raw: o conteúdo do item, um dicionário, conforme enviado pela spider  
    url: todos os items já devem vir com uma chave "url"  
timestamp: o horário que o item foi coletado  
hash: o sha256 do json do conteúdo do item  
spider: o nome da spider  
version: o commit que no qual o código esta sendo executado  
crawl: o horário que o crawl foi iniciado

