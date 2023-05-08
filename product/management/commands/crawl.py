from distutils.util import execute
from django.core.management.base import BaseCommand
from scrapy.crawler import CrawlerProcess
from scraperr.scraperr.spiders import amazon

import logging
from scrapy.utils.log import configure_logging

class Command(BaseCommand):
    help = 'Crawl Amazon products and store it using djanog models'
    
    def handle(self, *args, **options):
        # Set the logging level for the Scrapy spider
        process = CrawlerProcess(settings={
            'LOG_LEVEL': 'DEBUG',
            'LOG_FILE': 'scrapy.log',
            'DEFAULT_REQUEST_HEADERS' : {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en',
                'accept': '*/*',
                'accept-encoding': 'gzip, deflate, br', 
                'accept-language': 'en-US,en;q=0.9',
                'cookie': 'session-id=260-4273701-4308428; i18n-prefs=EGP; ubid-acbeg=259-8093131-7307554; lc-acbeg=en_AE; session-id-time=2082787201l; session-token=xQcA5bPfPljgDC5khwGaiWa5a+EeM1UUOg+8TSNPcmugbiUVV89YYg7q4gCisw9XtylPsBOMEl9K9Alb+pVvF4ZqXzuKnJSNSeJIQX63T/B9Cpujx9JMd3V/u3xpHzRiCs8i3+U8c/XKlvW36L/0G5KRhDMF6wk6N3jwH0thgClUhweGiO3gPyJ/9NWnfY+7UWaptuyUe3eLZo3juBzgHgjjc7TN07KT6yiDejt/jKo=; csm-hit=tb:s-ACEMZVGHTGZKW120BE3Z|1683569795324&t:1683569796353&adb:adblk_yes',
                'rtt': '50',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.35',
                'x-requested-with':' XMLHttpRequest'
                },
            'ITEM_PIPELINES' : {
                'scraperr.pipelines.ProductPipeline': 300,
                },
            'AUTOTHROTTLE_ENABLED' : True
        })
        process.crawl(amazon.AmazonSpSpider)
        process.start()
