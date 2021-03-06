import pandas as pd
from datetime import date
from models.options import Options
from models.telling_status import TellingStatus


class Categorie:
    def __init__(self, options: Options):
        self.teldatum = options.teldatum
        self.peildatum_cat1 = options.peildatum_cat1
        self.peildatum_cat2 = options.peildatum_cat2
        self.soort = options.soort

    def get_category_somtoday(self,
                              dinl: date, nat: str, begin: date, eind: date,
                              bek: str, stam: str, bron: str) -> str:
        if pd.isnull(begin) or begin > self.teldatum:
            return TellingStatus.NIET_INGESCHREVEN
        elif not pd.isnull(eind) and eind < self.teldatum:
            return TellingStatus.NIET_INGESCHREVEN
        elif bek != 'Standaard':
            return TellingStatus.NIET_BEKOSTIGBAAR
        elif stam[:2] == 'IB':
            return TellingStatus.INBURGERING
        elif stam[:1] == 'U':
            return TellingStatus.UITWISSELING
        elif bron == 'J':
            return TellingStatus.NIET_NAAR_BRON
        elif nat == 'Nederlandse':
            return TellingStatus.REGULIER_NL
        elif dinl > self.peildatum_cat1:
            return TellingStatus.CATEGORIE_1
        elif dinl > self.peildatum_cat2 and self.soort == 'nieuwkomer':
            return TellingStatus.CATEGORIE_2
        else:
            return TellingStatus.REGULIER

    def get_category_tbgi(self, signaal: int, cat_nk: str, bekostigbaar: bool) -> str:
        # print(f'{signaal} - {cat_nk} - {bekostigbaar} - {self.soort}')
        if 1 == signaal:
            return TellingStatus.NIET_INGESCHREVEN
        elif 7 == signaal:
            return TellingStatus.DUBBELE_INSCHRIJVING
        elif 9 == signaal:
            return TellingStatus.NIET_BEKOSTIGBAAR
        elif not bekostigbaar:
            return TellingStatus.NIET_BEKOSTIGBAAR
        elif Options.REGULIER == self.soort and '10' == signaal:
            return TellingStatus.CATEGORIE_1
        elif Options.NIEUWKOMER == self.soort and "1" == cat_nk:
            return TellingStatus.CATEGORIE_1
        elif Options.NIEUWKOMER == self.soort and "2" == cat_nk:
            return TellingStatus.CATEGORIE_2
        elif Options.REGULIER == self.soort:
            return TellingStatus.REGULIER
        else:
            return TellingStatus.TBGI_ONBEKEND
