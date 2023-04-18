from models import Quote, Author
import sys
from bson.objectid import ObjectId
import connect

author_name = "Albert Einstein"

author_name = Author.objects(fullname=author_name).first()


if author_name:
    print(author_name.fullname)
    quotes_by_author = Quote.objects(author=author_name)
    print(quotes_by_author)
    for quote in quotes_by_author:
        print(quote.author)
else:
    print(f"No quotes found for author {author_name}")

