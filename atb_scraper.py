import requests
from bs4 import BeautifulSoup
from datetime import date
from time import sleep
import random
import json

today_date = date.today()
url = "https://www.atbmarket.com/catalog/315-molochni-produkti"
headers = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
}
req = requests.get(url, headers=headers)
src = req.text
soup = BeautifulSoup(src, "lxml")
categories = soup.find_all('a', class_="custom-tag__text catalog-subcategory-list__link")

categories_list = []
for category in categories:
    categories_list.append({"name": category.text.strip(), "url": category["href"], "status": False})

product_list = []
iteration = 0
error_count = 0
for cat in categories_list:
    url = "https://www.atbmarket.com" + cat["url"]
    req = requests.get(url, headers=headers)
    src = req.text
    soup = BeautifulSoup(src, "lxml")
    products = soup.find("div", class_="catalog-list").find_all("article")

    sleep(random.randrange(2, 4))
    for product in products:
        iteration += 1
        print(iteration)
        category = cat["name"]
        try:
            name = product.find("div", class_="catalog-item__title").text.strip()
        except Exception as e:
            error_count += 1
            name = None
        try:
            current_price = product.find("data", class_="product-price__top").get("value")
        except Exception as e:
            current_price = 0
        try:
            base_price = product.find("data", class_="product-price__bottom").get("value")
        except Exception as e:
            base_price = current_price
        if name:
            product_list.append({"date": today_date.strftime("%d/%m/%Y"),
                                 "category": category,
                                 "name": name,
                                 "current_price": current_price,
                                 "base_price": base_price})

print(f"Scrapping finished with {error_count} errors")

with open(f"data/atb_{today_date}.json", "w") as file:
    json.dump(product_list, file, indent=4, ensure_ascii=False)
