
import pandas as pd
import requests
from bs4 import BeautifulSoup

names_books = []
authors = []
formats = []
prices = []

for page in range(1,10):
    page_request = requests.get(f'https://www.wonderbk.com/shop/books/fiction?page={page}')
    soup = BeautifulSoup(page_request.text, "html.parser")
    tag = soup.find_all('article')
    
    for book in tag:
        names_books.append(book.find("h3"))
        authors.append(book.find_all("p")[0].string)
        formats.append(book.find_all("p")[0].string)
        prices.append(book.find_all("p")[0].string)

books = pd.DataFrame({'Author': authors, 'Formats': formats, 'Price': prices}, index = names_books)
print(books.shape)