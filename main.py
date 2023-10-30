import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv
def get_single_product_infos(url):
    #getting the html data and parsing it
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
    stock = soup.find('p', class_='instock availability').text.strip()
    iddesc = soup.find('div', id="product_description")
    desc_element = iddesc.find_next('p')
    desc = desc_element.get_text() if desc_element else ''
    return {"title": title.text.strip(), "product_type": product_type.text.strip(), "upc": upc.text.strip(), "price_excluding_tax": price_excluding_tax.text.strip(), "price_including_tax": price_including_tax.text.strip(), "stock": stock.strip(), "description": desc}

'''
def addcsvheaders(product_infos) :
    # adding the csv headers
    headers = list(product_infos.keys())  # creating the headers of the csv file
    with open("data.csv", "w", newline="") as file:
        csv_file = csv.writer(file, delimiter=",")
        csv_file.writerow(headers)
'''
def addtocsv(product_infos):
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

def getcategory_infos(caturl): #get all urls from a category page
    #getting the html data and parsing it
    catpage = requests.get(caturl)
    soup = BeautifulSoup(catpage.content, 'html.parser')

    # getting all the links inside a category
    product_section = soup.find_all("article", class_="product_pod")
    product_urls = []  # put the results inside list
    for product in product_section:
        h3 = product.find('h3')  # the url is inside a h3 tag
        if h3:
            product_url = h3.find('a')['href']  # get the href
            full_url = urljoin(caturl, product_url) # get the full url of the product
            product_urls.append(full_url) #adding the results inside the original list
    return product_urls

def next_status(caturl): #testing if there's a next page
    cat_infos = []
    while True: # iterate as long as these are true
        response = requests.get(caturl)
        next_content = BeautifulSoup(response.content, 'html.parser')
        cat_infos.extend(getcategory_infos(caturl)) #adding the results obtained through the function inside a new list
        get_next = next_content.select_one("li.next>a") #testing if there's a next button
        if get_next: #if there's a next button
            next_url = get_next.get('href') #get its relative url
            caturl = urljoin(caturl, next_url) #get the full url and update the original caturl object
        else:
            break #if no next button exist, get out of the loop
    return cat_infos

# main function
caturl = "https://books.toscrape.com/catalogue/category/books/mystery_3/index.html"
product_urls = next_status(caturl)
for url in product_urls:
    product_info = get_single_product_infos(url)
    addtocsv(product_info)

