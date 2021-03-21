from scrapy.http import Request
import traceback
import scrapy

class SearchSpider(scrapy.Spider):
    name = "search"
    css_rules = {
            'title': '.gs_rt a *::text',
            'url': '.gs_rt a::attr(href)',
            'related-url': '.gs_ggs a::attr(href)',
            'citation-url': '.gs_fl > a:nth-child(1)::attr(href)',
            'abstract': '.gs_rs ::text',
            'authors-publicator-domain': '.gs_a ::text',
    }
    def __init__(self, *args, **kwargs): 
      super().__init__(*args, **kwargs) 

      self.start_urls = [kwargs.get('start_url')] 

    def parse(self, response):

        for article in response.css('.gs_r.gs_or.gs_scl'):
            data = dict()
            for k, v in self.css_rules.items():
                data[k]=''.join(article.css(v).getall())
                if k == 'authors-publicator-domain':
                    try:
                        split_data = data[k].split('-')
                        data['authors']= split_data[0]
                        data['publicator']= split_data[1].split(',')[0]
                        try:
                            data['year']= int(split_data[1].split(',')[1])
                        except:
                            traceback.print_exc()
                        data['domain']= split_data[2]
                    except:
                        traceback.print_exc()
            yield data

        for url in response.css('#gs_n a::attr(href)').getall():
            yield Request(response.urljoin(url),self.parse)
