import scrapy

import mm.items


class mmSp(scrapy.Spider):

    name = "mm"
    allowed_domains = ["www.mm131.com"]
    start_urls = [
        'http://www.mm131.com/xinggan/',
                  # 'http://www.mm131.com/qingchun/',
                  # 'http://www.mm131.com/xiaohua/',
                  # 'http://www.mm131.com/chemo/',
                  # 'http://www.mm131.com/qipao/',
                  # 'http://www.mm131.com/mingxing/'
                  ]

    def parse(self, response):
        list = response.css('.list-left dd:not(.page)')
        for img in list:
            imgname = img.css('a ::text').extract_first()
            imgurl = img.css('a ::attr(href)').extract_first()
            print('imgname:'+imgname+'\t''imgurl:'+str(imgurl)+'\n')
            next_url = response.css(".page-en:nth-last-child(2)::attr(href)").extract_first()

            print("@@@@@@@@@@"+next_url)
            if next_url is not None:
                yield response.follow(next_url, callback=self.parse)
            yield scrapy.Request(imgurl, callback=self.content)

    def content(self, response):
        item = mm.items.MmItem()
        item['name'] = response.css(".content h5::text").extract_first()
        item['url'] = response.css(".content-pic img::attr(src)").extract()
        item['referer'] = response.url
        yield item

        # 提取图片,存入文件夹
        # print(item['ImgUrl'])
        next_url = response.css(".page-ch:last-child::attr(href)").extract_first()

        if next_url is not None:
            # 下一页
            yield response.follow(next_url, callback=self.content)