import warnings
import pandas as pd
import numpy as np

from models.somtoday import Somtoday
from models.settings import Settings
from models.categorie import Categorie
from models.somtoday_bestand import SomtodayBestand


class SomtodayCsvController:
    def __init__(self, settings: Settings):
        somtoday: pd.DataFrame

        if settings.somtoday[-4:] == 'xlsx':
            with warnings.catch_warnings(record=True):
                warnings.simplefilter("always")
                somtoday: pd.DataFrame = pd.read_excel(settings.somtoday,
                                                       header=0,
                                                       index_col=False,
                                                       usecols=SomtodayBestand.COLUMNS,
                                                       dtype=SomtodayBestand.COLUMN_TYPES,
                                                       parse_dates=SomtodayBestand.DATE_COLUMNS,
                                                       true_values=['J', 1],
                                                       false_values=['N', 0],
                                                       engine='openpyxl'
                                                       )
        else:
            somtoday: pd.DataFrame = pd.read_csv(settings.somtoday,
                                                 header=0,
                                                 index_col=False,
                                                 usecols=SomtodayBestand.COLUMNS,
                                                 dtype=Somtoday.COLUMN_TYPES,
                                                 parse_dates=Somtoday.DATE_COLUMNS,
                                                 true_values=['J', 1],
                                                 false_values=['N', 0],
                                                 )

        somtoday.rename(columns=Somtoday.COLUMN_RENAME, inplace=True)

        c = Categorie(settings)
        somtoday[Somtoday.CATEGORIE] = \
            somtoday.apply(lambda x: c.get_category_somtoday(dinl=x[Somtoday.DATUM_IN_NEDERLAND].date(),
                                                             oinl=x[Somtoday.NEDERLANDS_ONDERWIJS_SINDS].date(),
                                                             nat=x[Somtoday.EERSTE_NATIONALITEIT],
                                                             begin=x[Somtoday.PLAATSING_VANAF_DATUM].date(),
                                                             eind=x[Somtoday.PLAATSING_TOT_DATUM].date(),
                                                             bek=x[Somtoday.BEKOSTIGING],
                                                             stam=x[Somtoday.STAMGROEP],
                                                             bron=x[Somtoday.NIET_VERSTUREN_NAAR_ROD]),
                           axis=1
                           ).astype('category')

        self.somtoday: pd.DataFrame = somtoday
