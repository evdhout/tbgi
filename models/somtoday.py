import pandas as pd
from models.somtoday_bestand import SomtodayBestand
from collections import namedtuple


class Somtoday(SomtodayBestand):
    CATEGORIE = 'categorie'

    def __init__(self, somtoday: namedtuple):
        self.data: dict = somtoday._asdict()

    def __getitem__(self, item):
        return self.data[item]

    def has_bsn(self) -> bool:
        return not pd.isna(self.data[Somtoday.BSN])

    def has_own(self) -> bool:
        return not pd.isna(self.data[Somtoday.OWN])

