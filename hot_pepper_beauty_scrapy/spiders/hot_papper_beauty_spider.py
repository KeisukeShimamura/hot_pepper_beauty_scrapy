import scrapy
from bs4 import BeautifulSoup
from hot_pepper_beauty_scrapy.items import HotPepperBeautyScrapyItem

class HotPapperBeautySpider(scrapy.Spider):
    name = 'hot_papper_beauty_spider'
    allowed_domains = ['beauty.hotpepper.jp', 'work.salonboard.com']
    start_urls = [
        'https://beauty.hotpepper.jp/work/svcSA/',
        'https://beauty.hotpepper.jp/work/svcSB/',
        'https://beauty.hotpepper.jp/work/svcSC/',
        'https://beauty.hotpepper.jp/work/svcSD/',
        'https://beauty.hotpepper.jp/work/svcSE/',
        'https://beauty.hotpepper.jp/work/svcSF/',
        'https://beauty.hotpepper.jp/work/svcSG/',
        'https://beauty.hotpepper.jp/work/svcSH/',
        'https://beauty.hotpepper.jp/work/svcSI/',
    ]

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')

        job_links = soup.find_all("a", class_="btnSlcViewDetail jscCareerLink")
        for link in job_links:
            yield scrapy.Request(link.get('href'), self.parse_job_page)

        # 次ページへ移動
        next_link = soup.find("li", class_="afterPage").findNext('a')
        yield scrapy.Request(next_link.get('href'), callback=self.parse)

    def parse_job_page(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')

        item = HotPepperBeautyScrapyItem()
        item['サロン名'] = soup.find("p", class_="c-name-salon").get_text()
        item['url'] = response.url
        for head in soup.find_all("dt", class_="c-table__head"):
            if head.get_text() == '勤務地':
                item['勤務地'] = head.next_element.findNext('pre').contents[0]
            elif head.get_text() == '雇用形態':
                item['雇用形態'] = head.next_element.findNext('pre').contents[0]
            elif head.get_text() == '職種':
                item['職種'] = head.next_element.findNext('pre').contents[0]
            elif head.get_text() == '給与':
                item['給与'] = head.next_element.findNext('pre').contents[0]
            elif head.get_text() == '勤務時間':
                item['勤務時間'] = head.next_element.findNext('pre').contents[0]
            elif head.get_text() == '休日':
                item['休日'] = head.next_element.findNext('pre').contents[0]
            elif head.get_text() == '待遇':
                item['待遇'] = head.next_element.findNext('pre').contents[0]
            elif head.get_text() == '教育・研修制度':
                item['教育研修制度'] = head.next_element.findNext('pre').contents[0]
            elif head.get_text() == '求める人物像':
                item['求める人物像'] = head.next_element.findNext('pre').contents[0]
            elif head.get_text() == '応募資格・条件':
                item['応募資格条件'] = head.next_element.findNext('pre').contents[0]
            elif head.get_text() == '会社名':
                item['会社名'] = head.next_element.findNext('pre').contents[0]
            elif head.get_text() == '会社所在地':
                item['会社所在地'] = head.next_element.findNext('pre').contents[0]
            elif head.get_text() == '設立年月日':
                item['設立年月日'] = head.next_element.findNext('pre').contents[0]
            elif head.get_text() == '店舗数':
                item['店舗数'] = head.next_element.findNext('pre').contents[0]

        yield item
