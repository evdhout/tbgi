import pandas as pd
from datetime import date
from models.settings import Settings
from models.telling_status import TellingStatus


class Categorie:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.teldatum = settings.teldatum
        self.peildatum_cat1 = settings.peildatum_cat1
        self.peildatum_cat2 = settings.peildatum_cat2
        self.soort = settings.soort
        self.regeling = settings.regeling

        print(self.settings.regeling)
        print(self.peildatum_cat1)
        print(self.peildatum_cat2)
        print(self.soort)


    def get_category_somtoday(self,
                              dinl: date, oinl: date, nat: str, begin: date, eind: date,
                              bek: str, stam: str, bron: str) -> str:
        if self.regeling == self.settings.REGELING_OINL:
            check_datum = oinl
        elif self.regeling == self.settings.REGELING_DINL:
            check_datum = dinl
        else:
            return TellingStatus.REGELING_ONBEKEND

        if pd.isnull(begin) or begin > self.teldatum:
            return TellingStatus.NIET_INGESCHREVEN
        elif not pd.isnull(eind) and eind < self.teldatum:
            return TellingStatus.NIET_INGESCHREVEN
        elif self.regeling == self.settings.REGELING_DINL and pd.isna(check_datum):
            # leerling woont niet in Nederland, maar wel ingeschreven
            return TellingStatus.REGULIER
        elif bek != 'Standaard':
            return TellingStatus.NIET_BEKOSTIGBAAR
        elif pd.isna(stam):
            return TellingStatus.GEEN_STAMGROEP
        elif stam[:2] == 'IB':
            return TellingStatus.INBURGERING
        elif stam[:1] == 'U':
            return TellingStatus.UITWISSELING
        elif bron == 'J':
            return TellingStatus.NIET_NAAR_ROD
        elif nat == 'Nederlandse':
            return TellingStatus.REGULIER_NL
        elif check_datum > self.peildatum_cat1:
            return TellingStatus.CATEGORIE_1
        elif check_datum > self.peildatum_cat2 and self.soort == self.settings.NIEUWKOMER:
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
        elif Settings.REGULIER == self.soort and '10' == signaal:
            return TellingStatus.CATEGORIE_1
        elif Settings.NIEUWKOMER == self.soort and "1" == cat_nk:
            return TellingStatus.CATEGORIE_1
        elif Settings.NIEUWKOMER == self.soort and "2" == cat_nk:
            return TellingStatus.CATEGORIE_2
        elif Settings.REGULIER == self.soort:
            return TellingStatus.REGULIER
        else:
            return TellingStatus.TBGI_ONBEKEND
