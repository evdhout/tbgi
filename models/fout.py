import pandas as pd
from models.leerling import Leerling


class Fout:
    ONBEKENDE_LEERLING = 0
    MEERVOUDIGE_LEERLING = 1
    LEERLING_NIET_GELIJK = 2
    MELDING = ['Onbekende leerling', 'Leerling meerdere keren gevonden', 'Leerling niet gelijk']

    TBGI = 0
    SOMTODAY = 1
    BRON = ['TBGI', 'Somtoday']

    def __init__(self,
                 fout: int,
                 bron: int = TBGI,
                 leerling: Leerling or None = None,
                 tbgi: pd.Series or None = None):
        self.fout: int = fout
        self.bron: int = bron
        self.leerling: [Leerling] = []
        self.tbgi: [pd.Series] = []

        if leerling is not None:
            self.leerling.append(leerling)
        if tbgi is not None:
            self.tbgi.append(tbgi)

    def __str__(self):
        if self.fout == Fout.LEERLING_NIET_GELIJK:
            return(f'{self.leerling[0].llno} ({self.leerling[0].naam}) '
                   f'met {Fout._get_bsn_own_string(bsn=self.tbgi[0]["BSN"], own=self.tbgi[0]["OWN"])} niet gelijk:\n'
                   f'  Somtoday categorie: {self.leerling[0].categorie}\n'
                   f'  TBGI categorie:     {self.tbgi[0]["categorie"]}')
        elif self.bron == Fout.TBGI:
            bsn_own_string = Fout._get_bsn_own_string(bsn=self.tbgi[0]['BSN'], own=self.tbgi[0]['OWN'])
            if self.fout == Fout.ONBEKENDE_LEERLING:
                return f'Leerling met {bsn_own_string} niet gevonden in Somtoday.'
            elif self.fout == Fout.MEERVOUDIGE_LEERLING:
                return f'Leerling met {bsn_own_string} meerdere keren gevonden in Somtoday.'
            else:
                return f'Onbekende fout {self.fout} voor leerling met {bsn_own_string}.'
        elif self.bron == Fout.SOMTODAY:
            leerling_string = (f'{self.leerling[0].llno} ({self.leerling[0].naam}) met '
                               f'{Fout._get_bsn_own_string(bsn=self.leerling[0].BSN, own=self.leerling[0].OWN)}')
            if self.fout == Fout.ONBEKENDE_LEERLING:
                return(f'{leerling_string} niet gevonden in TBGI.\n'
                       f'  Status Somtoday "{self.leerling[0].categorie}".')
            elif self.fout == Fout.MEERVOUDIGE_LEERLING:
                return f'{leerling_string} meerdere keren gevonden in TBGI.'
            else:
                return f'Onbekende fout {self.fout} voor {leerling_string}.'
        else:
            return f'Onbekende bron {self.bron}.'

    @staticmethod
    def _get_bsn_own_string(bsn: str = '', own: str = ''):
        bsn_own: [str] = []
        if not pd.isna(bsn) and bsn != '':
            bsn_own.append(f'BSN "{bsn}"')
        if not pd.isna(own) and own != '':
            bsn_own.append(f'OWN "{own}"')
        return ' of '.join(bsn_own)

    def add_leerling(self, leerling: Leerling):
        self.leerling.append(leerling)

    def add_tbgi_regel(self, tbgi: pd.Series):
        self.tbgi.append(tbgi)
