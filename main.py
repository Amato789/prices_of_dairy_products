from scrapers.scraper_factory import ScraperFactory


def handle(scraper_name):
    scraper = ScraperFactory.get_scraper(scraper_name)
    scraper.scrape()


if __name__ == "__main__":
    handle("novus")
