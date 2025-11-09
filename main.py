import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup

links = []
for page in range(1,10):
    page_request = requests.get(f'https://www.wonderbk.com/shop/books/fiction?page={page}')
    soup = BeautifulSoup(page_request.text, "html.parser")
    tag = soup.find_all('article')
    
    for l in tag:
        links.append(l.find_all('a')[0]['href'])
print(len(links))