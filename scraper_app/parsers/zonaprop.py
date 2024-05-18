from typing import Set

from posting_app.database import Posting, PostingRepository
from .base import BaseParser


class ZonapropParser(BaseParser):
    base_info_class = 'PostingCardLayout-sc-i1odl-0'
    base_info_tag = 'div'
    link_regex = 'a.go-to-posting'
    price_regex = 'div.Price-sc-12dh9kl-3'
    description_regex = 'h3.PostingDescription-sc-i1odl-11'
    location_regex = "div.LocationBlock-sc-ge2uzh-1"
    _base_url = 'https://www.zonaprop.com.ar'

    def extract_data(self) -> Set[Posting]:
        '''Extracting data and returning list of postings'''
        postings = set()
        base_info_soaps = self.soup.find_all(
            self.base_info_tag, class_=self.base_info_class)

        for base_info_soap in base_info_soaps:
            try:
                link_text = base_info_soap.attrs['data-to-posting']
                price_container = base_info_soap.select(self.price_regex)[0]
                description_container = base_info_soap.select(
                    self.description_regex)[0].a
                location_container = base_info_soap.select(
                    self.location_regex)[0].select("div.postingAddress")[0]
            except Exception as e:
                print('ERROR: the regex didnt work')
                continue

            href = '{}{}'.format(
                self._base_url,
                link_text,
            )
            title = self.sanitize_text(link_text)
            sha = self.get_id(href)
            price = price_container.text
            description = self.sanitize_text(description_container.text)
            location = self.sanitize_text(location_container.text)

            posting_repository = PostingRepository()
            if posting_repository.get_posting_by_sha(sha):
                continue

            new_posting = Posting(
                sha=sha,
                url=href,
                title=title,
                price=price,
                description=description,
                location=location,
            )
            postings.add(new_posting)

        return postings
