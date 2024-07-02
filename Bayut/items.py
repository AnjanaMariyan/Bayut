# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Assignment2Item(scrapy.Item):
    property_id = scrapy.Field()
    purpose = scrapy.Field()
    type_ = scrapy.Field()
    added_on = scrapy.Field()
    furnishing = scrapy.Field()
    currency = scrapy.Field()
    price = scrapy.Field()
    location = scrapy.Field()
    bed = scrapy.Field()
    bath = scrapy.Field()
    size = scrapy.Field()
    permit_number = scrapy.Field()
    agent_name = scrapy.Field()
    image_url = scrapy.Field()
    breadcrumb = scrapy.Field()
    amenities = scrapy.Field()
    description = scrapy.Field()

