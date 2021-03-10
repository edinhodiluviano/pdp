from urllib.parse import urlencode, parse_qs, urljoin

import scrapy
from scrapy import Request
import pandas as pd


class FlexjobsComSpider(scrapy.Spider):
    name = "flexjobs_com"
    allowed_domains = ["flexjobs.com"]

    def start_requests(self):
        yield self.request_for_page(page=1, callback=self.first_page)

    def request_for_page(self, page: int, callback):
        params = {
            "category%5B%5D": [38, 11],
            "location": "",
            "page": page,
            "search": "",
            "tele_level%5B%5D": "All+Telecommuting",
        }

        url = "https://www.flexjobs.com/search?" + urlencode(params)

        req = Request(
            url=url,
            callback=callback,
        )
        return req

    def first_page(self, response):
        """
        Parses only the first page yielded by start_requests
        yield:
            job pages requests
            other pages requests
        """

        last_page = 0
        for link in response.css("a.page-link"):
            if link.attrib["href"].startswith("/search?"):
                query_dict = parse_qs(link.attrib["href"])
                if "page" in query_dict:
                    page_str = query_dict["page"][0]
                    page = int(page_str)
                    last_page = max(last_page, page)

        for page in range(2, last_page + 1):
            yield self.request_for_page(page=page, callback=self.other_pages)

        self.other_pages(response)

    def other_pages(self, response):
        """
        Parses all other pages yielded by the first page
        yield
            job pages requests
        """
        for link in response.css("a.job-link"):
            if link.attrib["href"].startswith("/publicjobs/"):
                req = Request(
                    url=urljoin(response.url, link.attrib["href"]),
                    callback=self.parse,
                )
                print(req)
                yield req

    def parse(self, response):
        """For each page yield one item"""

        item = {}
        item["url"] = response.url
        item["title"] = response.css("h1")[0].css("::text")[0].get()
        item["description"] = response.xpath(
            '//div[contains(@id,"job-description")]//p/text()'
        ).get()

        table_html = response.xpath(
            '//div[contains(@id,"job-description")]//table'
        ).get()
        df = pd.read_html(table_html)[0]
        for idx, row in df.iterrows():
            item[row[0].strip(":")] = row[1]

        yield item
