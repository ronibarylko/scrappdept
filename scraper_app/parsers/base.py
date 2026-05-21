import logging
from abc import ABC
from hashlib import sha1
from typing import Optional

from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class BaseParser(ABC):

    def get_soup_object(self, html: str):
        '''
        Taking HTML code as an entry, returns
        a BeautifulSoup object of the HTML code
        '''
        self.soup = BeautifulSoup(html, 'html.parser')

    def get_id(self, text: str) -> str:
        '''Get a SHA1 hash to identify each object.'''
        _id = sha1(text.lower().encode('utf-8')).hexdigest()
        return _id

    def sanitize_text(self, text):
        '''
        Sometimes the message comes out weirdly from the html
        this fixes it for you.
        '''
        return ' '.join(text.split())

    def extract_data(self):
        """Returns (new_postings, reached_known) where reached_known=True means
        a previously-seen posting was found and pagination should stop."""
        pass

    def extract_antiquity(self, detail_html: str) -> Optional[str]:
        """Extracts the antiquity text from a posting's detail page HTML.
        Returns None by default; parsers can override."""
        return None