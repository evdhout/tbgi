import pandas as pd
from models.telling_status import TellingStatus
from models.signaal import Signaal
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

class LeerlingOud:

    def __init__(self, leerling: dict or pd.Series = None):
        self.llno = 0
        self.naam = None
        self.dinl = None
        self.BSN = None
        self.OWN = None
        self.nat = None
        self.stam = None
        self.bek = None
        self.begin = None
        self.eind = None
        self.categorie = None
        if leerling is not None:
            if isinstance(leerling, dict):
                leerling = pd.Series(leerling)
            self.init_series(leerling)

    def init_series(self, leerling: pd.Series):
        self.llno = leerling['llno']
        self.naam = leerling['naam']
        self.dinl = leerling['dinl']
        self.BSN = leerling['BSN']
        self.OWN = leerling['OWN']
        self.nat = leerling['nat']
        self.stam = leerling['stam']
        self.bek = leerling['bek']
        self.begin = leerling['begin']
        self.eind = leerling['eind']
        self.categorie = leerling['categorie']

    def check_tbgi(self, tbgi: pd.Series):
        if TellingStatus.is_gelijk(self.categorie, tbgi['categorie']):
            return True

        print(f"Leerling {self.naam} {self.llno} met BSN {tbgi.BSN} of OWN {tbgi.OWN} niet gelijk")
        print(f"  Categorie somtoday = {self.categorie}")
        print(f"  BSN somtoday       = {self.BSN}")
        print(f"  OWN somtoday       = {self.OWN}")
        print(f"  Begindatum         = {self.begin}")
        print(f"  Einddatum          = {self.eind}")
        print(f"  Categorie TBG-i    = {tbgi['categorie']}")
        print(f"  BSN TBG-i          = {tbgi['BSN']}")
        print(f"  OWN TBG-i          = {tbgi['OWN']}")
        Signaal.show_signals(tbgi)

    def is_actief(self):
        if self.categorie in TellingStatus.ALT_NIET_INGESCHREVEN:
            return False
        return True
