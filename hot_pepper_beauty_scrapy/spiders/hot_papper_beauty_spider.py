import scrapy
from bs4 import BeautifulSoup
from hot_pepper_beauty_scrapy.items import HotPepperBeautyScrapyItem

class HotPapperBeautySpider(scrapy.Spider):
    name = 'hot_papper_beauty_spider'
    allowed_domains = ['beauty.hotpepper.jp', 'work.salonboard.com']
    start_urls = [
        'https://beauty.hotpepper.jp/work/svcSA/',
        #'https://beauty.hotpepper.jp/work/svcSB/',
        #'https://beauty.hotpepper.jp/work/svcSC/',
        #'https://beauty.hotpepper.jp/work/svcSD/',
        #'https://beauty.hotpepper.jp/work/svcSE/',
        #'https://beauty.hotpepper.jp/work/svcSF/',
        #'https://beauty.hotpepper.jp/work/svcSG/',
        #'https://beauty.hotpepper.jp/work/svcSH/',
        #'https://beauty.hotpepper.jp/work/svcSI/',
    ]

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')

        salon_links = soup.find_all("a", class_="slcHeadLink")
        for link in salon_links:
            # サロンページへ遷移
            yield scrapy.Request(link.get('href'), self.parse_salon_page)

        # 次ページへ移動
        #next_link = soup.find("li", class_="afterPage").findNext('a')
        #yield scrapy.Request(next_link.get('href'), callback=self.parse)

    def parse_salon_page(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')

        item = HotPepperBeautyScrapyItem()
        item['サロン名'] = soup.h1.get_text()
        tel_link = None
        for th in soup.find("table", class_="slnDataTbl").find_all("th"):
            if th.get_text() == '電話番号':
                tel_link = th.next_element.findNext('td').findNext('a')
            elif th.get_text() == '住所':
                item["サロン住所"] = th.next_element.findNext('td').get_text()
            elif th.get_text() == 'アクセス・道案内':
                item["アクセス道案内"] = th.next_element.findNext('td').get_text()
            elif th.get_text() == '営業時間':
                item["営業時間"] = th.next_element.findNext('td').get_text()
            elif th.get_text() == '定休日':
                item["定休日"] = th.next_element.findNext('td').get_text()
            elif th.get_text() == 'クレジットカード':
                item["クレジットカード"] = th.next_element.findNext('td').get_text()
            elif th.get_text() == 'お店のホームページ':
                item["お店のホームページ"] = th.next_element.findNext('td').get_text()
            elif th.get_text() == 'カット価格':
                item["カット価格"] = th.next_element.findNext('td').get_text()
            elif th.get_text() == '席数':
                item["席数"] = th.next_element.findNext('td').get_text()
            elif th.get_text() == 'スタッフ数':
                item["スタッフ数"] = th.next_element.findNext('td').get_text()
            elif th.get_text() == '駐車場':
                item["駐車場"] = th.next_element.findNext('td').get_text()
            elif th.get_text() == 'こだわり条件':
                item["こだわり条件"] = th.next_element.findNext('td').get_text()
            elif th.get_text() == '備考':
                item["備考"] = th.next_element.findNext('td').get_text()

        # 電話番号ページへ
        request = scrapy.Request(tel_link.get('href'), self.parse_tel_page)
        request.meta['item'] = item
        yield request

    def parse_tel_page(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')

        item = response.meta['item']
        item["電話番号"] = soup.find("td").get_text()
        
        # サロンページへ戻る
        salon_link = soup.find("div", class_="title").find("a")
        request = scrapy.Request(salon_link.get('href'), self.parse_salon_page_back)
        request.meta['item'] = item
        yield request

    def parse_salon_page_back(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        item = response.meta['item']

        # 求人ページへ
        job_link = soup.find("a", class_="jscCareerLink")
        request = scrapy.Request(job_link.get('href'), self.parse_job_page)
        request.meta['item'] = item
        yield request

    def parse_job_page(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')

        item = response.meta['item']
        item['求人ページurl'] = response.url
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
