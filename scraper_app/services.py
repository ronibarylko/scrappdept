from typing import List, Optional

from rich.console import Console

from posting_app.database import Posting
from .gateways import (
    ArgenpropGateway,
    BaseGateway,
    LaVozGateway,
    MercadolibreGateway,
    ProperatiGateway,
    ZonapropGateway,
)
from .parsers import (
    ArgenpropParser,
    BaseParser,
    LaVozParser,
    MercadolibreParser,
    ProperatiParser,
    ZonapropParser,
)

console = Console()


class ScraperService:
    def __init__(
            self,
            pages: int,
            url: str,
            gateway: BaseGateway,
            parser: BaseParser,
            max_antiquity_days: Optional[int] = None,
    ):
        self._pages = pages
        self._url = url
        self._gateway = gateway
        self._parser = parser
        self._max_antiquity_days = max_antiquity_days

    def get_postings_from_scraper(self) -> List[Posting]:
        postings = []
        max_pages = self._pages if self._gateway.paginated else 1
        too_old_reached = False

        for page in range(1, max_pages + 1):
            console.log(f'Page {page} of at most {max_pages}')
            html = self._gateway.make_request(
                url=self._url.format(page)
            )

            self._parser.get_soup_object(html=html)
            new_postings, reached_known = self._parser.extract_data()
            console.log(f'Got {len(new_postings)} new postings')

            for posting in new_postings:
                detail_html = self._gateway.make_request(url=posting.url)
                posting.antiquity = self._parser.extract_antiquity(detail_html)
                console.log(f'Antiquity for {posting.url}: {posting.antiquity}')

                days = posting.antiquity_days()
                if (
                    self._max_antiquity_days is not None
                    and days is not None
                    and days > self._max_antiquity_days
                ):
                    console.log(
                        f'Posting has antiquity of {days} days '
                        f'(> {self._max_antiquity_days}). Stopping scraping.',
                        style='yellow',
                    )
                    too_old_reached = True
                    break

                postings.append(posting)

            if too_old_reached:
                break

            if reached_known:
                console.log('Reached a known posting — stopping pagination', style='italic')
                break

        return postings


class ScraperServiceFactory:
    @classmethod
    def build_for_zonaprop(
            cls,
            pages: int,
            full_url: str,
            max_antiquity_days: Optional[int] = None,
    ) -> ScraperService:
        return ScraperService(
            pages=pages,
            url=full_url,
            gateway=ZonapropGateway(),
            parser=ZonapropParser(),
            max_antiquity_days=max_antiquity_days,
        )

    @classmethod
    def build_for_argenprop(
            cls,
            pages: int,
            full_url: str,
            max_antiquity_days: Optional[int] = None,
    ) -> ScraperService:
        return ScraperService(
            pages=pages,
            url=full_url,
            gateway=ArgenpropGateway(),
            parser=ArgenpropParser(),
            max_antiquity_days=max_antiquity_days,
        )

    @classmethod
    def build_for_mercadolibre(
            cls,
            pages: int,
            full_url: str,
            max_antiquity_days: Optional[int] = None,
    ) -> ScraperService:
        return ScraperService(
            pages=pages,
            url=full_url,
            gateway=MercadolibreGateway(),
            parser=MercadolibreParser(),
            max_antiquity_days=max_antiquity_days,
        )

    @classmethod
    def build_for_la_voz(
            cls,
            pages: int,
            full_url: str,
            max_antiquity_days: Optional[int] = None,
    ) -> ScraperService:
        return ScraperService(
            pages=pages,
            url=full_url,
            gateway=LaVozGateway(),
            parser=LaVozParser(),
            max_antiquity_days=max_antiquity_days,
        )

    @classmethod
    def build_for_properati(
            cls,
            pages: int,
            full_url: str,
            max_antiquity_days: Optional[int] = None,
    ) -> ScraperService:
        return ScraperService(
            pages=pages,
            url=full_url,
            gateway=ProperatiGateway(),
            parser=ProperatiParser(),
            max_antiquity_days=max_antiquity_days,
        )
