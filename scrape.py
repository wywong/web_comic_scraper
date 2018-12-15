from bs4 import BeautifulSoup
from urllib import request
from contextlib import ExitStack
import traceback
from io import BytesIO
from PIL import Image
import pytesseract
import re


class ScrapeResult:
    def __init__(self, source, extracted_text):
        self.source = source
        self.extracted_text = extracted_text

    def __str__(self):
        return "ScrapeResult: (source, extracted_text)=(%s, %s)" \
            % (self.source, self.extracted_text)


class ComicScraper:
    PROTOCOL = 'https://'

    def __init__(self, parser):
        self.parser = parser

    def scrape(self, comic_range=range(1, 5)):
        for comic_id in comic_range:
            source = self.PROTOCOL + self.parser.BASE_URL + str(comic_id)
            try:
                with request.urlopen(source) as comic_page:
                    html = comic_page.read()
                    image_src = self.parser.parse(html)
                    extracted_text = self.extract_text(image_src)
                    result = ScrapeResult(source, extracted_text)
                    print(result)
            except Exception as err:
                print(err)
                print(traceback.format_exc())
                print("Missed comic: %s" % source)

    def extract_text(self, image_src):
        stripped_src = re.sub(r'^.*\/\/', '', image_src)
        with request.urlopen(self.PROTOCOL + stripped_src) as image_response:
            image = Image.open(BytesIO(image_response.read()))
            text = pytesseract.image_to_string(image)
            image.close()
            return text


class AbstruseGooseParser:
    BASE_URL = 'abstrusegoose.com/'

    def parse(self, html):
        soup = BeautifulSoup(html, "html.parser")
        section = soup.find('section')
        img_node = section.find('img')
        return img_node['src']

class XkcdParser:
    BASE_URL = 'xkcd.com/'

    def parse(self, html):
        soup = BeautifulSoup(html, "html.parser")
        comic = soup.find(id='comic')
        img_node = comic.find('img')
        return img_node['src']

#ComicScraper(AbstruseGooseParser()).scrape()
#ComicScraper(XkcdParser()).scrape(range(100, 105))

