from bs4 import BeautifulSoup
import requests
import pandas as pd
import os


base_url = "https://books.toscrape.com/catalogue/page-{}.html"
books_base_url = "https://books.toscrape.com/catalogue/"

os.makedirs("data_sheet", exist_ok=True)
os.makedirs("images", exist_ok=True)

books = []

def extract_data(soup, page):
    for book in soup.find_all("article", class_ = "product_pod"):
        title = book.h3.a['title']
        price = book.find("p", class_ = "price_color").text
        availability = book.find("p", class_ = "instock availability").text.strip()
        rating_text = book.p['class'][1]
        rating = convert_into_numeric(rating_text)
        link = books_base_url + book.h3.a['href']
        thumbnail_url = "https://books.toscrape.com/" + book.find("img", class_ = "thumbnail")['src']
        thumbnail_file = save_thumbnail_image(thumbnail_url, title)

        books_data = {
            "Title" : title,
            "Price" : price,
            "Availability" : availability,
            "Rating" : rating,
            "Thumbnail URL" : thumbnail_url,
            "Thumbnail File Name" : thumbnail_file
        }

        books.append(books_data)

        print(f"Page: {page}")
        print(f"Title: {title}")
        print(f"Price: {price}")
        print(f"Availability: {availability}")
        print(f"Rating: {rating}")
        print(f"Link: {link}")
        print(f"Thumbnail URL: {thumbnail_url}")
        print(f"Thumbnail File Name: {thumbnail_file}")
        print("-"*60)



def save_thumbnail_image(thumbnail_url, title):
    response = requests.get(thumbnail_url)
    sanitized_title = "".join([char if char.isalnum() else "_" for char in title])
    image_path = os.path.join("images",f"{sanitized_title}.jpg")
    with open(image_path, "wb") as file:
        file.write(response.content)
    return image_path



def convert_into_numeric(rating_text):
    rating_numeric = {
        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5
    }
    return rating_numeric.get(rating_text, 0)


pages = int(input("Enter no. of pages to scrape: "))
for page in range(1,pages+1):
    url = base_url.format(page)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    extract_data(soup, page)
    print(f"Extracted data from Page-{page}")
    
df = pd.DataFrame(books)
df.to_csv('data_sheet/books_data.csv', index=False)
print("Data saved to Data Sheet file")
