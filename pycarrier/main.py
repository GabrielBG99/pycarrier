#!/usr/bin/env python3

import asyncio
from enum import Enum
import typer
from tabulate import tabulate
from .carriers.base import BaseCarreier
from .carriers.correios import Correios
from .carriers.jadlog import Jadlog
from .exceptions import BaseCorreioException
from .event import Event


class Carrier(str, Enum):
    CORREIOS = 'correios'
    JADLOG = 'jadlog'


def track(carrier: Carrier, tracking_code: str) -> None:
    carrier: BaseCarreier = {
        Carrier.CORREIOS: Correios,
        Carrier.JADLOG: Jadlog,
    }[carrier]()

    try:
        events: list[Event] = asyncio.run(carrier.track(code=tracking_code))
    except BaseCorreioException as e:
        typer.echo(f'Error: {str(e)}')
        raise typer.Exit(1) from e

    data = [
        {
            k.capitalize(): v
            for k, v in e.dict().items()
        }
        for e in events
    ]
    table = tabulate(data, headers='keys', tablefmt='github')
    typer.echo(table)


def main():
    typer.run(track)


if __name__ == '__main__':
    main()
