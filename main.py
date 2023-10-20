#importing all necessary packages
import requests
from bs4 import BeautifulSoup
import csv

def get_single_product_infos(url):
    #getting the html data and parsing it
    link = url
    page = requests.get(link)
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
    stock = soup.find('p', class_='instock availability').text.strip()
    iddesc = soup.find('div', id="product_description")
    desc = iddesc.find_next_sibling('p').get_text()
    return {"title": title.text.strip(), "product_type": product_type.text.strip(), "upc": upc.text.strip(), "price_excluding_tax": price_excluding_tax.text.strip(), "price_including_tax": price_including_tax.text.strip(), "stock": stock.strip(), "description": desc}

def addtocsv(product_infos):
    #creating the csv file and adding the headers
    headers = list(product_infos.keys()) #creating the headers of the csv file
    with open("data.csv", "w", newline="") as file:
      csv_file = csv.writer(file, delimiter =",")
      csv_file.writerow(headers)

    #adding the informations inside the list into the csv file
    with open("data.csv", "a", newline = "") as file: #a means append here to add the informations
      csv_writer = csv.writer(file, delimiter =",")
      csv_writer.writerow([
        product_infos["title"],
        product_infos["product_type"],
        product_infos["upc"],
        product_infos["price_excluding_tax"],
        product_infos["price_including_tax"],
        product_infos["stock"],
        product_infos["description"]
      ])

    #display the content of the csv file
    with open("data.csv", "r") as file :
      csv_reader = csv.reader(file, delimiter =",")
      for row in csv_reader:
        print(row)

url = "https://books.toscrape.com/catalogue/forever-and-forever-the-courtship-of-henry-longfellow-and-fanny-appleton_894/index.html"
product_infos = get_single_product_infos(url)
addtocsv(product_infos)
