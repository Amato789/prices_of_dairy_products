import json
from abc import ABC, abstractmethod
from datetime import date


class Scraper(ABC):
    url: str
    source_name: str

    def __init__(self):
        self.headers = {
            "Accept": "*/*",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
            Chrome/113.0.0.0 Safari/537.36"
        }
        self.execution_date = date.today().strftime("%d.%m.%Y")

    @abstractmethod
    def scrape(self):
        raise NotImplementedError

    def save_data(self, products_list: list):
        with open(f"data/{self.source_name}_{self.execution_date}.json", "w") as file:
            json.dump(products_list, file, indent=4, ensure_ascii=False)
