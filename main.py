import requests
import os
from bs4_tutorial import get_post


os.makedirs("books", exist_ok=True)
def check_for_redirect(response):
    if not response.history:
        return True

for book_id in range(10):
    url = f'http://tululu.org/b{book_id}/'
    response = requests.get(url)
    response.raise_for_status()
    
    if check_for_redirect(response):
        print(get_post(response)[1][0])
        for comment in get_post(response)[3]:
            print(comment)     



for id in range(10):
    url = f"http://tululu.org/txt.php?id={id+1}"
    response = requests.get(url, allow_redirects=True)
    response.raise_for_status() 
    filename = f'id{id+1}.txt'
    if check_for_redirect(response):
        with open(f'books/{filename}', 'w') as file:
            file.write(response.text)