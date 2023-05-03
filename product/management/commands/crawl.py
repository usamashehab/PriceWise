from django.core.management.base import BaseCommand
from scrapy.crawler import CrawlerProcess
from scraperr.scraperr.spiders import amazon

class Command(BaseCommand):
    help = 'Crawl Amazon products and store it using djanog models'

    def handle(self, *args, **options):
        process = CrawlerProcess()
        process.crawl(amazon.AmazonSpSpider)
        process.start()
        # execute(['scrapy', 'crawl', 'amazon'])
