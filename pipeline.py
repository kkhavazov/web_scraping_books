import pandas as pd
import requests
from bs4 import BeautifulSoup
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
class wonder_posgres_pipeline():
    def __init__(self, first_page, last_page):
        self.buffer = [] 
        self.batch_size = 1000
        self.first_page = first_page
        self.last_page = last_page
    def get_data(self, current_page):
        page_request = requests.get(f'https://www.wonderbk.com/shop/books/fiction?page={page}')
        soup = BeautifulSoup(page_request.text, "html.parser")
        tag = soup.find_all('article')
        for book in tag:
            names_books.append(str(book.find("h3").string))
            authors.append(str(book.find_all("p")[0].string))
            formats.append(str(book.find_all("p")[0].string))
            prices.append(str(book.find_all("p")[0].string))
            links.append(str(book.find_all('a')[0]['href']))
            
    def process_data(self, current_page):
        data = self.get_data(current_page)
        if len(self.buffer) >= self.batch_size:
            self.flush()
        current_page += 1
    def upload_postgress(self, books):
        try:
            dotenv_path = find_dotenv()
            load_dotenv('.venv/.env')

            password = os.getenv("PASSWORD")
            encoded_password = quote_plus(str(password))
            engine = create_engine(f'postgresql://postgres:{encoded_password}@localhost:5432/wonder_books')
            books.to_sql('books', engine, if_exists='append', index = False)
        except:
            print("Mistake in PostgreSQL. Full error details:")
            traceback.print_exc()
    def flush(self):
        books = pd.DataFrame({'name': names_books, 'author': authors, 'format': formats, 'price': prices, "link": links})
        self.upload_postgres(books)
        self.buffer = []