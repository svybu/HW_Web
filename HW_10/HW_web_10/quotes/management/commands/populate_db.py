import json
from django.core.management.base import BaseCommand

from quotes.models import Author, Quote


class Command(BaseCommand):
    help = 'Populate the database with data from authors.json and quotes.json'

    def handle(self, *args, **options):

        with open('authors.json', 'r') as file:
            authors_data = json.load(file)

        with open('quotes.json', 'r') as file:
            quotes_data = json.load(file)

        for author_data in authors_data:
            Author.objects.create(
                fullname=author_data['fullname'],
                born_date=author_data['born_date'],
                born_location=author_data['born_location'],
                description=author_data['description']
            )

        for quote_data in quotes_data:
            author_fullname = quote_data['author']
            author = Author.objects.filter(fullname=author_fullname).first()

            Quote.objects.create(
                text=quote_data['quote'],
                author=author
            )

        self.stdout.write(self.style.SUCCESS('Database population completed successfully.'))
