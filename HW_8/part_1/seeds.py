from models import Author, Quote
import connect
import json

def load_authors(filename):
    with open(filename) as f:
        data = json.load(f)
        for author in data:
            author = Author(fullname=author['fullname'],
                            born_date=author['born_date'],
                            born_location=author['born_location'],
                            description=author['description'])
            print(author)
            author.save()
            print()

def load_quotes(filename):
    with open(filename) as f:
        data = json.load(f)
        for quote in data:
            quote = Quote(tags=quote['tags'],
                           author=quote['author'],
                           quote=quote['quote'])
            quote.save()

if __name__ == "__main__":
    load_authors('authors.json')
    load_quotes('quotes.json')

