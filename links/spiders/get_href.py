# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import HtmlResponse
from lxml import html
import sys
import cfscrape
import re

from links.items import Info

l1 = []
with open("~/python_projects/venv/python36/sch_br_links/links/cities3.txt", "rt") as f:
  for name in f.readlines():
    city = name.replace("\n", '')
    l1.append("https://www.melhorescola.com.br/escola/busca?municipio={}&omni=&bairro=&redes=privada&series=&bairros=&sort=&mensalidadeMax=&mensalidadeMin=".format(city))

class SchoolLinks(CrawlSpider):
  name = "get_href"
  allowed_domains = ["melhorescola.com.br"]
  start_urls = l1
  rules = (Rule(LinkExtractor(allow=(), restrict_xpaths=("//a[contains(@class, 'page-link')]",)), callback="parse_page", follow=True),)

  def parse_page(self, response):
    site = html.fromstring(response.body_as_unicode())
    item = Info()
    scraper = cfscrape.create_scraper()
    for href in site.xpath("//div[contains(@class, 'col-12 col-md6 col-lg-6 card-search-item')]/a[contains(@class, 'card-link')]//@href"):
      try:
        body = scraper.get(href).content
        body2 = body.decode("utf-8")
        resp = HtmlResponse(url=href, body=body)
        title = "".join(resp.css("title::text").extract())
        name = title.split('-')[0]
        item = Info()
        s = str(body2)
        item["school_name"] = name
        #item["school_name"] = resp.xpath("//h1[contains(@class, 'h4 white')]/text()").extract()
        street_address = re.compile(r'"streetAddress":"(.*)"\n')
        item["street_address"] = street_address.findall(s)
        address_locality = re.compile(r'"addressLocality":"(.*)",\n')
        item["address_locality"] = address_locality.findall(s)
        address_region = re.compile(r'"addressRegion":"(.*)",\n')
        item["address_region"] = address_region.findall(s)
        postal_code = re.compile(r'"postalCode":"(.*)",\n')
        item["postal_code"] = postal_code.findall(s)
        address_email = re.compile(r'"email":"(.*)",\n')
        item["address_email"] = address_email.findall(s)
        telephone = re.compile(r'"telephone":"(.*)",\n')
        item["telephone"] = telephone.findall(s)
        childrens_education = re.compile(r'<p class="grey">Ensino Infantil: <strong class="orange">(\d+)')
        item["childrens_education"] = childrens_education.findall(s)
        elementary_school1 = re.compile(r'<p class="grey">Fundamental I: <strong class="orange">(\d+)')
        item["elementary_school1"] = elementary_school1.findall(s)
        elementary_school2 = re.compile(r'<p class="grey">Fundamental II: <strong class="orange">(\d+)')
        item["elementary_school2"] = elementary_school2.findall(s)
        high_school = re.compile(r'<p class="grey">Ensino Médio: <strong class="orange">(\d+)')
        item["high_school"] = high_school.findall(s)
        ce_value = re.compile(r'<p class="grey">Ensino Infantil: <strong class="orange">R\$ (\d+,\d+)')
        item["childrens_education_cost"] = ce_value.findall(s)
        es_value = re.compile(r'<p class="grey">Ensino Fundamental: <strong class="orange">R\$ (\d+,\d+)')
        item["elementary_school_cost"] = es_value.findall(s)
        hs_value = re.compile(r'<p class="grey">Ensino Médio: <strong class="orange">R\$ (\d+,\d+)')
        item["high_school_cost"] = hs_value.findall(s)
        yield item
      except Exception as e:
        print("\n\n{}\nError on line: {}\n\n".format(e, sys.exc_info()[-1].tb_lineno))
        continue





