import scrapy
from bs4 import BeautifulSoup
from hot_pepper_beauty_scrapy.items import HotPepperBeautyScrapyItem

class HotPapperBeautySpider(scrapy.Spider):
    name = 'hot_papper_beauty_spider'
    allowed_domains = ['beauty.hotpepper.jp', 'work.salonboard.com']
    start_urls = [
        'https://beauty.hotpepper.jp/pre01/',
        'https://beauty.hotpepper.jp/pre02/',
        'https://beauty.hotpepper.jp/pre03/',
        'https://beauty.hotpepper.jp/pre04/',
        'https://beauty.hotpepper.jp/pre05/',
        'https://beauty.hotpepper.jp/pre06/',
        'https://beauty.hotpepper.jp/pre07/',
        'https://beauty.hotpepper.jp/pre08/',
        'https://beauty.hotpepper.jp/pre09/',
        'https://beauty.hotpepper.jp/pre10/',
        #'https://beauty.hotpepper.jp/pre11/',
        #'https://beauty.hotpepper.jp/pre12/',
        #'https://beauty.hotpepper.jp/pre13/',
        #'https://beauty.hotpepper.jp/pre14/',
        'https://beauty.hotpepper.jp/pre15/',
        'https://beauty.hotpepper.jp/pre16/',
        'https://beauty.hotpepper.jp/pre17/',
        'https://beauty.hotpepper.jp/pre18/',
        'https://beauty.hotpepper.jp/pre19/',
        'https://beauty.hotpepper.jp/pre20/',
        'https://beauty.hotpepper.jp/pre21/',
        'https://beauty.hotpepper.jp/pre22/',
        'https://beauty.hotpepper.jp/pre23/',
        'https://beauty.hotpepper.jp/pre24/',
        'https://beauty.hotpepper.jp/pre25/',
        'https://beauty.hotpepper.jp/pre26/',
        'https://beauty.hotpepper.jp/pre27/',
        'https://beauty.hotpepper.jp/pre28/',
        'https://beauty.hotpepper.jp/pre29/',
        'https://beauty.hotpepper.jp/pre30/',
        'https://beauty.hotpepper.jp/pre31/',
        'https://beauty.hotpepper.jp/pre32/',
        'https://beauty.hotpepper.jp/pre33/',
        'https://beauty.hotpepper.jp/pre34/',
        'https://beauty.hotpepper.jp/pre35/',
        'https://beauty.hotpepper.jp/pre36/',
        'https://beauty.hotpepper.jp/pre37/',
        'https://beauty.hotpepper.jp/pre38/',
        'https://beauty.hotpepper.jp/pre39/',
        'https://beauty.hotpepper.jp/pre40/',
        'https://beauty.hotpepper.jp/pre41/',
        'https://beauty.hotpepper.jp/pre42/',
        'https://beauty.hotpepper.jp/pre43/',
        'https://beauty.hotpepper.jp/pre44/',
        'https://beauty.hotpepper.jp/pre45/',
        'https://beauty.hotpepper.jp/pre46/',
        'https://beauty.hotpepper.jp/pre47/',
    ]

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')

        salon_h3_list = soup.find_all("h3", class_="slcHead")
        for salon_h3 in salon_h3_list:
            link = salon_h3.find('a')
            # サロンページへ遷移
            yield scrapy.Request(link.get('href'), self.parse_salon_page)

        # 次ページへ移動
        next_link = soup.find("li", class_="afterPage").findNext('a')
        yield scrapy.Request(next_link.get('href'), callback=self.parse)

    def parse_salon_page(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')

        item = HotPepperBeautyScrapyItem()
        item['サロン名'] = soup.h1.get_text()
        item['サロンページurl'] = response.url
        tel_link = None
        job_link = soup.find("a", class_="jscCareerLink")
        for th in soup.find("table", class_="slnDataTbl").find_all("th"):
            if th.get_text() == '電話番号':
                tel_link = th.next_element.findNext('td').findNext('a')
            elif th.get_text() == '住所':
                item["サロン住所"] = th.next_element.findNext('td').get_text().strip()
            elif th.get_text() == 'アクセス・道案内':
                item["アクセス道案内"] = th.next_element.findNext('td').get_text().strip()
            elif th.get_text() == '営業時間':
                item["営業時間"] = th.next_element.findNext('td').get_text().strip()
            elif th.get_text() == '定休日':
                item["定休日"] = th.next_element.findNext('td').get_text().strip()
            elif th.get_text() == 'クレジットカード':
                item["クレジットカード"] = th.next_element.findNext('td').get_text().strip()
            elif th.get_text() == 'お店のホームページ':
                item["お店のホームページ"] = th.next_element.findNext('td').get_text().strip()
            elif th.get_text() == 'カット価格':
                item["カット価格"] = th.next_element.findNext('td').get_text().strip()
            elif th.get_text() == '席数':
                item["席数"] = th.next_element.findNext('td').get_text().strip()
            elif th.get_text() == 'スタッフ数':
                item["スタッフ数"] = th.next_element.findNext('td').get_text().strip()
            elif th.get_text() == '駐車場':
                item["駐車場"] = th.next_element.findNext('td').get_text().strip()
            elif th.get_text() == 'こだわり条件':
                item["こだわり条件"] = th.next_element.findNext('td').get_text().strip()
            elif th.get_text() == '備考':
                item["備考"] = th.next_element.findNext('td').get_text().strip()

        if tel_link is not None and job_link is not None:
            # 電話番号ページ→求人ページへ
            request = scrapy.Request(tel_link.get('href'), self.parse_tel_page)
            request.meta['item'] = item
            request.meta['exists_job'] = True
            yield request
        elif tel_link is not None:
            # 電話番号ページへ
            request = scrapy.Request(tel_link.get('href'), self.parse_tel_page)
            request.meta['item'] = item
            request.meta['exists_job'] = False
            yield request
        elif job_link is not None:
            # 求人ページへ
            job_link = soup.find("a", class_="jscCareerLink")
            request = scrapy.Request(job_link.get('href'), self.parse_job_page)
            request.meta['item'] = item
            yield request
        else:
            yield item

    def parse_tel_page(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')

        item = response.meta['item']
        item["電話番号"] = soup.find("td").get_text()

        exists_job = response.meta['exists_job']
        if exists_job:
            # サロンページへ戻る
            salon_link = soup.find("div", class_="title").find("a")
            request = scrapy.Request(salon_link.get('href'), self.parse_salon_page_back)
            request.meta['item'] = item
            yield request
        else:
            yield item

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
                item['勤務地'] = head.next_element.findNext('pre').contents[0].strip()
            elif head.get_text() == '雇用形態':
                item['雇用形態'] = head.next_element.findNext('pre').contents[0].strip()
            elif head.get_text() == '職種':
                item['職種'] = head.next_element.findNext('pre').contents[0].strip()
            elif head.get_text() == '給与':
                item['給与'] = head.next_element.findNext('pre').contents[0].strip()
            elif head.get_text() == '勤務時間':
                item['勤務時間'] = head.next_element.findNext('pre').contents[0].strip()
            elif head.get_text() == '休日':
                item['休日'] = head.next_element.findNext('pre').contents[0].strip()
            elif head.get_text() == '待遇':
                item['待遇'] = head.next_element.findNext('pre').contents[0].strip()
            elif head.get_text() == '教育・研修制度':
                item['教育研修制度'] = head.next_element.findNext('pre').contents[0].strip()
            elif head.get_text() == '求める人物像':
                item['求める人物像'] = head.next_element.findNext('pre').contents[0].strip()
            elif head.get_text() == '応募資格・条件':
                item['応募資格条件'] = head.next_element.findNext('pre').contents[0].strip()
            elif head.get_text() == '会社名':
                item['会社名'] = head.next_element.findNext('pre').contents[0].strip()
            elif head.get_text() == '会社所在地':
                item['会社所在地'] = head.next_element.findNext('pre').contents[0].strip()
            elif head.get_text() == '設立年月日':
                item['設立年月日'] = head.next_element.findNext('pre').contents[0].strip()
            elif head.get_text() == '店舗数':
                item['店舗数'] = head.next_element.findNext('pre').contents[0].strip()

        yield item
