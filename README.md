# Version française

# Programme d'extraction des prix

## Description

Ce script a été conçu pour récupérer des informations sur un site Web qui vend des livres. Il extrait des données telles que les détails du produit, les prix, la disponibilité et les images pour chaque livre dans diverses catégories.

## Exigences

beautifulsoup4==4.12.2  
certificat==2023.7.22  
jeu de caractères-normaliseur==3.3.0  
idna==3.4  
requêtes == 2.31.0  
tamis à soupe ==2,5  
urllib3==2.0.7

Ce script a été testé sur un **environnement Windows** à l'aide de PyCharm.  

Les prérequis sont fournis dans le fichier Requirements.txt.  

Pour obtenir exactement le même environnement de production, vous devez exécuter la commande suivante :

*pip install -r requirements.txt*

## Utilisation

Clonez le dépôt git :

*git clone https://github.com/dogmatus07/PriceSurveySystem.git*

Accédez au répertoire du projet :

*cd PriceSurveySystem*

Exécutez le script :

*python main.py*

Le script commencera à récupérer les données du site Web spécifié.

## Configuration
### Variable page

Mettez à jour la variable page. Cela doit être la page d'accueil de Books.toscrape.com

*page = "https://books.toscrape.com/"*

### Noms des dossiers

Donnez un nom au dossier qui stockera tous les fichiers CSV.

*csv_folder = "csv_files"*

Où *csv_files* est le nom du dossier.

Donnez un nom au dossier qui stockera toutes les images.

*image_folder = "images"*

Où *images* est le nom du dossier.

## Résultats

+ Le script générera un fichier CSV pour chaque catégorie.
+ Chaque fichier CSV contiendra toutes les informations nécessaires sur un livre (titre, UPC, prix, etc.).
+ Tous les fichiers CSV seront stockés dans le dossier précédemment créé (variable : csv_folder).
+ L'image de chaque livre sera téléchargée et stockée dans le dossier précédemment créé (variable : image_folder).
+ Les noms des images ont été nettoyés pour éviter les erreurs lors du téléchargement (pas de caractères spéciaux)
+ Les fichiers CSV utilisent le codage UTF-8-sig et contiennent des en-têtes de colonne.
+ Lorsqu'il y a un bouton suivant (next) dans la page de catégorie, le script le détectera et récupérera des informations supplémentaires si nécessaire

## Remarques

Le script utilise les librairies suivantes :

+ Requests : pour faire des requêtes HTML
+ BeautifulSoup : pour l'analyse HTML
+ urljoin depuis urllib.parse : pour la jonction d'URL
+ CSV : pour gérer les fichiers csv
+ os : pour la gestion des fichiers/dossiers
+ datetime : pour l'horodatage
+ time : pour ajouter time.sleep()

## Clause de non-responsabilité

+ Ce script sera utilisé à des fins éducatives uniquement.
+ Cela ne peut fonctionner que pour la structure du site : books.toscrape.com. Il doit être modifié pour qu'il fonctionne sur un autre site Web.

--------------------------------------------

# English Version

# Price Survey System

## Description

This script is designed to scrape information from a website that sells books for education purpose. It extracts data such as product details, prices, availability, and images for each book in various categories.

## Requirements

beautifulsoup4==4.12.2  
certifi==2023.7.22  
charset-normalizer==3.3.0  
idna==3.4  
requests==2.31.0  
soupsieve==2.5  
urllib3==2.0.7

This script has been tested on a **Windows environment** using PyCharm.

The prerequisites are provided in the requirements.txt file.

To obtain exactly the same production environment, you need to run the following command: 

*pip install -r requirements.txt*

## Usage

Clone the repository:

*git clone https://github.com/dogmatus07/PriceSurveySystem.git*

Navigate to the project directory:

*cd PriceSurveySystem*

Run the script:

*python main.py*

The script will start scraping data from the specified website.

## Configuration
### Page variable
Update the page variable. This has to be the homepage of Books.toscrape.com

*page = "https://books.toscrape.com/"*

### Folder names
Give a name for the folder that will store all CSV files. 

*csv_folder = "csv_files"*

Where *csv_files* here is the name of the folder.

Give a name for the folder that will store all images.

*image_folder = "images"*

## Output

+ The script will generate a CSV file for each category.
+ Each CSV file will contain all necessary informations about a book (title, UPC, price, etc.).
+ All CSV files will be stored inside the previously created folder (variable : csv_folder).
+ Image of every book will be downloaded and stored inside the previously created folder (variable : image_folder).
+ Image names are cleaned to avoid errors when downloading (no special characters)
+ CSV files use UTF-8-sig encoding and contain headers
+ When there's a next button inside category page, the script will detect it and scrape additional informations if needed

## Notes

The script uses the following librairies :

+ Requests : to make HTML requests
+ BeautifulSoup : for HTML parsing
+ urljoin from urllib.parse : for URL joining
+ CSV : for handling csv files
+ os : for file / folder management
+ datetime : for horodatage
+ time : to add time.sleep()

## Disclaimer

+ This script will be used for educational purpose only. 
+ It can only work for the structure of the website : books.toscrape.com. It has to be edited for it to work for another website.