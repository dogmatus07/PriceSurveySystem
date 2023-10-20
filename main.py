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

url = "https://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html"
product_infos = get_single_product_infos(url)
for key, value in product_infos.items():
    print(f"{key} : {value}")

'''#creating the csv file and adding the headers
headers = ["Titre", "Type de Livre", "UPC", "Prix HT","Prix TTC", "Stock", "Description"] #creating the headers of the csv file
with open("data.csv", "w", newline="") as file:
  csv_file = csv.writer(file, delimiter =",")
  csv_file.writerow(headers)

#specifying the list containing all the informations about the product
product_data = [title.text.strip(), product_type.text.strip(), upc.text.strip(), price_excluding_tax.text.strip(), price_including_tax.text.strip(), stock.text.strip(), desc.text.strip()]

#adding the informations inside the list into the csv file
with open("data.csv", "a", newline = "") as file: #a means append here to add the informations
  csv_writer = csv.writer(file, delimiter =",")
  csv_writer.writerow(product_data)

#display the content of the csv file
with open("data.csv", "r") as file : #r means read as we want to read and display what's inside the csv file
  csv_reader = csv.reader(file, delimiter =",")
  for row in csv_reader:
    print(row)'''