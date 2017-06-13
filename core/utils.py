import re
import requests

from django.conf import settings
from bs4 import BeautifulSoup


class ParsedApp:
    BASE_URL = settings.GOOGLE_PLAY_URL
    APP_ID_URL = settings.GOOGLE_PLAY_APP_ID

    def __init__(self, app_soup):
        self.app_soup = app_soup

    @property
    def doc_id(self):
        return self.app_soup['data-docid']

    @property
    def url(self):
        return self.APP_ID_URL.format(self.doc_id)

    @property
    def title(self):
        detail_a_tag = self.app_soup.find('a', class_='title')
        return detail_a_tag['title']

    @property
    def description(self):
        description_div_tag = self.app_soup.find('div', class_='description')
        return description_div_tag.getText().strip()

    @property
    def price(self):
        price_span = self.app_soup.find('span', class_='display-price')
        return price_span.getText()

    @property
    def rating(self):
        rating_text = self.app_soup.find(
            'div', class_='tiny-star')['aria-label']
        return re.findall(r'\d+.\d+', rating_text)[0]

    @property
    def cover_large(self):
        return self.cover_img_selector['data-cover-large']

    @property
    def cover_small(self):
        return self.cover_img_selector['data-cover-small']

    @property
    def cover_img_selector(self):
        return self.app_soup.find('img', class_='cover-image')

    @property
    def developer_url(self):
        return self.BASE_URL + self.developer_selector['href']

    @property
    def developer_title(self):
        return self.developer_selector['title']

    @property
    def developer_selector(self):
        return self.app_soup.find('a', class_='subtitle')


def fetchPlayHTML(search_terms):
    SEARCH_URL = settings.GOOGLE_PLAY_SEARCH_URL
    URL = SEARCH_URL.format(search_terms)
    html = requests.get(URL).content
    return html


class PlayParser:
    APPS_SELECTOR = '.cluster.apps .card.apps'

    def __init__(self, search_terms):
        self.search_terms = search_terms
        self.soup = BeautifulSoup(
            fetchPlayHTML(self.search_terms),
            'html.parser'
        )

    def getApps(self):
        apps_soup = self.soup.select(self.APPS_SELECTOR)
        return list(map(self.parseAppHTML, apps_soup))

    def parseAppHTML(self, app_soup):
        return ParsedApp(app_soup)
