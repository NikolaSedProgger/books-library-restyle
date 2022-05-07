from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin, urlparse
import os
from main import parse_book_page, download_text, download_image
import json

os.makedirs("books", exist_ok=True)
os.makedirs("images", exist_ok=True)
parsed_books = []
for book_id in range(1, 11):
    url = f'https://tululu.org/l55/{book_id}/'
    response = requests.get(url, allow_redirects=True)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    books =  soup.find_all('table', class_='d_book')
    for book in books:
        book_url = urljoin('https://tululu.org/', book.find('a')['href'])
        book_id = urlparse(book_url).path.replace('/b','')
        response = requests.get(book_url)
        parsed_book = parse_book_page(response)
        parsed_books.append(parsed_book)

        print(book_id)
        try:
            download_text(book_id, parsed_book['book_title'])
            download_image(parsed_book['book_image'])
        except requests.HTTPError:
            None

with open('books.json', 'w', encoding='utf8') as json_file:
    json.dump(parsed_books, json_file, ensure_ascii=False)