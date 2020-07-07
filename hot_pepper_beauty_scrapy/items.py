# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class HotPepperBeautyScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    サロン名 = scrapy.Field()
    # サロンデータ
    電話番号 = scrapy.Field()
    サロン住所 = scrapy.Field()
    アクセス道案内 = scrapy.Field()
    営業時間 = scrapy.Field()
    定休日 = scrapy.Field()
    クレジットカード = scrapy.Field()
    お店のホームページ = scrapy.Field()
    カット価格 = scrapy.Field()
    席数 = scrapy.Field()
    スタッフ数 = scrapy.Field()
    駐車場 = scrapy.Field()
    こだわり条件 = scrapy.Field()
    備考 = scrapy.Field()
    # 求人情報
    勤務地 = scrapy.Field()
    雇用形態 = scrapy.Field()
    職種 = scrapy.Field()
    給与 = scrapy.Field()
    勤務時間 = scrapy.Field()
    休日 = scrapy.Field()
    待遇 = scrapy.Field()
    教育研修制度 = scrapy.Field()
    求める人物像 = scrapy.Field()
    応募資格条件 = scrapy.Field()
    会社名 = scrapy.Field()
    会社所在地 = scrapy.Field()
    設立年月日 = scrapy.Field()
    店舗数 = scrapy.Field()
    求人ページurl = scrapy.Field()
