import requests
from bs4 import BeautifulSoup
import pandas as pd

base_url = "http://books.toscrape.com/catalogue/page-{}.html"
data = []

for page in range(1, 6):  # scrape first 5 pages
    url = base_url.format(page)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    books = soup.find_all("article", class_="product_pod")

    for book in books:
        title = book.h3.a["title"]
        price = book.find("p", class_="price_color").text
        availability = book.find("p", class_="instock availability").text.strip()

        data.append([title, price, availability, page])

df = pd.DataFrame(data, columns=["Title", "Price", "Availability", "Page"])

df.to_csv("jobs_data.csv", index=False)

print("Scraping completed. CSV file created successfully.")