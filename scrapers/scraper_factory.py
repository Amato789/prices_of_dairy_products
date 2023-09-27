from .novus_scraper import NovusScraper
from .scraper import Scraper


class ScraperFactory:
    @staticmethod
    def get_scraper(scraper_name) -> Scraper:
        if scraper_name == 'novus':
            return NovusScraper()
        else:
            raise Exception("Not supported retailer")
