import pandas as pd

from models.fout import Fout
from models.leerling import Leerling
from models.options import Options
from models.somtoday import Somtoday
from models.tbgi import Tbgi
from models.telling_status import TellingStatus


class Vergelijk:
    VERGELIJKING = {'tbgi': {'van': 'TBGI', 'met': 'Somtoday'},
                    'somtoday': {'van': 'Somtoday', 'met': 'TBGI'}}

    def __init__(self, somtoday: Somtoday, tbgi: Tbgi, options: Options):
        self.options: Options = options
        self.soort: str = options.soort
        self.somtoday: pd.DataFrame = somtoday.somtoday
        self.tbgi: pd.DataFrame = tbgi.tbgi
        self.tbgi_fouten: [Fout] = []
        self.somtoday_fouten: [Fout] = []
        self.fouten: {str: [Fout]} = {'tbgi': [], 'somtoday': []}
        self.telling: {str: {str: int}} = {'tbgi': {}, 'somtoday': {}}

    def check_tbgi(self):
        self.options.message("#### TBGI vergelijken met Somtoday")
        fouten = self.fouten['tbgi']
        for _, tbgi_row in self.tbgi.iterrows():
            self.telling['tbgi'][tbgi_row['categorie']] = self.telling['tbgi'].get(tbgi_row['categorie'], 0) + 1

            # zoek de leerling in somtoday op BSN of OWN
            sll: pd.DataFrame
            sll = self.somtoday[self.somtoday.BSN == tbgi_row['BSN']]
            if sll.empty:
                sll = self.somtoday[self.somtoday.OWN == tbgi_row['OWN']]

            if sll.empty:
                fouten.append(Fout(fout=Fout.ONBEKENDE_LEERLING,
                                   bron=Fout.TBGI,
                                   tbgi=tbgi_row))
                continue
            elif 1 < len(sll):
                fout = Fout(fout=Fout.MEERVOUDIGE_LEERLING,
                            bron=Fout.TBGI,
                            tbgi=tbgi_row)

                for _, ll_row in sll.iterrows():
                    fout.add_leerling(Leerling(leerling=ll_row))

                fouten.append(fout)
                continue

            # we weten zeker dat er maar 1 rij in het dataframe zit
            ll: Leerling = Leerling()
            for _, ll_row in sll.iterrows():
                ll.init_series(leerling=ll_row)

            if not TellingStatus.is_gelijk(ll.categorie, tbgi_row['categorie']):
                fouten.append(Fout(fout=Fout.LEERLING_NIET_GELIJK,
                                   bron=Fout.TBGI,
                                   leerling=ll,
                                   tbgi=tbgi_row))

    def check_somtoday(self):
        self.options.message("#### Somtoday vergelijken met TBGI")
        fouten = self.fouten['somtoday']
        for _, somtoday_row in self.somtoday.iterrows():
            sll = Leerling(somtoday_row)
            self.telling['somtoday'][sll.categorie] = self.telling['somtoday'].get(sll.categorie, 0) + 1

            tll: pd.DataFrame or None = None
            if not pd.isna(sll.BSN):
                tll = self.tbgi[self.tbgi.BSN == sll.BSN]
            if tll is None or tll.empty:
                if not pd.isna(sll.OWN):
                    tll = self.tbgi[self.tbgi.OWN == sll.OWN]

            if tll is None or tll.empty:
                if sll.is_actief() and (sll.categorie[:8] != 'Regulier' or self.soort == 'regulier'):
                    fouten.append(Fout(fout=Fout.ONBEKENDE_LEERLING,
                                       bron=Fout.SOMTODAY,
                                       leerling=sll))
                continue
            elif 1 < len(tll):
                fout = Fout(fout=Fout.MEERVOUDIGE_LEERLING,
                            bron=Fout.SOMTODAY,
                            leerling=sll)
                for _, tbgi_row in tll.iterrows():
                    fout.add_tbgi_regel(tbgi_row)
                fouten.append(fout)
                continue

            for _, tll_row in tll.iterrows():
                if not TellingStatus.is_gelijk(sll.categorie, tll_row['categorie']):
                    fouten.append(Fout(fout=Fout.LEERLING_NIET_GELIJK,
                                       bron=Fout.SOMTODAY,
                                       leerling=sll,
                                       tbgi=tll_row))

    def print_fouten(self, bron: str):
        fouten = self.fouten[bron]
        aantal_fouten = len(fouten)
        print(f'{aantal_fouten} fout{"en" if aantal_fouten != 1 else ""} in vergelijking van '
              f'{Vergelijk.VERGELIJKING[bron]["van"]} met {Vergelijk.VERGELIJKING[bron]["met"]}')
        for fout in fouten:
            print(fout)

    def print_telling(self):
        tellingen = [TellingStatus.CATEGORIE_1, TellingStatus.CATEGORIE_2, TellingStatus.REGULIER,
                     TellingStatus.REGULIER_NL, TellingStatus.NIET_BEKOSTIGBAAR, TellingStatus.NIET_INGESCHREVEN,
                     TellingStatus.NIET_NAAR_BRON, TellingStatus.UITWISSELING, TellingStatus.INBURGERING]
        print(f'    TBGI  Somtoday  Status')

        for telling in tellingen:
            print(f'{self.telling["tbgi"].get(telling, ""):8}  '
                  f'{self.telling["somtoday"].get(telling, ""):8}  {telling}')

    def print_results(self):
        for bron in ['tbgi', 'somtoday']:
            self.print_fouten(bron=bron)
        self.print_telling()
