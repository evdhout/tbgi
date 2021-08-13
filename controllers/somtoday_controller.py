import warnings
import pandas as pd
import numpy as np

from models.somtoday import Somtoday
from models.options import Options
from models.categorie import Categorie


class SomtodayController:
    def __init__(self, options: Options):
        somtoday: pd.DataFrame

        if options.somtoday[-4:] == 'xlsx':
            with warnings.catch_warnings(record=True):
                warnings.simplefilter("always")
                somtoday: pd.DataFrame = pd.read_excel(options.somtoday,
                                                       header=0,
                                                       index_col=False,
                                                       dtype=Somtoday.COLUMN_TYPES,
                                                       parse_dates=Somtoday.DATE_COLUMNS,
                                                       true_values=['J'],
                                                       false_values=['N'],
                                                       engine='openpyxl'
                                                       )
        else:
            somtoday: pd.DataFrame = pd.read_csv(options.somtoday,
                                                 header=0,
                                                 index_col=False,
                                                 dtype=Somtoday.COLUMN_TYPES,
                                                 parse_dates=Somtoday.DATE_COLUMNS,
                                                 true_values=['J'],
                                                 false_values=['N'],
                                                 )

        somtoday.rename(columns=Somtoday.COLUMN_NAMES, inplace=True)
        if 'eind' not in somtoday.columns:
            somtoday['eind'] = np.nan
        else:
            somtoday['eind'] = pd.to_datetime(somtoday['eind'])
        if 'OWN' not in somtoday.columns:
            somtoday['OWN'] = np.nan
        if 'bron' not in somtoday.columns:
            somtoday['bron'] = np.nan

        # self.somtoday.eind.fillna(date(self.options.bekostigingsjaar, 12, 31), inplace=True)
        c = Categorie(options)
        somtoday['categorie'] = somtoday.apply(lambda x: c.get_category_somtoday(x['dinl'].date(),
                                                                                 x['nat'],
                                                                                 x['begin'].date(),
                                                                                 x['eind'].date(),
                                                                                 x['bek'],
                                                                                 x['stam'],
                                                                                 x['bron']),
                                               axis=1
                                               ).astype('category')

        self.somtoday: Somtoday = Somtoday(somtoday)
