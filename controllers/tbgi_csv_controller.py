import pandas as pd

from models.settings import Settings
from models.categorie import Categorie
from models.tbgi import Tbgi


class TbgiCsvController:
    def __init__(self, settings: Settings):
        try:
            df_tbgi = pd.read_csv(settings.tbgi,
                                  index_col=False,
                                  usecols=Tbgi.CSV_HEADER,
                                  dtype=Tbgi.COLUMN_TYPES,
                                  true_values=Tbgi.TRUE_VALUES,
                                  false_values=Tbgi.FALSE_VALUES,
                                  parse_dates=[*Tbgi.DATE_COLUMNS, *Tbgi.DATETIME_COLUMNS],
                                  sep=';'
                                  )
        except ValueError as e:
            raise e

        # de kolom regel bevat een # als eerste teken, hier fixen we de kolomnaam
        df_tbgi.rename(columns={Tbgi.TBG_I_AANMAAK_DATUMTIJD_COL_NAME: Tbgi.TBG_I_AANMAAK_DATUMTIJD},
                       inplace=True)

        c = Categorie(settings)
        df_tbgi[Tbgi.CATEGORIE] = \
            df_tbgi.apply(lambda x: c.get_category_tbgi(x[Tbgi.SIGNAAL_1],
                                                        x[Tbgi.CATEGORIE_NK],
                                                        x[Tbgi.INDICATIE_BEKOSTIGBAAR] in Tbgi.TRUE_VALUES
                                                        ),
                          axis=1
                          ).astype('category')

        self.tbgi: pd.DataFrame = df_tbgi[(df_tbgi[Tbgi.VESTIGING] == settings.vestiging)
                                          & (df_tbgi[Tbgi.SOORT_TELDATUM] == settings.soort.upper())
                                          & (df_tbgi[Tbgi.TELDATUM].dt.date == settings.teldatum)]
