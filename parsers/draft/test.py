import re
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from mechanize import Browser, urlopen
import logging

_format = f"%(asctime)s [%(levelname)s] - %(name)s - %(funcName)s(%(lineno)d) - %(message)s"

file = 'app_logs.log'

file_handler = logging.FileHandler(file)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter(_format))

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(logging.Formatter(_format))


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    return logger

""" Парсер для роботи з сайтом parsers """

HEADERS = {
    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko)"
}
cur_time = datetime.now().strftime("%d_%m_%Y_%H_%M")
logger = get_logger(__name__)


def get_url(url_):
    url_ += '#additional:~:text=Spezifikationen'
    br = Browser()
    # Add some headers
    br.addheaders = [('User-agent',
                      'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 '
                      'Firefox/3.0.1')]
    # Open url in Browser instance
    br.open(url_)
    forms = br.forms()
    links = br.links()
    content = br.click_link(url_)
    with open(f"parsers/draft/test_link.html", "w") as fh:
        fh.write(content)
    logger.debug(content)
    # for link in links:
    #     print(link.text, link.url)

    logger.debug(forms)




def parse_link(url):  # парсить сайт за допомогою лінк

    # url += '#additional:~:text=Spezifikationen'
    response = requests.get(url).content
    # with open(f"parsers/draft/test_link.html", "w") as fh:
    #     fh.write(response)
    soup = BeautifulSoup(response, 'lxml')
    logger.debug(f'URL {url}')
    try:
        tables = soup.find('table', class_='data table additional-attributes').find_all('td', class_="col data")
        title_ = soup.title.text.split('|')
        content = soup.find_all('meta')
        table_content = ''
        for table in tables:
            table_content += table.text + ' '
        ean_ = re.search('\d{13}', table_content)
        if ean_:
            ean = ean_.group()
            logger.debug(f'EAN {ean}')
        article_ = re.search('\d{8}', table_content)
        article = None
        if article_:
            article = article_.group()
            logger.debug(f'Article {article}')
        if not ean_ and article_:
            url_q = f'https://www.babypark.de/search/?q={article}'
            response = requests.get(url_q).content
            # with open(f"parsers/draft/test_link.html", "w") as fh:
            #     fh.write(response)
            soup = BeautifulSoup(response, 'lxml')
            item = soup.find('div', class_='klevuImgWrap')
            logger.debug(item)
    except Exception as err:
        print(err)


if __name__ == '__main__':
    url = 'https://www.babypark.de/smallstuff-teppich-rund-melange.html'
    # get_url(url)
    parse_link(url)
