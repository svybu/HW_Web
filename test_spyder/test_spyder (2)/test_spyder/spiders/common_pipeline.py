from itemadapter import ItemAdapter
import json


class CommonPipeline:
    authors = []
    quotes = []

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if 'author' in adapter.keys():
            self.quotes.append({'author': adapter['author'], 'quote': adapter['quote'], 'tags': adapter['tags']})
        if 'fullname' in adapter.keys():
            self.authors.append({'fullname': adapter['fullname'], 'born_date': adapter['born_date'],
                                 'born_location': adapter['born_location'], 'description': adapter['description']})
        return item

    def close_spider(self, spider):
        with open('quotes.json', 'w', encoding='utf-8') as f:
            json.dump(self.quotes, f, ensure_ascii=False, indent=4)
        with open('authors.json', 'w', encoding='utf-8') as f:
            json.dump(self.authors, f, ensure_ascii=False, indent=4)
