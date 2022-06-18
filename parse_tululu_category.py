import argparse
import os
import json
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup
from requests import get, HTTPError

from main import parse_book_page, download_text, download_image


LIBRARY_NUM = 55
parser = argparse.ArgumentParser(
    description='Программа скачивает книги по указаным страницам'
)
parser.add_argument('-start', '--start_page', help='Первая страница', type=int)
parser.add_argument('-end', '--end_page', help='Последняя страница', default='702', type=int)
parser.add_argument('--skip_txt', action='store_true')
parser.add_argument('--skip_imgs', action='store_true')
parser.add_argument('--dest_folder', default='library files')
parser.add_argument('--json_path', default='json files')
args = parser.parse_args()


def get_books_urls(start_page, end_page):
    books_urls = []
    for page in range(start_page, end_page):
        url = f'https://tululu.org/l{LIBRARY_NUM}/{page}/'
        response = get(url, allow_redirects=True)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')
        soup_tags = soup.select('table.d_book')
        for tag in soup_tags:
            books_urls.append(urljoin('https://tululu.org/', tag.select_one('a')['href']))
    return books_urls


def main(start_page, end_page):
    os.makedirs(f"{args.dest_folder}/books", exist_ok=True)
    os.makedirs(f"{args.dest_folder}/images", exist_ok=True)
    os.makedirs(f"{args.dest_folder}/{args.json_path}", exist_ok=True)
    parsed_books = []
    for book_url in get_books_urls(start_page, end_page+1):
        response = get(book_url)
        response.raise_for_status()
        parsed_book = parse_book_page(response)
        book_id = urlparse(book_url).path.replace('/b', '')
        try:
            if not args.skip_txt:
                download_text(book_id, book_id, f'{args.dest_folder}/books')
            if not args.skip_imgs:
                download_image(parsed_book['book_image'], f'{args.dest_folder}/images')
            parsed_books.append(parsed_book)
        except HTTPError:
            None
    with open(f'{args.dest_folder}/{args.json_path}/books.json', 'w', encoding='utf8') as json_file:
        json.dump(parsed_books, json_file, ensure_ascii=False)

if __name__ == "__main__":
    main(args.start_page, args.end_page)
