# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PfassessmentItem(scrapy.Item):

    # the individual data fields that are required:
    notice_title = scrapy.Field()
    notice_text = scrapy.Field()
    category_name = scrapy.Field()
    notice_types = scrapy.Field()
    publish_date = scrapy.Field()
    edition = scrapy.Field()
    notice_id = scrapy.Field()
    notice_code = scrapy.Field()
    company_number = scrapy.Field()
    notice_url = scrapy.Field()
    pass
