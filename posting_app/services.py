from typing import Optional

from rich.console import Console

from scraper_app.services import ScraperService, ScraperServiceFactory
from .database import PostingRepository

console = Console()


class PostingService:
    def __init__(self, scraper_service: ScraperService):
        self._scraper_service = scraper_service
    
    def scrap_and_create_postings(self):
        postings = self._scraper_service.get_postings_from_scraper()
        posting_repository = PostingRepository()

        console.log(f'About to save {len(postings)} postings')
        for posting in postings:
            posting_repository.create_posting(posting)
        console.log('Postings saved successfully!', style='green')


class PostingServiceFactory:
    @classmethod
    def build_for_zonaprop(
        cls,
        pages: int,
        full_url: str,
        max_antiquity_days: Optional[int] = None,
    ) -> PostingService:
        scrapper_service = ScraperServiceFactory.build_for_zonaprop(
            pages=pages,
            full_url=full_url,
            max_antiquity_days=max_antiquity_days,
        )
        return PostingService(scraper_service=scrapper_service)

    @classmethod
    def build_for_argenprop(
        cls,
        pages: int,
        full_url: str,
        max_antiquity_days: Optional[int] = None,
    ) -> PostingService:
        scrapper_service = ScraperServiceFactory.build_for_argenprop(
            pages=pages,
            full_url=full_url,
            max_antiquity_days=max_antiquity_days,
        )
        return PostingService(scraper_service=scrapper_service)

    @classmethod
    def build_for_mercadolibre(
        cls,
        pages: int,
        full_url: str,
        max_antiquity_days: Optional[int] = None,
    ) -> PostingService:
        scrapper_service = ScraperServiceFactory.build_for_mercadolibre(
            pages=pages,
            full_url=full_url,
            max_antiquity_days=max_antiquity_days,
        )
        return PostingService(scraper_service=scrapper_service)

    @classmethod
    def build_for_la_voz(
        cls,
        pages: int,
        full_url: str,
        max_antiquity_days: Optional[int] = None,
    ) -> PostingService:
        scrapper_service = ScraperServiceFactory.build_for_la_voz(
            pages=pages,
            full_url=full_url,
            max_antiquity_days=max_antiquity_days,
        )
        return PostingService(scraper_service=scrapper_service)

    @classmethod
    def build_for_properati(
        cls,
        pages: int,
        full_url: str,
        max_antiquity_days: Optional[int] = None,
    ) -> PostingService:
        scrapper_service = ScraperServiceFactory.build_for_properati(
            pages=pages,
            full_url=full_url,
            max_antiquity_days=max_antiquity_days,
        )
        return PostingService(scraper_service=scrapper_service)
