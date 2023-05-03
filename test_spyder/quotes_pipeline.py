import json


class QuotesPipeline:
    def __init__(self):
        self.quotes_list = []

    def process_item(self, item, spider):
        quote = {'tags': item['tags'], 'author': item['author'], 'quote': item['quote']}
        self.quotes_list.append(quote)

    def close_spider(self, spider):
        with open('quotes.json', 'w') as f:
            for quote in self.quotes_list:
                f.write(json.dumps(quote) + '\n')
