from tkinter.messagebox import NO
from turtle import pos
from bs4 import BeautifulSoup
import requests
from pathvalidate import sanitize_filename
import os
from urllib.parse import urlparse

os.makedirs("books", exist_ok=True)
os.makedirs("images", exist_ok=True)

def check_for_redirect(response):
    if not response.history:
        return True

def parse_book_page(response):
    soup = BeautifulSoup(response.text, 'lxml')

    post_image = f"https://tululu.org/{soup.find('table').find('td', class_='ow_px_td').find('img')['src']}"
    post_title = soup.find('table').find('h1').text.replace('::', '').split('      ')
    post_text = soup.find('table').find('div', id='content').find_all('table', class_='d_book')[1].find('td').text
    post_comments = []
    for comment in soup.find('table').find_all('div', class_='texts'):
        post_comments.append(comment.find('span', class_='black').text)
    post_genres = []
    for genre in soup.find('table').find('span', class_='d_book').find_all('a'):
        post_genres.append(genre.text)
    post = {
        "post_title": post_title,
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
        with open(f'{folder + sanitize_filename(filename)}', 'w') as file:
            file.write(response.text)

def download_image(url, folder):
    response = requests.get(url, allow_redirects=True)
    response.raise_for_status()
    if check_for_redirect(response):
        filename = urlparse(url).path.replace("//images/", "")
        with open(f'{folder + sanitize_filename(filename)}', 'wb') as file:
            file.write(response.content) 


for book_id in range(10):
    url = f'http://tululu.org/b{book_id}/'
    response = requests.get(url)
    response.raise_for_status()
    
    if check_for_redirect(response):
        print(parse_book_page(response)['post_genres'])

