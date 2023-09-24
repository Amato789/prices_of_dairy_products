import json
import requests
from bs4 import BeautifulSoup
from time import sleep
import random
from datetime import date
import math

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
                            "url": category.find("a")["href"],
                            "quantity_of_goods":
                                int(category.find("p", class_="card-first-level__count p3").text.strip())})

product_list = []
iteration = 0

for cat in categories_list:
    goods_per_page = 41
    pages = math.ceil(cat["quantity_of_goods"] / goods_per_page)

    for page in range(1, pages + 1):
        sleep(random.randrange(2, 3))
        iteration += 1
        print(iteration)
        url = "https://novus.online" + cat["url"] + "/page-" + str(page)
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

with open(f"data/novus_{today_date}.json", "w") as file:
    json.dump(product_list, file, indent=4, ensure_ascii=False)
