from datetime import date, datetime


class Options:
    NIEUWKOMER = 'nieuwkomer'
    REGULIER = 'regulier'

    SOORT_TELDATUM = {
        'n': 'nieuwkomer',
        'nieuwkomer': 'nieuwkomer',
        'r': 'regulier',
        'regulier': 'regulier'
    }

    JANUARI = 1
    APRIL = 4
    JULI = 7
    OKTOBER = 10

    MAAND_NAAM = {1: 'januari', 4: 'april', 7: 'juli', 10: 'oktober'}
    MAAND_AFKORTING = {1: 'jan', 4: 'apr', 7: 'jul', 10: 'okt'}
    MAANDNUMMER_TELDATUM = {'jan': 1, 'apr': 4, 'jul': 7, 'okt': 10}
    TELDATUM_PER_MAAND = [None, 'jan', 'jan', 'jan', 'apr', 'apr', 'apr', 'jul', 'jul', 'jul', 'okt', 'okt', 'okt']

    def __init__(self, **kwargs):
        # config options read from ini only
        self.verbose: bool = kwargs.get('verbose', False)
        self.initial_directory: str or None = kwargs.get('initial directory', None)

        # options read from command line or from window
        self.tbgi: str or None = None
        self.somtoday: str or None = None
        self.today = datetime.now()
        self.bekostigingsjaar: int = self.today.year
        self.teldatum_naam: str = Options.TELDATUM_PER_MAAND[self.today.month]
        self.soort: str = Options.NIEUWKOMER
        self.teldatum: date or None = None
        self.peildatum_cat1: date or None = None
        self.peildatum_cat2: date or None = None

        self.update_settings(**kwargs)

    def update_settings(self, **kwargs):
        self.tbgi = kwargs.get('tbgi', None)
        self.somtoday = kwargs.get('somtoday', None)
        self.bekostigingsjaar = int(kwargs.get('bekostigingsjaar', self.today.year))

        self.verbose = kwargs.get('verbose', self.verbose)

        teldatum = kwargs.get('teldatum', self.today.month)
        try:
            self.teldatum_naam = Options.TELDATUM_PER_MAAND[teldatum]
        except KeyError:
            self.teldatum_naam = teldatum
        except TypeError:
            self.teldatum_naam = teldatum

        try:
            self.soort: str or None = Options.SOORT_TELDATUM[kwargs.get('soort', Options.NIEUWKOMER)]
        except KeyError:
            raise TypeError(f"Incorrect type teldatum '{self.soort}'.")

        if Options.NIEUWKOMER == self.soort:
            self.teldatum = date(self.bekostigingsjaar, self.MAANDNUMMER_TELDATUM[self.teldatum_naam], 1)
        else:
            self.teldatum = date(self.bekostigingsjaar - 1, 10, 1)

        self.peildatum_cat1 = date(self.bekostigingsjaar - 2, 10, 1)
        self.peildatum_cat2 = date(self.bekostigingsjaar - 2, self.MAANDNUMMER_TELDATUM[self.teldatum_naam], 1)

    def __str__(self):
        return (f"TBGI             = {self.tbgi}\n"
                f"Somtoday         = {self.somtoday}\n"
                f"Bekostigingsjaar = {self.bekostigingsjaar}\n"
                f"Teldatum naam    = {self.teldatum_naam}\n"
                f"Teldatum         = {self.teldatum}\n"
                f"Soort teldatum   = {self.soort}\n"
                f"Peildatum cat1   = {self.peildatum_cat1}\n"
                f"Peildatum cat2   = {self.peildatum_cat2}\n"
                f"Verbose          = {self.verbose}")

    def message(self, message: str):
        if self.verbose:
            print(message)

    def is_regulier(self) -> bool:
        return self.soort == 'regulier'

    def get(self, option: str, default=None):
        value = getattr(self, option, None)
        if value is None:
            return default
        else:
            return value
