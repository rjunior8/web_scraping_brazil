# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class LinksPipeline(object):
    def process_item(self, item, spider):
        return item

"""from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from scrapy.exporters import CsvItemExporter

class LinksPipeline(object):

	def __init__(self):
		dispatcher.connect(self.spider_opened, signals.spider_opened)
		dispatcher.connect(self.spider_closed, signals.spider_closed)
		self.files = {}

	def spider_opened(self, spider):
		arq = open("{}_ads.csv".format(spider.name), "w+b")
		self.files[spider] = arq
		self.exporter = CsvItemExporter(arq)
		self.exporter.start_exporting()

	def spider_closed(self, spider):
		self.exporter.finish_exporting()
		arq = self.files.pop(spider)
		arq.close()

	def process_item(self, item, spider):
		self.exporter.export_item(item)
		return item"""


