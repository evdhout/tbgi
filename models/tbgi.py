import pandas as pd
from collections import namedtuple
from models.tbgi_bestand import TbgiBestand


class Tbgi(TbgiBestand):
    CATEGORIE = 'categorie'

    def __init__(self, tbgi: namedtuple):
        self.data: dict = tbgi._asdict()
        self.data[Tbgi.TBG_I_AANMAAK_DATUMTIJD_COL_NAME] = self.data[Tbgi.TBG_I_AANMAAK_DATUMTIJD]

    def __getitem__(self, item):
        return self.data[item]

    def has_bsn(self) -> bool:
        return not pd.isna(self.data[Tbgi.BSN])

    def has_own(self) -> bool:
        return not pd.isna(self.data[Tbgi.OWN])
