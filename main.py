import requests
import urllib
import os

os.makedirs("books", exist_ok=True)


for id in range(10):
    url = f"http://tululu.org/txt.php?id={id+1}"
    response = requests.get(url)
    response.raise_for_status() 
    filename = f'id{id+1}.txt'
    if '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"' not in response.text:
        with open(f'books/{filename}', 'w') as file:
            file.write(response.text)