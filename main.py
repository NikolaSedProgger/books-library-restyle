import argparse
import os
from urllib.parse import urlparse, urljoin

from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
import requests




def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError


def parse_book_page(response):
    soup = BeautifulSoup(response.text, "lxml").select_one('table')
    book_title, book_author = soup.select_one('h1').text.split(' \xa0 :: \xa0 ')
    book_image = urljoin("https://tululu.org/", soup.select_one('td.ow_px_td img')['src'])
    book_description = soup.find('div', id='content').select('table.d_book')[1].select_one('td').text
    book_comments = [comment.select_one('span.black').text for comment in soup.select('div.texts')]
    book_genres = [genre.text for genre in soup.select_one('span.d_book').select('a')]
    parsed_book = {
        "book_title": book_title,
        "book_author": book_author,
        "book_description": book_description,
        "book_genres": book_genres,
        "book_comments": book_comments,
        "book_image": book_image,
    }
    return parsed_book


def download_text(id, filename, folder):
    params = {'id': id}
    url = 'https://tululu.org/txt.php'
    response = requests.get(url, params, allow_redirects=True)
    response.raise_for_status()
    check_for_redirect(response)
    with open(f'{os.path.join(folder, sanitize_filename(filename))}.txt', 'w', encoding='utf8') as file:
        file.write(response.text)


def download_image(url, folder):
    response = requests.get(url, allow_redirects=True)
    response.raise_for_status()
    check_for_redirect(response)
    filename = urlparse(url).path.replace("//images/", "")
    with open(os.path.join(folder, sanitize_filename(filename)), 'wb') as file:
        file.write(response.content)

if __name__ == '__main__':
    os.makedirs(os.path.join("library files", "books"), exist_ok=True)
    os.makedirs(os.path.join("library files", "images"), exist_ok=True)
    parser = argparse.ArgumentParser(
        description='Программа скачивает книги по их id с tululu.org'
    )
    parser.add_argument('start_id', help='Первый id книги', type=int)
    parser.add_argument('end_id', help='Последний id книги', type=int)
    args = parser.parse_args()
    for book_id in range(args.start_id, args.end_id+1):
        url = f'https://tululu.org/b{book_id}/'
        response = requests.get(url, allow_redirects=True)
        response.raise_for_status()
        try:
            check_for_redirect(response)
            parsed_book = parse_book_page(response)
            print(parsed_book)
            download_text(f'https://tululu.org/txt.php', book_id, parsed_book['book_title'], 'library files/books')
            download_image(parsed_book['book_image'], os.path.join('library files', 'images'))
        except requests.HTTPError:
            print(response.history)
