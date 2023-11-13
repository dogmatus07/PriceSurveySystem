import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv
import os
import datetime


def create_csv_folder(csv_folder):
    if not os.path.exists(csv_folder):
        os.makedirs(csv_folder)
        print("Dossier CSV créé avec succès")
    else:
        print("Folder already exists, nothing created")


def create_image_folder(im_folder):
    if not os.path.exists(im_folder):
        os.makedirs(im_folder)
        print("Dossier image créé avec succès")
    else:
        print("Folder already exists, nothing created")


def get_single_product_infos(book_url):
    print("Récupération des informations pour le livre : ", book_url)
    # getting the html data and parsing it
    page_to_scrap = ""
    try:
        page_to_scrap = requests.get(book_url, timeout=20)
    except requests.exceptions.Timeout:
        print("Requête expirée, erreur Timeout")

    results = {}

    if page_to_scrap:
        soup = BeautifulSoup(page_to_scrap.content, 'html.parser')

        # gathering the data and put them inside variables
        table = soup.find('table', class_="table table-striped")
        category_page = soup.find('ul', class_="breadcrumb")
        category_book = category_page.find_all('li')[2]
        id_description = soup.find('div', id="product_description")
        description = id_description.find_next('p').get_text() if id_description and id_description.find_next(
            'p') else ''
        image_class = soup.find('div', class_='item active')
        image_url = image_class.find('img')['src']
        image_download(image_folder, image_url)  # download image of the book
        results = {
            "product_page_url": book_url,
            "upc": table.find_all('td')[0].get_text(),
            "title": soup.find('h1', class_='').get_text(),
            "price_including_tax": table.find_all('td')[3].get_text(),
            "price_excluding_tax": table.find_all('td')[2].get_text(),
            "number_available": table.find_all('td')[5].get_text(),
            "product_description": description,
            "category": category_book.get_text(strip=True),
            "review_rating": table.find_all('td')[6].get_text(),
            "full_img_url": urljoin(book_url, image_url)
        }
        print("Terminé avec succès")
    else:
        print("Requête annulée, car expirée (timeout)")
    return results


def add_csv_headers(folder, file_name):
    # adding the csv headers
    headers = [
        "product_page_url",
        "upc",
        "title",
        "price_including_tax",
        "price_excluding_tax",
        "number_available",
        "product_description",
        "category",
        "review_rating",
        "full_img_url",
    ]

    file_path = os.path.join(folder, file_name)  # get the path of the file to the csv folder
    with open(file_path, "w", newline="", encoding='utf-8-sig') as file:
        csv_file = csv.writer(file, delimiter=",")
        csv_file.writerow(headers)


def add_to_csv(folder, product_infos, file_name):
    # adding the data inside the list into the csv file
    print("Ajout des informations du livre dans le fichier CSV")

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

    file_path = os.path.join(folder, file_name)

    with open(file_path, "a", newline="", encoding='utf-8-sig') as file:  # a means append here to add the datas
        csv_writer = csv.writer(file, delimiter=",")
        csv_writer.writerow(data)

    print("Informations ajoutées avec succès")
    '''
    # display the content of the csv file
    print("Aperçu du fichier CSV")
    with open("data.csv", "r") as file:
        csv_reader = csv.reader(file, delimiter=",")
        for row in csv_reader:
            print(row)
    print("Fichier CSV mis à jour")
    '''


def get_category_infos(cat_url):  # get all urls from a category page
    # getting the html data and parsing it
    catpage = requests.get(cat_url)
    soup = BeautifulSoup(catpage.content, 'html.parser')

    # getting all the links inside a category
    product_section = soup.find_all("article", class_="product_pod")
    product_urls = []  # put the results inside list
    for product in product_section:
        h3 = product.find('h3')  # the url is inside a h3 tag
        if h3:
            product_url = h3.find('a')['href']  # get the href
            full_url = urljoin(cat_url, product_url)  # get the full url of the product
            product_urls.append(full_url)  # adding the results inside the original list
    return product_urls


def next_status(cat_url):  # testing if there's a next page
    print("Recherche d'une page Next")
    cat_infos = []
    while True:  # iterate as long as these are true
        response = requests.get(cat_url)
        next_content = BeautifulSoup(response.content, 'html.parser')
        cat_infos.extend(
            get_category_infos(cat_url))  # adding the results obtained through the function inside a new list
        next_exists = next_content.select_one("li.next>a")  # testing if there's a next button
        if next_exists:  # if there's a next button
            print("Page Next trouvée, recherche de plus d'informations...")
            next_url = next_exists.get('href')  # get its relative url
            cat_url = urljoin(cat_url, next_url)  # get the full url and update the original caturl object
        else:
            print("Pas de page Next")
            break  # if no next button exist, get out of the loop
    return cat_infos


def scrap_category(cat_url, category_name):
    print("Récupération des URLs des livres de cette catégorie :", cat_url)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S").replace("/", "_")
    category_file_name = f"{category_name}_{timestamp}.csv"
    add_csv_headers(csv_folder, category_file_name)

    product_urls = next_status(cat_url)
    all_product_infos = []

    for product_url in product_urls:
        infos = get_single_product_infos(product_url)
        add_to_csv(csv_folder, infos, category_file_name)
        all_product_infos.append(infos)

    print("Terminé")
    return all_product_infos


def scrap_main(page):
    print("Récupération des URLs de catégories sur :", page)
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
            category_name = a.get_text(strip=True)
            category_urls.append((caturls, category_name))  # create a tuple to store url and its category

    for link, name in category_urls:
        scrap_category(link, name)
    print("Terminé")
    return category_urls


def image_download(image_folder, picture_url):
    print("Téléchargement de l'image :", picture_url)
    r = requests.get(picture_url)
    soup = BeautifulSoup(r.content, 'html.parser')

    image_class = soup.find('div', class_='item active')
    image_src = image_class.find('img')['src']
    image_url = urljoin(picture_url, image_src)
    image_name = image_class.find('img')['alt'].replace(' ', '-').replace('(', '').replace('#', '').replace(')', '')
    image_path = os.path.join(image_folder, image_name)
    with open(image_path + '.jpg', 'wb') as f:
        image = requests.get(image_url)
        f.write(image.content)
    print("Images téléchargées avec succès")
    return image_name, image_url


# main code
csv_folder = "csv_files"
create_csv_folder(csv_folder)
image_folder = "images"
create_image_folder(image_folder)
page = "https://books.toscrape.com/"
scrap_main(page)

# url = "https://books.toscrape.com/catalogue/the-secret-garden_413/index.html"
# print(get_single_product_infos(url))
# caturl = "https://books.toscrape.com/catalogue/category/books/travel_2/index.html"
# scrap_category(caturl)
# image_picture_url = "https://books.toscrape.com/catalogue/the-secret-garden_413/index.html"
# image_download(image_picture_url)
