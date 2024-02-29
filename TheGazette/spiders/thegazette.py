from scrapy import Spider, Request, Selector
from ..items import PfassessmentItem


class thegazette(Spider):
    name = 'thegazette'

    # Using Scrapy custom settings to create an output csv file
    custom_settings = {
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'thegazette_data.csv',
    }

    url = ('https://www.thegazette.co.uk/all-notices/notice?text=&categorycode-all='
           'all&noticetypes=&location-postcode-1=&location-distance-1=1&'
           'location-local-authority-1=&numberOfLocationSearches=1&start-publish-date='
           '&end-publish-date=&edition=&london-issue=&edinburgh-issue=&'
           'belfast-issue=&sort-by=&results-page-size=10')

    # Using header to avoid blockage from the website due to missing user-agent
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/'
                      '537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    }

    def start_requests(self):
        meta = {'dont_merge_cookies': True} # Using Dont Merge Cookies to avoid getting blocked
        yield Request(self.url, self.parse_notices,
                      meta=meta, headers=self.headers)

    def parse_notices(self, response):
        notice_urls = response.css('article h3 a::attr(href)').getall()
        for url in notice_urls:
            yield response.follow(url, self.parse_detail,
                                  meta=response.meta, headers=self.headers)

        next_page = response.css('.next a::attr(href)').get()

        if 'results-page=16' in next_page: # We need to go till page 15 only
            return

        if next_page:
            yield response.follow(next_page, self.parse_notices,
                                  meta=response.meta, headers=self.headers)

    def parse_detail(self, response):
        item = PfassessmentItem()
        item['notice_title'] = response.css('h2.timeline-title::text').get('').strip().split('\n')[-1].strip()
        # Used strip to clear the extra characters in the description
        notice_text = [text.strip() for text in response.css('.content span::text, p::text').getall()]
        item['notice_text'] = '\n'.join(notice_text)
        item['category_name'] = response.css('dd.category::text').get('').strip()
        item['notice_types'] = response.css('dd.notice-type::text').get('').strip()
        item['edition'] = response.css('dt:contains("Edition") + dd::text').get('').strip()
        item['notice_id'] = response.css('dt:contains("Notice ID") + dd::text').get('').strip()
        item['notice_code'] = response.css('dt:contains("Notice code") + dd::text').get('').strip()
        item['company_number'] = response.css('dt:contains("Company number") + dd a::text').get('').strip()
        item['publish_date'] = response.css('dt:contains("Publication date") + dd time::text').get('').strip()
        item['notice_url'] = response.url
        yield item
