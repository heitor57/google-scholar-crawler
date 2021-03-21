from scrapy.http import Request
import traceback
import scrapy

class SearchSpider(scrapy.Spider):
    name = "search"
    css_rules = {
            'title': '.gs_rt a *::text',
            'url': '.gs_rt a::attr(href)',
            # 'related-text': '.gs_ggsS::text',
            # 'related-type': '.gs_ggsS .gs_ctg2::text',
            'related-url': '.gs_ggs a::attr(href)',
            # 'citation-text': '.gs_fl > a:nth-child(1)::text',
            'citation-url': '.gs_fl > a:nth-child(1)::attr(href)',
            # 'authors': '.gs_a a::text',
            'description': '.gs_rs ::text',
            'authors-publicator-domain': '.gs_a ::text',
    }
    def __init__(self, *args, **kwargs): 
      super().__init__(*args, **kwargs) 

      self.start_urls = [kwargs.get('start_url')] 

    def parse(self, response):
        # page = response.url.split("/")[-2]

        for article in response.css('.gs_r.gs_or.gs_scl'):
            data = dict()
            for k, v in self.css_rules.items():
                data[k]=''.join(article.css(v).getall())
                if k == 'authors-publicator-domain':
                    try:
                        split_data = data[k].split('-')
                        data['authors']= split_data[0]
                        data['publicator']= split_data[1].split(',')[0]
                        data['year']= int(split_data[1].split(',')[1])
                        data['domain']= split_data[2]
                    except:
                        traceback.print_exc()
                        raise SystemExit
            yield data

            # print(data)
        # num_docs = len(data[list(data.keys())[0]])
        # docs = [dict() for i in range(num_docs)]
        # for i in range(num_docs):
            # for key in data.keys():
                # print(data[key])
                # print(i)
                # docs[i] = data[key][i]
        


        for url in response.css('#gs_n a::attr(href)').getall():
            yield Request(response.urljoin(url),self.parse)
        # filename = f'quotes-{page}.html'
        # with open(filename, 'wb') as f:
            # f.write(response.body)
        # self.log(f'Saved file {filename}')
