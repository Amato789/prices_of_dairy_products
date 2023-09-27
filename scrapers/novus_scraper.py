import requests
import math
import random
from bs4 import BeautifulSoup
from .scraper import Scraper
from time import sleep


class NovusScraper(Scraper):
    GOODS_PER_PAGE = 41
    url = "https://novus.online/category/molocne-ajca-sir"
    source_name = "Novus"

    def scrape(self):
        categories_list = self.get_categories_list()
        products_list = []
        for category in categories_list:
            products_list += self.get_products_list(category)
        self.save_data(products_list)

    def get_soup(self, url: str) -> BeautifulSoup:
        return BeautifulSoup(requests.get(url, headers=self.headers).text, "lxml")

    def get_categories_list(self) -> list:
        soup = self.get_soup(self.url)
        categories = soup.find_all("div", class_="subcategories-list__item")
        categories_list = []
        for category in categories:
            categories_list.append({
                "category_name": category.find("span").text.strip(),
                "url": category.find("a")["href"],
                "quantity_of_goods": int(category.find("p", class_="card-first-level__count p3").text.strip())
            })
        return categories_list

    def get_products_list(self, category: dict) -> list:
        products_list = []
        pages_per_category = math.ceil(category["quantity_of_goods"] / self.GOODS_PER_PAGE)
        for page in range(1, pages_per_category + 1):
            sleep(random.randrange(2, 3))
            soup = self.get_soup("https://novus.online" + category["url"] + "/page-" + str(page))
            products = soup.find_all("a", class_="base-is-link base-card catalog-products__item")
            for product in products:
                product_name = " ".join(product.find("p", class_="base-card__label regular p2").text.split())
                try:
                    current_price = product.find("p", class_="base-card__price-current").text.strip()
                except Exception as e:
                    current_price = 0
                try:
                    base_price = product.find("p", class_="base-card__price-old p3").text.strip()
                except Exception as e:
                    base_price = current_price
                products_list.append({"date": self.execution_date,
                                      "category": category["category_name"],
                                      "product": product_name,
                                      "current_price": current_price,
                                      "base_price": base_price})
        return products_list
