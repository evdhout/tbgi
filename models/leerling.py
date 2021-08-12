import pandas as pd
from models.telling_status import TellingStatus
from models.signaal import Signaal


class Leerling:

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
