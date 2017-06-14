import re
import requests
from decimal import Decimal
from django.conf import settings
from bs4 import BeautifulSoup
from core.models import App


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
        reg_list = re.findall('\d+.?\d*', price_span.getText())
        if(reg_list):
            return Decimal(reg_list[0])
        return Decimal(0)

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


def fetch_play_html(search_terms):
    SEARCH_URL = settings.GOOGLE_PLAY_SEARCH_URL
    URL = SEARCH_URL.format(search_terms)
    html = requests.get(URL).content
    return html


class PlayParser:
    APPS_SELECTOR = '.cluster.apps .card.apps'

    def __init__(self, search_terms):
        self.search_terms = search_terms
        self.soup = BeautifulSoup(
            fetch_play_html(self.search_terms),
            'html.parser'
        )

    def get_apps(self):
        apps_soup = self.soup.select(self.APPS_SELECTOR)
        return list(map(self.parse_app_html, apps_soup))

    def parse_app_html(self, app_soup):
        return ParsedApp(app_soup)


def fetch_apps(query):
    tag = query.lower()
    qs = App.objects.filter(tags__name=tag)
    if qs.exists():
        return qs
    play_parser = PlayParser(query)

    apps = list(map(get_or_create_app, play_parser.get_apps()))

    for app in apps:
        app.tags.add(tag)
    return App.objects.filter(tags__name=tag)


def get_or_create_app(parsed_app):
    app = App.objects.filter(app_id=parsed_app.doc_id).first()
    if app:
        return app
    app = App.objects.create(
        app_id=parsed_app.doc_id,
        description=parsed_app.description,
        url=parsed_app.url,
        rating=parsed_app.rating,
        name=parsed_app.title,
        developer_name=parsed_app.developer_title,
        developer_url=parsed_app.developer_url,
        price=parsed_app.price,
        cover_large=parsed_app.cover_large,
        cover_small=parsed_app.cover_small
    )
    return app
