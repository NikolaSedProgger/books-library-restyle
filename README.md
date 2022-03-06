# Tululu python parser
### Как установить
Python3 должен быть уже установлен. Затем используйте `pip` (или `pip3`, есть конфликт с Python2) для установки зависимостей:
```
pip install -r requirements.txt
```
Рекомендуется использовать [virtualenv/venv](https://docs.python.org/3/library/venv.html)

### Как запустить?
Открываем консоль и пишем
```
python main.py Начальное_айди Последнее_айди
```

Начальное айди - id книги с которой начнётся цикл парсинга
Последнее айди - id книги на которой закончится цикл парсинга

После чего начнётся цикл парсинга страниц онлайн-библиотеки [tululu.org](tululu.org)
Вы можете вывести результат, дописав ``` print(post) ```

```python
if check_for_redirect(response):
    post = parse_book_page(response)
    print(post)
```

И получите результат:
```python
{
'post_title': 'Название поста', 
'post_author': 'Автор', 
'post_text': '', 
'post_genres': ['Жанр 1', 'Жанр 2'], 'post_comments': ['Комментарий 1', 'Коментарий 2'], 
'post_image': 'Ссылка на картинку'
}
```
### Дополнительные функции
#### Функция download_text
```
download_text(url, filename, folder)
```
На вход получает:
* Ссылку на книгу
* Ваше название для файла
* Папку (Если её нет, сама создаётся)

Что делает функция:
* Скачивает книгу по ссылке ( ссылку можно получить из post['post_text'])
* Создаёт папку для книг, при необходимости

#### Функция download_image
```
def download_image(url, folder)
```
На вход получает:
* Ссылку на картинку
* Папку (Если её нет, сама создаётся)

Что делает функция:
* Скачивает картинку по ссылке ( ссылку можно получить из post['post_image'])
* Создаёт папку для картинок, при необходимости

### Цель проекта
Проект создан для обучения людей базовым навыкам программирования на Python

