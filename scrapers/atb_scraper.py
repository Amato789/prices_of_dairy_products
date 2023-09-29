import requests
import random
from .scraper import Scraper
from bs4 import BeautifulSoup
from time import sleep


class AtbScraper(Scraper):
    url = "https://www.atbmarket.com/catalog/315-molochni-produkti"
    source_name = "ATB"

    def scrape(self):
        category_list = self.get_category_list()
        product_list = self.get_product_list(category_list)
        self.save_data(product_list)

    def get_soup(self, url: str) -> BeautifulSoup:
        return BeautifulSoup(requests.get(url, headers=self.headers).text, "lxml")

    def get_category_list(self) -> list:
        soup = self.get_soup(self.url)
        categories = soup.find_all('a', class_="custom-tag__text catalog-subcategory-list__link")
        category_list = []
        for category in categories:
            category_list.append({"name": category.text.strip(), "url": category["href"], "status": False})
        return category_list

    def get_product_list(self, category_list):
        product_list = []
        for category in category_list:
            sleep(random.randrange(2, 4))
            soup = self.get_soup(self.url)
            products = soup.find("div", class_="catalog-list").find_all("article")
            for product in products:
                try:
                    name = product.find("div", class_="catalog-item__title").text.strip()
                except Exception as e:
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
                    product_list.append({"date": self.execution_date,
                                         "category": category["name"],
                                         "name": name,
                                         "current_price": current_price,
                                         "base_price": base_price})
        return product_list
