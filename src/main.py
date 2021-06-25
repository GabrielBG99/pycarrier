#!/usr/bin/env python3

import asyncio
from enum import Enum
import typer
from tabulate import tabulate
from carriers.base import BaseCarreier
from carriers.correios import Correios
from carriers.jadlog import Jadlog
from event import Event


class Carrier(str, Enum):
    CORREIOS = 'correios'
    JADLOG = 'jadlog'


def main(carrier: Carrier, tracking_code: str) -> None:
    carrier: BaseCarreier = {
        Carrier.CORREIOS: Correios,
        Carrier.JADLOG: Jadlog,
    }[carrier]()

    events: list[Event] = asyncio.run(carrier.track(code=tracking_code))

    data = [
        {
            k.capitalize(): v
            for k, v in e.dict().items()
        }
        for e in events
    ]
    table = tabulate(data, headers='keys', tablefmt='github')
    typer.echo(table)


if __name__ == '__main__':
    typer.run(main)
