from datetime import datetime
import httpx
from bs4 import BeautifulSoup
from bs4.element import Tag
from .base import BaseCarreier
from ..event import Event
from ..exceptions import NoTrackingData, InvalidTrackingCode


class Jadlog(BaseCarreier):
    URL = 'http://www.jadlog.com.br/siteInstitucional/tracking_dev.jad'

    async def track(self, code: str) -> list[Event]:
        if not code:
            raise InvalidTrackingCode

        params = {'cte': code}
        async with httpx.AsyncClient() as client:
            r = await client.get(Jadlog.URL, params=params)

        soup = BeautifulSoup(r.content, 'html.parser')
        if 'Não existem dados referentes a remessa' in soup.text:
            raise NoTrackingData

        events = []
        for tr in soup.find('tbody').find_all('tr'):
            e = self._parse_event(tr=tr)
            events.append(e)

        events.sort(key=lambda e: e.time, reverse=True)

        return events

    def _parse_event(self, tr: Tag) -> Event:
        texts = []
        for td in tr.find_all('td'):
            texts.append(' '.join(td.text.strip().split()))

        time = datetime.strptime(texts[0], '%d/%m/%Y %H:%M')
        local = texts[1]
        title = texts[2]
        detail = f'Com ponto de destino "{texts[3]}"'
        if texts[4]:
            detail += f' e com documento de número {texts[4]}'

        event = Event(
            time=time,
            local=local,
            title=title,
            detail=detail,
        )

        return event
