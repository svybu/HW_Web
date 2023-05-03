import scrapy
import json
import logging


class MainSpider(scrapy.Spider):
    name = "main"
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
    ]

    def parse_author(self, response):
        author_info = {
            'fullname': response.css('h3.author-title::text').get().strip(),
            'born_date': response.css('span.author-born-date::text').get().strip(),
            'born_location': response.css('span.author-born-location::text').get().strip(),
            'description': response.css('div.author-description::text').get().strip()
        }
        yield author_info

    def parse(self, response):
        for quote in response.css('div.quote'):
            quote_data = {
                'tags': [tag.css('a::text').get() for tag in quote.css('div.tags a')],
                'author': quote.css('div.quote > span > small::text').get().strip(),
                'quote': quote.css('span.text::text').get().strip(),
            }
            yield quote_data

            author_url = quote.css('div.quote > span > a::attr(href)').get()
            yield response.follow(author_url, self.parse_author)

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)


logging.basicConfig(filename='log.txt', level=logging.DEBUG)
logging.debug('Debugging information')

if __name__ == '__main__':
    process = scrapy.crawler.CrawlerProcess()
    process.crawl(MainSpider)
    process.start()

