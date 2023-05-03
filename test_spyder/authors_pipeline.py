import json


class AuthorsPipeline:
    def __init__(self):
        self.authors_list = []

    def process_item(self, item, spider):
        author = {'fullname': item['fullname'], 'born_date': item['born_date'], 'born_location': item['born_location'],
                  'description': item['description']}
        if author not in self.authors_list:
            self.authors_list.append(author)

    def close_spider(self, spider):
        with open('authors.json', 'w') as f:
            for author in self.authors_list:
                f.write(json.dumps(author) + '\n')
