import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv
import os


def get_single_product_infos(url):
    print("Getting single product informations")
    # getting the html data and parsing it
    try:
        page = requests.get(url, timeout=10)
    except requests.exceptions.Timeout:
        print("Requête expirée")
    soup = BeautifulSoup(page.content, 'html.parser')

    # gathering the informations and put them inside variables
    table = soup.find('table', class_="table table-striped")
    category_page = soup.find('ul', class_="breadcrumb")
    category_book = category_page.find_all('li')[2]
    iddesc = soup.find('div', id="product_description")
    desc_element = iddesc.find_next('p')
    im = soup.find('div', class_='item active')
    image_url = im.find('img')['src']
    results = {
        "product_page_url": url,
        "upc": table.find_all('td')[0].get_text(),
        "title": soup.find('h1', class_='').get_text(),
        "price_including_tax": table.find_all('td')[3].get_text(),
        "price_excluding_tax": table.find_all('td')[2].get_text(),
        "number_available": table.find_all('td')[5].get_text(),
        "product_description": desc_element.get_text() if desc_element else '',
        "category": category_book.get_text(strip=True),
        "review_rating": table.find_all('td')[6].get_text(),
        "full_img_url": urljoin(url, image_url)
    }
    print("Getting single product informations - Success")
    return results


def imgdown(url):
    print("Downloading images")
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    im = soup.find('div', class_='item active')
    image_url = im.find('img')['src']
    image_link = urljoin(url, image_url)
    name = im.find('img')['alt'].replace(' ', '-').replace('(', '').replace('#', '').replace(')', '')
    with open(name + '.jpg', 'wb') as f:
        image = requests.get(image_link)
        f.write(image.content)
    print("Downloading images success")
    return name, image_link


def add_csv_headers(product_infos):
    # adding the csv headers
    headers = list(product_infos.keys())  # creating the headers of the csv file
    with open("data.csv", "w", newline="") as file:
        csv_file = csv.writer(file, delimiter=",")
        csv_file.writerow(headers)


def add_to_csv(product_infos):
    print("Adding informations to a CSV file")
    # adding the informations inside the list into the csv file
    # writing the headers of the csv file
    print("Adding the product informations into the CSV file")

    data = [
        product_infos["product_page_url"],
        product_infos["upc"],
        product_infos["title"],
        product_infos["price_including_tax"],
        product_infos["price_excluding_tax"],
        product_infos["number_available"],
        product_infos["product_description"],
        product_infos["category"],
        product_infos["review_rating"],
        product_infos["full_img_url"],
    ]

    with open("data.csv", "a", newline="") as file:  # a means append here to add the informations
        csv_writer = csv.writer(file, delimiter=",")
        csv_writer.writerow(data)
    print("Product informations added to the CSV file")

    # display the content of the csv file
    print("Overview of the content of CSV file")
    with open("data.csv", "r") as file:
        csv_reader = csv.reader(file, delimiter=",")
        for row in csv_reader:
            print(row)
    print("Adding informations to CSV : success")


def get_category_infos(caturl):  # get all urls from a category page
    print("Getting all product URLS from category page")
    # getting the html data and parsing it
    catpage = requests.get(caturl)
    soup = BeautifulSoup(catpage.content, 'html.parser')

    # getting all the links inside a category
    product_section = soup.find_all("article", class_="product_pod")
    product_urls = []  # put the results inside list
    for product in product_section:
        h3 = product.find('h3')  # the url is inside a h3 tag
        if h3:
            product_url = h3.find('a')['href']  # get the href
            full_url = urljoin(caturl, product_url)  # get the full url of the product
            product_urls.append(full_url)  # adding the results inside the original list
    print("Getting all product URLS from category page : success")
    return product_urls


def next_status(caturl):  # testing if there's a next page
    print("Test if there's a next page")
    cat_infos = []
    while True:  # iterate as long as these are true
        response = requests.get(caturl)
        next_content = BeautifulSoup(response.content, 'html.parser')
        cat_infos.extend(
            get_category_infos(caturl))  # adding the results obtained through the function inside a new list
        get_next = next_content.select_one("li.next>a")  # testing if there's a next button
        if get_next:  # if there's a next button
            print("Next page found")
            next_url = get_next.get('href')  # get its relative url
            caturl = urljoin(caturl, next_url)  # get the full url and update the original caturl object
        else:
            print("No next page")
            break  # if no next button exist, get out of the loop
    return cat_infos


def scrap_category(cat_url):
    print("Getting all informations from category URL")
    product_urls = next_status(cat_url)
    product_info = {}

    # getting the csv headers
    one_product = get_single_product_infos(product_urls[0]) # get the infos from 1 product to get the keys
    add_csv_headers(one_product) # write the keys as headers

    for url in product_urls:
        infos = get_single_product_infos(url)
        product_info.update(infos)
        add_to_csv(product_info)
    print("Getting all informations from category URL : Success")
    return product_info


def scrap_main(page):
    print("Finding all category urls on the homepage")
    r = requests.get(page)
    soup = BeautifulSoup(r.content, 'html.parser')
    cat = soup.find('ul', class_='nav nav-list')
    li_items = cat.find_all('li')[1:]  # avoid to get the Books url which is a page for all books
    category_urls = []
    for li in li_items:
        atags = li.find_all('a')
        for a in atags:
            href = a.get('href')
            caturls = urljoin(page, href)
            category_urls.append(caturls)
    print("Finding all category urls on the homepage : success")
    return category_urls

# main code
page = "https://books.toscrape.com/"
caturl = scrap_main(page)
for link in caturl:
    scrap_category(link)

#url ="https://books.toscrape.com/catalogue/its-only-the-himalayas_981/index.html"
#get_single_product_infos(url)
# caturl = "https://books.toscrape.com/catalogue/category/books/travel_2/index.html"
# scrap_category(caturl)
