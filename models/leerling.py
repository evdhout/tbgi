from models.somtoday import Somtoday
from models.tbgi import Tbgi
from collections import namedtuple


class Leerling:
    SOMTODAY = 'somtoday'
    TBGI = 'tbgi'
    BSN = 'bsn'
    OWN = 'own'

    def __init__(self, info: namedtuple, source: str = SOMTODAY):
        self.source: str = source
        self.somtoday: Somtoday or None = None
        self.tbgi: [Tbgi] = []
        self.bsn: str or None = None
        self.own: str or None = None
        self.ll_nr: int = 0

        if source == Leerling.SOMTODAY:
            self.somtoday = Somtoday(somtoday=info)
            self.bsn = self.somtoday[Somtoday.BSN] if self.somtoday.has_bsn() else None
            self.own = self.somtoday[Somtoday.OWN] if self.somtoday.has_own() else None
            self.ll_nr = self.somtoday[Somtoday.LEERLINGNUMMER]
        else:
            tbgi = Tbgi(tbgi=info)
            self.tbgi.append(tbgi)
            self.bsn = tbgi.data[Tbgi.BSN] if tbgi.has_bsn() else None
            self.own = tbgi.data[Tbgi.OWN] if tbgi.has_own() else None

    def add_tbgi(self, tbgi: namedtuple):
        tbgi = Tbgi(tbgi=tbgi)
        if not self.bsn and tbgi.data[Tbgi.BSN]:
            self.bsn = tbgi.data[Tbgi.BSN]
        if not self.own and tbgi.data[Tbgi.OWN]:
            self.own = tbgi.data[Tbgi.OWN]

    def has_bsn(self) -> bool:
        return self.bsn is not None

    def has_own(self) -> bool:
        return self.own is not None
