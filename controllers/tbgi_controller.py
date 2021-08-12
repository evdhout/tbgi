import pandas as pd

from models.options import Options
from models.categorie import Categorie
from models.tbgi import Tbgi


class TbgiController:
    def __init__(self, options: Options):
        print(options.tbgi)
        df_tbgi = pd.read_csv(options.tbgi,
                              index_col=False,
                              usecols=[*Tbgi.COLUMN_TYPES.keys(), *Tbgi.DATE_COLUMNS, *Tbgi.BOOL_COLUMNS],
                              dtype=Tbgi.COLUMN_TYPES,
                              true_values=['J', 'j', 'Ja', 'ja', 'JA'],
                              false_values=['N', 'n', 'Nee', 'nee', 'NEE'],
                              parse_dates=Tbgi.DATE_COLUMNS,
                              sep=';'
                              )

        c = Categorie(options)
        df_tbgi['categorie'] = df_tbgi.apply(lambda x: c.get_category_tbgi(x['SIGNAAL_1'],
                                                                           x['CATEGORIE_NK'],
                                                                           x['INDICATIE_BEKOSTIGBAAR']
                                                                           ),
                                             axis=1
                                             ).astype('category')

        self.tbgi = Tbgi(df_tbgi[(df_tbgi['VESTIGING'] == Tbgi.LOCATION)
                                 & (df_tbgi['SOORT_TELDATUM'] == options.soort.upper())
                                 & (df_tbgi['TELDATUM'].dt.date == options.teldatum)])
