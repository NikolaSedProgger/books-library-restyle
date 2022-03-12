from bs4 import BeautifulSoup
from urllib.parse import urlparse
from pathvalidate import sanitize_filename
import requests
import os
import argparse

def check_for_redirect(response):
    if not response.history:
        return True

def parse_book_page(response):
    soup = BeautifulSoup(response.text, 'lxml').find('table')



    post_image = f"https://tululu.org/{soup.find('td', class_='ow_px_td').find('img')['src']}"
    post_title = soup.find('h1').text.replace('::', '').split('      ')
    post_text = soup.find('div', id='content').find_all('table', class_='d_book')[1].find('td').text
    post_comments = []
    for comment in soup.find_all('div', class_='texts'):
        post_comments.append(comment.find('span', class_='black').text)
    post_genres = []
    for genre in soup.find('span', class_='d_book').find_all('a'):
        post_genres.append(genre.text)
    post = {
        "post_title": post_title[0],
        "post_author": post_title[1],
        "post_text": post_text,
        "post_genres": post_genres,
        "post_comments": post_comments,
        "post_image": post_image,
    }
    return post

def download_text(url, filename, folder):
    response = requests.get(url, allow_redirects=True)
    response.raise_for_status()
    if check_for_redirect(response):
        with open(f'{folder}{sanitize_filename(filename)}.txt', 'w') as file:
            file.write(response.text)

def download_image(url, folder):
    response = requests.get(url, allow_redirects=True)
    response.raise_for_status()
    if check_for_redirect(response):
        filename = urlparse(url).path.replace("//images/", "")
        with open(f'{folder}{sanitize_filename(filename)}', 'wb') as file:
            file.write(response.content) 


if __name__ == '__main__':
    os.makedirs("books", exist_ok=True)
    os.makedirs("images", exist_ok=True)
    
    parser = argparse.ArgumentParser(
        description='Программа скачивает книги по их id с tululu.org'
    )
    parser.add_argument('start_id', help='Первый id книги', type=int)
    parser.add_argument('end_id', help='Последний id книги', type=int)
    args = parser.parse_args()

    for book_id in range(args.start_id, args.end_id):
        url = f'http://tululu.org/b{book_id}/'
        response = requests.get(url)
        response.raise_for_status()



        if check_for_redirect(response):
            post = parse_book_page(response)