import logging
from enum import Enum
from typing import List, Optional

import typer
import yaml
from pydantic import BaseModel
from pydantic.error_wrappers import ValidationError
from rich.console import Console

from posting_app.database import create_database, create_db_and_tables, PostingRepository
from posting_app.services import PostingServiceFactory
from telegram_app.services import TelegramService

console = Console()


class OutputMode(str, Enum):
    telegram = "telegram"
    console = "console"


class Config(BaseModel):
    pages: Optional[int] = 3
    sleep_time: Optional[int] = 5
    bot_token: Optional[str] = None
    chat_room: Optional[str] = None
    persist: Optional[bool] = False
    zonaprop_barrios: Optional[List[str]] = None
    zonaprop_tipos: Optional[List[str]] = None
    zonaprop_precio_min: Optional[int] = None
    zonaprop_precio_max: Optional[int] = None
    max_posting_antiquity_days: Optional[int] = 30
    database_filename: Optional[str] = 'scrapdep'


def build_zonaprop_url(tipos: List[str], barrios: List[str], precio_min: int, precio_max: int) -> str:
    tipos_str = "-".join(tipos)
    barrios_str = "-".join(barrios)
    return (
        f"https://www.zonaprop.com.ar/{tipos_str}-alquiler-{barrios_str}"
        f"-desde-1-hasta-3-ambientes-{precio_min}-{precio_max}"
        f"-pesos-orden-publicado-descendente-pagina-{{}}.html"
    )


def main(
        config_path: str,
        output: OutputMode = typer.Option(OutputMode.console, help="Destino de los postings: telegram o console"),
        log_level: str = typer.Option("WARNING", help="Nivel de logging: DEBUG, INFO, WARNING, ERROR"),
):
    logging.basicConfig(level=log_level.upper(), format='%(name)s %(levelname)s: %(message)s')

    # LOAD CONFIG
    with open(config_path) as config_json:
        config_dict = yaml.safe_load(config_json)

    try:
        config = Config(**config_dict)
    except ValidationError as ex:
        console.log(
            '[bold u]ERROR[/bold u]: Config error.\n', ex, style='red'
        )
        return
    console.log('Configuration read correctly', style='italic bold green')

    # CREATE DATABASE
    create_database(config.database_filename)

    # LOAD DATABASE
    create_db_and_tables()
    console.log('Database loaded', style='italic bold green')

    if config.zonaprop_barrios and config.zonaprop_tipos:
        zonaprop_url = build_zonaprop_url(
            tipos=config.zonaprop_tipos,
            barrios=config.zonaprop_barrios,
            precio_min=config.zonaprop_precio_min,
            precio_max=config.zonaprop_precio_max,
        )
        console.log(f'Zonaprop URL: [u]{zonaprop_url}[/u]')
        zonaprop_posting_service = PostingServiceFactory.build_for_zonaprop(
            pages=config.pages,
            full_url=zonaprop_url,
            max_antiquity_days=config.max_posting_antiquity_days,
        )
        zonaprop_posting_service.scrap_and_create_postings()

    console.log('Postings scrapped', style='italic bold green')

    # SEND POSTINGS
    posting_repository = PostingRepository()
    unsent_postings = posting_repository.get_unsent_postings()

    console.log(f'About to send [u]{len(unsent_postings)}[/u] postings')

    if output == OutputMode.console:
        for posting in unsent_postings:
            console.print(posting)
    else:
        if not config.bot_token or not config.chat_room:
            console.log('[bold u]ERROR[/bold u]: bot_token y chat_room son requeridos para modo telegram', style='red')
            return
        telegram_service = TelegramService(
            bot_token=config.bot_token,
            chat_room=config.chat_room,
        )
        for posting in unsent_postings:
            msg_text = telegram_service.format_posting_to_message(posting)
            sent = telegram_service.send_telegram_message(msg_text)
            if sent:
                posting_repository.set_posting_as_sent(posting.sha)
            else:
                console.log(
                    (
                        '[bold u]WARNING[/bold u]: '
                        f'Unable to send {posting.title}. '
                        'I\'m going to try later though, [u]don\'t panic[/u]'
                    ),
                    style='yellow'
                )

    console.log('Done', style='italic bold green')


if __name__ == '__main__':
    typer.run(main)
