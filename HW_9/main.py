import requests
from bs4 import BeautifulSoup
import json

url = 'https://quotes.toscrape.com/'

def get_author_info(about_url, authors_list):
    response = requests.get(about_url)
    soup = BeautifulSoup(response.text, 'lxml')
    fullname = soup.find('h3', class_='author-title').text
    for author in authors_list:
        if author['fullname'] == fullname:
            return author
    born_date = soup.find('span', class_='author-born-date').text
    born_location = soup.find('span', class_='author-born-location').text
    description = soup.find('div', class_='author-description').text
    author = {'fullname': fullname, 'born_date': born_date, 'born_location': born_location, 'description': description}
    authors_list.append(author)
    return author

def get_quotes_info(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    quotes = soup.find_all('div', class_='quote')
    quotes_list = []
    authors_list = []
    for quote in quotes:
        tags = [tag.text for tag in quote.select('.tags a.tag')]
        author_link = quote.select_one('.author + a')['href']
        about_url = url + author_link
        author = get_author_info(about_url, authors_list)
        quote_text = quote.select_one('.text').text
        quote_dict = {'tags': tags, 'author': author['fullname'], 'quote': quote_text}
        quotes_list.append(quote_dict)
    return quotes_list, authors_list

if __name__ == '__main__':
    url = 'http://quotes.toscrape.com/'
    quotes_list, authors_list = get_quotes_info(url)
    with open('quotes.json', 'w') as f:
        json.dump(quotes_list, f)
    with open('authors.json', 'w') as f:
        json.dump(authors_list, f)
