from models import Quote, Author
import sys
from bson.objectid import ObjectId
import connect

def utf(text):
    r =text.encode('utf-8')
    return r
def search_by_author(author_name):
    author = Author.objects(fullname=author_name).first()
    if not author:
        print(f"No quotes found for author {author_name}")
        return
    quotes = Quote.objects(author=author.fullname)
    for quote in quotes:
        print(utf(quote.quote))


def search_by_tag(tag):
    quotes = Quote.objects(tags=tag)
    if not quotes:
        print(f"No quotes found for tag {tag}")
        return
    for quote in quotes:
        print(utf(quote.quote))


def search_by_tags(tags):
    tags_list = tags.split(',')
    quotes = Quote.objects(tags__in=tags_list)
    if not quotes:
        print(f"No quotes found for tags {tags}")
        return
    for quote in quotes:
        print(utf(quote.quote))

def exit_program(*args):
    print("Exiting program...")
    sys.exit()

COMMANDS= {"name": search_by_author,
           "tag": search_by_tag,
           'tags': search_by_tags,
           'exit': exit_program
           }
def main():
    while True:
        command = input('Enter command: ')
        command_parts = command.split(':')
        command_name = command_parts[0].strip()
        if command_name in COMMANDS:
            command_args = command_parts[1].strip() if len(command_parts) > 1 else ''
            COMMANDS[command_name](command_args)
        else:
            print('Invalid command')


if __name__ == "__main__":
    main()