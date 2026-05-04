import logging

from posting_app.database import Posting, PostingRepository
from .base import BaseParser

logger = logging.getLogger(__name__)


class ZonapropParser(BaseParser):
    base_info_class = 'postingCardLayout-module__posting-card-layout'
    price_div_class = 'postingPrices-module__price-container'
    description_div_class = 'postingCard-module__posting-description'
    location_regex = "div.LocationBlock-sc-ge2uzh-1"
    _base_url = 'https://www.zonaprop.com.ar'

    def extract_data(self):
        '''Extracting data and returning list of postings'''
        postings = set()
        reached_known = False
        base_info_soaps = self.soup.find_all("div", class_=self.base_info_class)

        logger.debug(f'Found {len(base_info_soaps)} items on page')

        posting_repository = PostingRepository()
        for base_info_soap in base_info_soaps:
            try:
                link_text = base_info_soap.attrs['data-to-posting']
                price_container = base_info_soap.find("div", class_=self.price_div_class)
                description_container = base_info_soap.find("h2", class_=self.description_div_class)
                location_container = base_info_soap.find("div", class_="postingLocations-module__location-block")
            except Exception as e:
                logger.debug(f'Skipping item, parse error: {e}')
                continue

            href = f'{self._base_url}{link_text}'
            title = self.sanitize_text(link_text)
            sha = self.get_id(href)
            price = price_container.text
            description = self.sanitize_text(description_container.text)
            location = self.sanitize_text(location_container.text)

            if posting_repository.get_posting_by_sha(sha):
                logger.debug(f'Skipping {href}, already in DB — reached frontier')
                reached_known = True
                continue

            logger.debug(f'New posting: {location} | {price} | {href}')
            new_posting = Posting(
                sha=sha,
                url=href,
                title=title,
                price=price,
                description=description,
                location=location,
            )
            postings.add(new_posting)

        return postings, reached_known
