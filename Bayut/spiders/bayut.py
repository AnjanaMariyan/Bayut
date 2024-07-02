import scrapy
import re
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from parsel import Selector

class BayutSpider(CrawlSpider):
    name = 'bayut'
    allowed_domains = ['bayut.com']
    start_urls = ['https://www.bayut.com/to-rent/property/dubai/']
    base_url = 'https://www.bayut.com/s/upgraded-properties-rent-dubai/page-{page_number}'
    page_number = 1
    max_pages = 1500
    max_items = 1000 

    
    scraped_items = 0

    rules = (
        Rule(LinkExtractor(allow=r'/property/details-\d+\.html'), callback='parse_property'),
        Rule(LinkExtractor(restrict_css='a._95dd93c1[title="Next"]'), follow=True),
    )

    def parse(self, response):
        selector = Selector(response.text)
        
       
        property_urls = selector.xpath("//a[@aria-label='Listing']/@href").getall()
        for url in property_urls:
            yield scrapy.Request(url, callback=self.parse_property)
            
        
        while self.page_number <= self.max_pages and self.scraped_items < self.max_items:
            url = self.base_url.format(page_number=self.page_number)
            yield scrapy.Request(url, callback=self.parse_next_page)
            self.page_number += 1

    def parse_property(self, response):
        if self.scraped_items >= self.max_items:
            return
        
        selector = Selector(response.text)
        
        
        script_texts = selector.xpath("//script/text()").getall()
        all_script_text = "\n".join(script_texts)
        pattern = r'"permitNumber":"(\d+)"'
        
        property_id = selector.xpath("//span[@aria-label='Reference']/text()").get()
        purpose = selector.xpath("//span[@aria-label='Purpose']/text()").get()
        type_ = selector.xpath("//span[@aria-label='Type']/text()").get()
        added_on = selector.xpath("//span[@aria-label='Reactivated date']/text()").get()
        furnishing = selector.xpath("//span[@class='_2fdf7fc5' and @aria-label='Furnishing']/text()").get()
        currency = selector.xpath("//span[@aria-label='Currency']/text()").get()
        price = selector.xpath("//span[@aria-label='Price']/text()").get()
        location = selector.xpath("//div[@aria-label='Property header']/text()").get()
        bed = selector.xpath("//span[@aria-label='Beds']/span/text()").get()
        bath = selector.xpath("//span[@aria-label='Baths']/span/text()").get()
        size = selector.xpath("//span[@aria-label='Area']/span/span/text()").get()
        permit_numbers = re.findall(pattern, all_script_text)
        permit_number = permit_numbers[0] if permit_numbers else None
        agent_name = selector.xpath('//span//a[@aria-label="Agent name"]/text()').get()
        image_url = selector.xpath("//img[@aria-label='Cover Photo']/@src").get()
        breadcrumb = type_ + " for rent in " + '>'.join(selector.xpath('//div[@aria-label="Breadcrumb"]//span[@class="_43ad44d9"]/text()').extract())
        amenities = selector.xpath('//div[@class="_91c991df"]//span[@class="_7181e5ac"]/text()').getall()
        description = ' '.join(selector.xpath('//div[@aria-label="Property description"]//span[@class="_3547dac9"]//text()').getall())
        

        self.scraped_items += 1
        yield {
            'property_id': property_id,
            'purpose': purpose,
            'type': type_,
            'added_on': added_on,
            'furnishing': furnishing,
            'currency': currency,
            'price': price,
            'location': location,
            'bed': bed,
            'bath': bath,
            'size': size,
            'permit_number': permit_number,
            'agent_name': agent_name,
            'image_url': image_url,
            'breadcrumb': breadcrumb,
            'amenities': amenities,
            'description': description
        }

    def parse_next_page(self, response):
        if self.scraped_items >= self.max_items:
            return
        
        
        pass
