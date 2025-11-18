import pandas as pd
import requests
from bs4 import BeautifulSoup
import psycopg2
from sqlalchemy import create_engine
from urllib.parse import quote_plus
import traceback
from dotenv import load_dotenv, find_dotenv
import os

names_books = []
authors = []
formats = []
prices = []
links = []
current = 3867

for page in range(1):
    page_request = requests.get(f'https://www.wonderbk.com/shop/books/fiction?page={page}')
    soup = BeautifulSoup(page_request.text, "html.parser")
    tag = soup.find_all('article')
    
    for book in tag:
        names_books.append(str(book.find("h3").string))
        authors.append(str(book.find_all("p")[0].string))
        formats.append(str(book.find_all("p")[0].string))
        prices.append(str(book.find_all("p")[0].string))
        links.append(str(book.find_all('a')[0]['href']))
try:
    books = pd.DataFrame({'name': names_books, 'author': authors, 'format': formats, 'price': prices, "link": links})

    dotenv_path = find_dotenv()
    load_dotenv('.venv/.env')

    password = os.getenv("PASSWORD")
    encoded_password = quote_plus(str(password))
    engine = create_engine(f'postgresql://postgres:{encoded_password}@localhost:5432/wonder_books')
    books.to_sql('books', engine, if_exists='append', index = False)
except:
    print("Mistake in PostgreSQL. Full error details:")
    traceback.print_exc()