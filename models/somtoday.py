import pandas as pd


class Somtoday:
    COLUMN_TYPES = {'Leerlingnummer': 'Int32',
                    'Volledige Naam': str,
                    'BSN': 'Int64',
                    'Onderwijsnummer': 'Int64',
                    'Eerste nationaliteit': 'category',
                    'Stamgroep': 'category',
                    'Bekostiging': 'category',
                    'Niet versturen naar BRON J/N': bool
                    }

    # DATE_COLUMNS = ['Datum in Nederland', 'Inschrijfdatum', 'Uitschrijfdatum']
    DATE_COLUMNS = ['Datum in Nederland', 'Inschrijfdatum']

    COLUMN_NAMES = {'Leerlingnummer': 'llno',
                    'Volledige Naam': 'naam',
                    'Onderwijsnummer': 'OWN',
                    'Eerste Nationaliteit': 'nat',
                    'Stamgroep': 'stam',
                    'Bekostiging': 'bek',
                    'Datum in Nederland': 'dinl',
                    'Inschrijfdatum': 'begin',
                    'Uitschrijfdatum': 'eind',
                    'Niet versturen naar BRON J/N': 'bron'
                    }

    def __init__(self, somtoday: pd.DataFrame):
        self.somtoday: pd.DataFrame = somtoday
