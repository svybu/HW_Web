import scrapy
import json
import logging
from scrapy.crawler import CrawlerProcess
from common_pipeline import CommonPipeline


class QuoteItem(scrapy.Item):
    author = scrapy.Field()
    quote = scrapy.Field()
    tags = scrapy.Field()


class AuthorItem(scrapy.Item):
    fullname = scrapy.Field()
    born_date = scrapy.Field()
    born_location = scrapy.Field()
    description = scrapy.Field()


class MainSpider(scrapy.Spider):
    name = "main"
    custom_settings = {"FEED_EXPORT_ENCODING": 'utf-8', "ITEM_PIPELINES": {CommonPipeline: 300}}
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        for quote in response.xpath("/html//div[@class='quote']"):
            yield response.follow(url=self.start_urls[0] + quote.xpath("span/a/@href").get(),
                                  callback=self.parse_author)

        for quote in response.xpath("/html//div[@class='quote']"):
            tags, *_ = quote.xpath("div[@class='tags']/a/text()").extract(),
            author, *_ = quote.xpath("span/small/text()").get(),
            quote = quote.xpath("span[@class='text']/text()").get()
            quote_item = QuoteItem(author=author, quote=quote, tags=tags)
            yield quote_item

        next_link = response.xpath("//li[@class='next']/a/@href").get()
        if next_link:
            yield scrapy.Request(url=self.start_urls[0] + next_link)

    def parse_author(self, response):
        info = response.xpath("/html//div[@class='author-details']")
        fullname, *_ = info.xpath("h3/text()").get().strip(),
        born_date, *_ = info.xpath("p/span[@class='author-born-date']/text()").get().strip(),
        born_location, *_ = info.xpath("p/span[@class='author-born-location']/text()").get().strip(),
        description, *_ = info.xpath("div[@class='author-description']/text()").get().strip(),
        author_item = AuthorItem(fullname=fullname, born_date=born_date, born_location=born_location,
                                 description=description)
        yield author_item


if __name__ == '__main__':
    # run spider
    process = CrawlerProcess()
    process.crawl(MainSpider)
    process.start()
    print('end')
