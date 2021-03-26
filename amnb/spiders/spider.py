import scrapy

from scrapy.loader import ItemLoader

from ..items import AmnbItem
from itemloaders.processors import TakeFirst


class AmnbSpider(scrapy.Spider):
	name = 'amnb'
	start_urls = ['https://www.amnb.com/blog']

	def parse(self, response):
		post_links = response.xpath('//div[@class="card-body content"]//a[@data-link-type-id="page"]')
		for post in post_links:
			url = post.xpath('./@href').get()
			date = post.xpath('./text()').get()
			yield response.follow(url, self.parse_post, cb_kwargs={'date': date})

	def parse_post(self, response, date):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//div[@class="subpage-content"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()

		item = ItemLoader(item=AmnbItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
