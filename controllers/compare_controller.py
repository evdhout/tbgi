import pandas as pd

from models.fout import Fout
from models.leerling import Leerling
from models.settings import Settings
from models.somtoday import Somtoday
from models.tbgi import Tbgi
from models.telling_status import TellingStatus


class Vergelijk:
    VERGELIJKING = {'tbgi': {'van': 'TBGI', 'met': 'Somtoday'},
                    'somtoday': {'van': 'Somtoday', 'met': 'TBGI'}}

    def __init__(self, somtoday: pd.DataFrame, tbgi: pd.DataFrame, options: Settings):
        self.options: Settings = options
        self.soort: str = options.soort
        self.somtoday: pd.DataFrame = somtoday
        self.tbgi: pd.DataFrame = tbgi
        self.tbgi_fouten: [Fout] = []
        self.somtoday_fouten: [Fout] = []
        self.fouten: {str: [Fout]} = {Leerling.TBGI: [], Leerling.SOMTODAY: []}
        self.telling: {str: {str: int}} = {Leerling.TBGI: {}, Leerling.SOMTODAY: {}}
        self.telling_tbgi_leerlingen: {int: [Tbgi]} = {}
        self.leerlingen: {int: Leerling} = {}

    def check_tbgi(self):
        self.options.message("#### TBGI vergelijken met Somtoday")
        fouten = self.fouten['tbgi']

        for tbgi in [Tbgi(tbgi=row) for row in self.tbgi.itertuples()]:
            tbgi_category = tbgi[Tbgi.CATEGORIE]
            tbgi_bsn = tbgi[Tbgi.BSN]
            tbgi_own = tbgi[Tbgi.OWN]

            self.telling['tbgi'][tbgi_category] = self.telling['tbgi'].get(tbgi_category, 0) + 1

            # zoek de leerling in somtoday op BSN of OWN
            sll: pd.DataFrame
            sll = self.somtoday[self.somtoday.BSN == tbgi_bsn]
            if sll.empty:
                sll = self.somtoday[self.somtoday.Onderwijsnummer == tbgi_own]

            if sll.empty:
                fouten.append(Fout(fout=Fout.ONBEKENDE_LEERLING_TBGI,
                                   bron=Fout.TBGI,
                                   tbgi=tbgi))
                continue
            elif 1 < len(sll):
                fouten.append(Fout(fout=Fout.MEERVOUDIGE_LEERLING,
                                   bron=Fout.TBGI,
                                   tbgi=tbgi,
                                   leerling=[Leerling(s) for s in sll.itertuples()]
                                   )
                              )
                continue

            # we weten zeker dat er maar 1 rij in het dataframe zit
            leerling = [Leerling(s) for s in sll.itertuples()][0]
            self.telling_tbgi_leerlingen[leerling.somtoday[Somtoday.LEERLINGNUMMER]].append(tbgi)
            if not TellingStatus.is_gelijk(leerling.somtoday[Somtoday.CATEGORIE], tbgi_category):
                fouten.append(Fout(fout=Fout.LEERLING_NIET_GELIJK,
                                   bron=Fout.TBGI,
                                   leerling=leerling,
                                   tbgi=tbgi))
            if (self.options.regeling == Settings.REGELING_DINL
                    and tbgi[Tbgi.DATUM_BINNENKOMST_IN_NL] != leerling.somtoday[Somtoday.DATUM_IN_NEDERLAND]):
                fouten.append(Fout(fout=Fout.DINL_NIET_GELIJK,
                                   bron=Fout.TBGI,
                                   leerling=leerling,
                                   tbgi=tbgi))
            if len(self.telling_tbgi_leerlingen[leerling.somtoday[Somtoday.LEERLINGNUMMER]]) > 1:
                fouten.append(
                    Fout(fout=Fout.LEERLING_MEER_KEER_GETELD_IN_TBGI,
                         bron=Fout.TBGI,
                         leerling=leerling,
                         tbgi=self.telling_tbgi_leerlingen[leerling.somtoday[Somtoday.LEERLINGNUMMER]]
                         )
                )
                fouten.append(
                    Fout(fout=Fout.LEERLING_MEER_KEER_GETELD_IN_TBGI,
                         bron=Fout.TBGI,
                         leerling=leerling,
                         tbgi=[x
                               for x
                               in reversed(self.telling_tbgi_leerlingen[leerling.somtoday[Somtoday.LEERLINGNUMMER]])
                               ]
                         )
                )

    def _add_leerling(self, leerling: Leerling, id_type: str = Leerling.BSN):
        if id_type == Leerling.BSN:
            ll_has_id = leerling.has_bsn()
            ll_id = leerling.bsn
            fout_code = Fout.MEERDERE_LEERLINGEN_BSN
        else:
            ll_has_id = leerling.has_own()
            ll_id = leerling.own
            fout_code = Fout.MEERDERE_LEERLINGEN_OWN

        if ll_has_id:
            if ll_id in self.leerlingen[id_type].keys():
                return Fout(fout=fout_code,
                            bron=Fout.SOMTODAY,
                            leerling=[leerling, self.leerlingen[id_type[ll_id]]]
                            )
            else:
                self.leerlingen[id_type][ll_id] = leerling

    def check_somtoday(self):
        self.options.message("#### Somtoday vergelijken met TBG-i")
        fouten = self.fouten['somtoday']
        for leerling in [Leerling(info=row, source=Leerling.SOMTODAY) for row in self.somtoday.itertuples()]:
            self.leerlingen[leerling.somtoday[Somtoday.LEERLINGNUMMER]] = Leerling
            self.telling_tbgi_leerlingen[leerling.somtoday[Somtoday.LEERLINGNUMMER]] = []
            ll_cat = leerling.somtoday[Somtoday.CATEGORIE]

            self.telling[Leerling.SOMTODAY][ll_cat] = self.telling[Leerling.SOMTODAY].get(ll_cat, 0) + 1

            tll: pd.DataFrame or None = None
            if leerling.has_bsn():
                tll = self.tbgi[self.tbgi.BSN == leerling.bsn]
            if tll is None or tll.empty:
                if leerling.has_own():
                    tll = self.tbgi[self.tbgi.OWN == leerling.own]
                    if not tll.empty and leerling.has_bsn():
                        fouten.append(Fout(fout=Fout.MATCH_OWN_MET_BSN,
                                           bron=Fout.SOMTODAY,
                                           leerling=leerling,
                                           tbgi=[Tbgi(t) for t in tll.itertuples()]
                                           )
                                      )

            if tll is None or tll.empty:
                if TellingStatus.is_actief(ll_cat) and (ll_cat[:8] != 'Regulier' or self.soort == 'regulier'):
                    fouten.append(Fout(fout=Fout.ONBEKENDE_LEERLING_SOMTODAY,
                                       bron=Fout.SOMTODAY,
                                       leerling=leerling))
                continue
            elif 1 < len(tll):
                fout = Fout(fout=Fout.MEERVOUDIGE_LEERLING,
                            bron=Fout.SOMTODAY,
                            leerling=leerling,
                            tbgi=[Tbgi(t) for t in tll.itertuples()])
                fouten.append(fout)
                continue

            for tbgi in [Tbgi(t) for t in tll.itertuples()]:
                if not TellingStatus.is_gelijk(ll_cat, tbgi.data['categorie']):
                    fouten.append(Fout(fout=Fout.LEERLING_NIET_GELIJK,
                                       bron=Fout.SOMTODAY,
                                       leerling=leerling,
                                       tbgi=tbgi))

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
