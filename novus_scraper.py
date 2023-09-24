import requests
from bs4 import BeautifulSoup
from time import sleep
import random
from datetime import date

today_date = date.today()
url = "https://novus.online/category/molocne-ajca-sir"
headers = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
    Chrome/113.0.0.0 Safari/537.36"
}

req = requests.get(url, headers=headers)
src = req.text
soup = BeautifulSoup(src, "lxml")
categories = soup.find_all("div", class_="subcategories-list__item")
categories_list = []
for category in categories:
    categories_list.append({"category_name": category.find("span").text.strip(),
                            "url": category.find("a")["href"]})

product_list = []

for cat in categories_list:
    sleep(random.randrange(2, 4))
    url = "https://novus.online" + cat["url"]
    req = requests.get(url, headers=headers)
    src = req.text
    soup = BeautifulSoup(src, "lxml")
    products = soup.find_all("a", class_="base-is-link base-card catalog-products__item")

    for product in products:
        category = cat["category_name"]
        name = " ".join(product.find("p", class_="base-card__label regular p2").text.split())
        try:
            current_price = product.find("p", class_="base-card__price-current").text.strip()
        except Exception as e:
            current_price = 0
        try:
            base_price = product.find("p", class_="base-card__price-old p3").text.strip()
        except Exception as e:
            base_price = current_price
        product_list.append({"date": today_date.strftime("%d/%m/%Y"),
                             "category": category,
                             "name": name,
                             "current_price": current_price,
                             "base_price": base_price})
print(product_list)
