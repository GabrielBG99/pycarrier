import re
from datetime import datetime
import httpx
from bs4 import BeautifulSoup
from bs4.element import Tag
from .base import BaseCarreier
from ..event import Event
from ..exceptions import InvalidTrackingCode, OrderNotDispatched, UnknownError


class Correios(BaseCarreier):
    URL = 'https://www2.correios.com.br/sistemas/rastreamento/ctrl/ctrlRastreamento.cfm?'
    TRACKING_CODE_LENGTH = 13

    async def track(self, code: str) -> list[Event]:
        if not code or not self._tracking_code_is_valid(code=code):
            raise InvalidTrackingCode

        async with httpx.AsyncClient() as client:
            r = await client.post(Correios.URL, data={
                'acao': 'track',
                'objetos': code.upper(),
                'btnPesq': 'Buscar',
            })

        page = BeautifulSoup(r.content, 'html.parser')
        if code.upper() not in page.text:
            self._raise_what_happened(text=page.text)

        event_list = page.find_all(class_='listEvent')

        events = []
        for e in event_list:
            event = self._parse_event(table=e)
            events.append(event)

        events.sort(key=lambda e: e.time, reverse=True)

        return events

    def _tracking_code_is_valid(self, code: str) -> bool:
        matchLength = len(code) == Correios.TRACKING_CODE_LENGTH
        matchPattern = re.search(r'^[A-Z]{2}\d{9}[A-Z\d]{2}$', code.upper())

        return matchLength and matchPattern

    def _parse_event(self, table: Tag) -> Event:
        data = table.find_all('tr')[0].find_all('td')

        geo_info = [
            d.strip()
            for d in data[0].text.split('\n')
            if d.strip()
        ]

        time = datetime.strptime(geo_info[0] + geo_info[1], '%d/%m/%Y%H:%M')
        local = geo_info[2].replace(u'\xa0', ' ')
        title = data[1].find('strong').text.strip()

        detail = '\n'.join(data[1].text.strip().split('\n')[1:])
        detail = ' '.join(detail.split())

        event = Event(
            time=time,
            local=local,
            title=title,
            detail=detail,
        )
        return event

    def _raise_what_happened(self, text: str) -> None:
        if 'Aguardando postagem pelo remetente' in text:
            raise OrderNotDispatched
        if 'O(s) código(s) ou CPF/CNPJ estão inválidos' in text:
            raise InvalidTrackingCode

        raise UnknownError
