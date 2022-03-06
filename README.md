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

### Цель проекта
Проект создан для обучения людей базовым навыкам программирования на Python

