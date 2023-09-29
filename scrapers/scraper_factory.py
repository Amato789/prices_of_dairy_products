from .novus_scraper import NovusScraper
from .atb_scraper import AtbScraper
from .scraper import Scraper


class ScraperFactory:
    @staticmethod
    def get_scraper(scraper_name) -> Scraper:
        if scraper_name == 'novus':
            return NovusScraper()
        elif scraper_name == 'atb':
            return AtbScraper()
        else:
            raise Exception("Not supported retailer")
