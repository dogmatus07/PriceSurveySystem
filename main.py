#importing all necessary packages
import requests
from bs4 import BeautifulSoup
import csv

#getting the html data and parsing it
url = "https://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html"
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

#gathering the informations and put them inside variables
table = soup.find('table', class_="table table-striped")
upc = table.find_all('td')[0]
product_type = table.find_all('td')[1]
price_excluding_tax = table.find_all('td')[2]
price_including_tax = table.find_all('td')[3]
number_available = table.find_all('td')[5]
category_page = soup.find('ul', class_="breadcrumb")
category_book = category_page.find_all('li')[2]
category = category_book.get_text(strip = True)
review_rating = table.find_all('td')[6]
title = soup.find('h1', class_='')
price = soup.find('p', class_='price_color')
stock = soup.find('p', class_='instock availability')
iddesc = soup.find('div', id="product_description")
desc = iddesc.find_next_sibling('p')
#desc_div = soup.find(id='product_description')
#description = desc_div.find_next_sibling('p') #p containing the description have no class nor id .find_next_sibling('p') will find the next p near the id specified in desc_div
print("UPC : " + upc.text.strip())
print("Type de produit : " + product_type.text.strip())
print("Prix HT : " + price_excluding_tax.text.strip())
print("Prix TTC : " + price_including_tax.text.strip())
print("Stock disponible : " + number_available.text.strip())
print("Catégorie : " + category)
print("Nombre d'avis : " + review_rating.text.strip())
print(desc.text.strip())