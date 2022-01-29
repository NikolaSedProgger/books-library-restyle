from tkinter.messagebox import NO
from bs4 import BeautifulSoup
import requests
from pathvalidate import sanitize_filename
from main import check_for_redirect


def get_post(book_id):
    url = f'http://tululu.org/b{book_id}/'
    response = requests.get(url)
    response.raise_for_status()
    
    if check_for_redirect(response):
        soup = BeautifulSoup(response.text, 'lxml')

        post_image = f"https://tululu.org/{soup.find('table').find('td', class_='ow_px_td').find('img')['src']}"
        post_title = soup.find('table').find('h1').text.replace('::', '').split('      ')
        post_text = soup.find('table').find('div', id='content').find_all('table', class_='d_book')[1].find('td').text
        return post_image, post_title, post_text

def download_txt(url, filename, folder='books/'):
    response = requests.get(url, allow_redirects=True)
    response.raise_for_status()
    if check_for_redirect(response):
        with open(f'{folder + sanitize_filename(filename)}.txt', 'w') as file:
            file.write(response.text)

for book_id in range(1, 11):
    url = f"http://tululu.org/txt.php?id={book_id}"
    try:
        download_txt(url, get_post(book_id)[1][0])
    except:
        None