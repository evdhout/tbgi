import pandas as pd
from models.leerling import Leerling
from models.somtoday import Somtoday
from models.tbgi import Tbgi


class Fout:
    ONBEKENDE_LEERLING = 0
    MEERVOUDIGE_LEERLING = 1
    LEERLING_NIET_GELIJK = 2
    MEERDERE_LEERLINGEN_BSN = 3
    MEERDERE_LEERLINGEN_OWN = 4
    MATCH_OWN_MET_BSN = 5
    LEERLING_MEER_KEER_GETELD_IN_TBGI = 6
    ONBEKENDE_LEERLING_TBGI = 7
    ONBEKENDE_LEERLING_SOMTODAY = 8
    DINL_NIET_GELIJK = 9
    MELDING = ['Onbekende leerling', 'Leerling meerdere keren gevonden', 'Leerling niet gelijk',
               'Meerdere leerlingen met hetzelfde BSN', 'Meerdere leerlingen met hetzelfde OWN',
               'Leerling gevonden op OWN, maar leerling heeft al BSN',
               'De leerling is twee keer geteld in de TBG-i',
               'Leerling niet in Somtoday',
               'Leerling niet in TBG-i',
               'Datum in Nederland niet gelijk']

    TBGI = 0
    SOMTODAY = 1
    BRON = ['TBGI', 'Somtoday']

    def __init__(self,
                 fout: int,
                 bron: int = TBGI,
                 leerling: Leerling or [Leerling] or None = None,
                 tbgi: Tbgi or [Tbgi] or None = None):
        self.fout: int = fout
        self.bron: int = bron
        self.leerling: [Leerling] = []
        self.tbgi: [Tbgi] = []

        if leerling is not None:
            if type(leerling) is list:
                self.leerling = leerling
            else:
                self.leerling = [leerling]
        if tbgi is not None:
            if type(tbgi) is list:
                self.tbgi = tbgi
            else:
                self.tbgi = [tbgi]

    def __str__(self):
        if self.fout == Fout.LEERLING_NIET_GELIJK:
            leerling: Somtoday = self.leerling[0]
            tbgi: Tbgi = self.tbgi[0]
            return(f'{leerling[Somtoday.LEERLINGNUMMER]} ({leerling[Somtoday.VOLLEDIGE_NAAM]}) met '
                   f'{Fout._get_bsn_own_string(bsn=tbgi[Tbgi.BSN], own=tbgi[Tbgi.OWN])} niet gelijk:\n'
                   f'  Somtoday categorie: {leerling[Somtoday.CATEGORIE]}\n'
                   f'  TBGI categorie:     {tbgi[Tbgi.CATEGORIE]}')
        elif self.bron == Fout.TBGI:
            tbgi: Tbgi = self.tbgi[0]
            bsn_own_string = Fout._get_bsn_own_string(bsn=tbgi[Tbgi.BSN], own=tbgi[Tbgi.OWN])
            if self.fout == Fout.ONBEKENDE_LEERLING:
                return f'Leerling met {bsn_own_string} niet gevonden in Somtoday.'
            elif self.fout == Fout.MEERVOUDIGE_LEERLING:
                return(f'Leerling met {bsn_own_string} meerdere keren gevonden in Somtoday: '
                       f'{", ".join([ll[Somtoday.LEERLINGNUMMER] for ll in self.leerling])}.')
            elif self.fout == Fout.LEERLING_MEER_KEER_GETELD_IN_TBGI:
                bsn = self.get_tbgi_bsns()
                own = self.get_tbgi_owns()

                return(f'Leerling meer keer geteld. BSN: {bsn}, OWN: {own} '
                       f'Somtoday: {self.leerling[0].somtoday[Somtoday.LEERLINGNUMMER]} '
                       f'({self.leerling[0].somtoday[Somtoday.VOLLEDIGE_NAAM]})')
            else:
                return f'Onbekende fout {self.fout} voor leerling met {bsn_own_string}.'
        elif self.bron == Fout.SOMTODAY:
            leerling: Somtoday = self.leerling[0]
            leerling_string = (f'{leerling[Somtoday.LEERLINGNUMMER]} ({leerling[Somtoday.VOLLEDIGE_NAAM]}) met '
                               f'{Fout._get_bsn_own_string(bsn=leerling[Somtoday.BSN], own=leerling[Somtoday.OWN])}')
            if self.fout == Fout.ONBEKENDE_LEERLING:
                return(f'{leerling_string} niet gevonden in TBGI.\n'
                       f'  Status Somtoday "{leerling[Somtoday.CATEGORIE]}".')
            elif self.fout == Fout.MEERVOUDIGE_LEERLING:
                return(f'{leerling_string} meerdere keren gevonden in TBGI op regel '
                       f'{", ".join([t[Tbgi.REGEL_NUMMER] for t in self.tbgi])}')
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

    def get_tbgi_bsns(self) -> str:
        return ', '.join([str(t[Tbgi.BSN]) for t in self.tbgi if not pd.isna(t[Tbgi.BSN])])

    def get_tbgi_owns(self) -> str:
        return ', '.join([str(t[Tbgi.OWN]) for t in self.tbgi if not pd.isna(t[Tbgi.OWN])])

    def add_leerling(self, leerling: Leerling):
        self.leerling.append(leerling)

    def add_tbgi_regel(self, tbgi: pd.Series):
        self.tbgi.append(tbgi)
