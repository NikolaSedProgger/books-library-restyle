import argparse
from dbm.ndbm import library
import os
import time
import json
from urllib.parse import urljoin, urlparse


from bs4 import BeautifulSoup
from requests import get, HTTPError, ConnectionError

from main import parse_book_page, download_text, download_image, check_for_redirect


def get_books_urls(start_page, end_page, library_num):
    books_urls = []
    for page in range(start_page, end_page):
        url = f'https://tululu.org/l{library_num}/{page}/'
        response = get(url, allow_redirects=True)
        response.raise_for_status()
        check_for_redirect(response)
        soup = BeautifulSoup(response.text, 'lxml')
        soup_tags = soup.select('table.d_book')
        for tag in soup_tags:
            books_urls.append(urljoin('https://tululu.org/', tag.select_one('a')['href']))
    return books_urls


def main(start_page, end_page):
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
    os.makedirs(os.path.join(args.dest_folder, "books"), exist_ok=True)
    os.makedirs(os.path.join(args.dest_folder, "images"), exist_ok=True)
    os.makedirs(os.path.join(args.dest_folder, args.json_path), exist_ok=True)
    library_num = 55
    parsed_books = []
    try:
        for book_url in get_books_urls(start_page, end_page+1, library_num):
            try:
                response = get(book_url)
                response.raise_for_status()
                check_for_redirect(response)
                parsed_book = parse_book_page(response)
                book_id = urlparse(book_url).path.replace('/b', '')
                if not args.skip_txt:
                    download_text(book_id, book_id, os.path.join(args.dest_folder,'books'))
                if not args.skip_imgs:
                    download_image(parsed_book['book_image'], os.path.join(args.dest_folder,'images'))
                parsed_books.append(parsed_book)
            except HTTPError:
                print('Ошибка HTTPError.')
                time.sleep(5)
                main(start_page, end_page)
    except ConnectionError:
        print("Ошибка ConnectionError.")
        time.sleep(5)
        main(start_page, end_page)
    with open(os.path.join(args.dest_folder, args.json_path, 'books.json'), 'w', encoding='utf8') as json_file:
        json.dump(parsed_books, json_file, ensure_ascii=False)
