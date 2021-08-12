import pandas as pd


class Signaal:
    SIGNALEN = ['',
                'De inschrijving wordt niet bekostigd omdat de leerling op uw school niet ingeschreven is op de'
                ' teldatum.',
                'De inschrijving wordt niet bekostigd omdat uw school voor vestiging [1] niet de toestemming heeft om'
                ' deze opleiding te geven.',
                'De inschrijving wordt niet bekostigd omdat de vestiging [1] van uw school op de teldatum niet in'
                ' bedrijf is.',
                'De inschrijving wordt niet bekostigd omdat het opgegeven leerjaar[1] niet toegestaan is bij de'
                ' opleiding.',
                'De inschrijving wordt niet bekostigd omdat de leerling vanwege leeftijd geen praktijkonderwijs mag'
                ' volgen.',
                '',
                'Voor dezelfde leerling zijn een of meer andere inschrijvingen aanwezig bij'
                ' Brinnummer(s) [1] [2] [3] [4] [5].'
                ' Uw inschrijving wordt niet bekostigd omdat dit niet de meest recente is.',
                'Voor dezelfde leerling zijn een of meer andere inschrijvingen aanwezig bij'
                ' Brinnummer(s) [1] [2] [3] [4] [5].'
                ' Uw inschrijving komt voor bekostiging in aanmerking omdat dit de meest recente is.',
                'De inschrijving wordt door de indicatie bekostigbaar niet voor bekostiging in aanmerking gebracht'
                ' door uw school.',
                'De inschrijving betreft een nieuwkomer korter dan 1 jaar in Nederland.',
                'De inschrijving komt niet voor Nieuwkomerbekostiging in aanmerking omdat de leerling op grond van'
                ' verblijfsduur niet aangewezen kan zijn op het leerwegondersteunend onderwijs dan wel toelaatbaar kan'
                ' zijn tot praktijkonderwijs.',
                'Voor deze teldatum heeft DUO de bekostigingsstatus ambtshalve vastgesteld. Reden: [1]',
                'DUO heeft de eerder ambtshalve vastgestelde bekostigingsstatus voor deze teldatum verwijderd. Vanaf'
                ' nu wordt de bekostigingsstatus weer volgens de beslisregels statustoekenning bepaald. Reden: [1]'
                ]
    PARAMETERS = [0, 0, 1, 1, 1, 0, 0, 5, 5, 0, 0, 0, 1, 1]

    def __init__(self, signal_number: int, parameters: [str] or None = None):
        self.number: int = signal_number
        self.parameters: [str] or None = parameters

    def __str__(self):
        signal_string = f'{Signaal.SIGNALEN[self.number]} [{self.number}]'
        if self.parameters is not None:
            param_string = '\n'.join([f'  {s}' for s in self.parameters])
            return f'{signal_string}:\n{param_string}'
        return signal_string

    @staticmethod
    def show_signal(n: int, p: [str]) -> str:
        sig = f"{n} : {Signaal.SIGNALEN[n]}"
        for x in range(Signaal.PARAMETERS[n]):
            sig = sig.replace(f'[{x + 1}]', f'[{p[x]}]')
        return sig

    @staticmethod
    def show_signals(row: pd.Series):
        for n in range(1, 6):
            if pd.notna(row[f'SIGNAAL_{n}']):
                print("  ", Signaal.show_signal(pd.to_numeric(row[f'SIGNAAL_{n}']),
                                                [row[f'PARAMETER_{n}{n}'] for n in range(1, 6)]))

    @staticmethod
    def get_signals(row: pd.Series) -> ['Signaal']:
        signals: [Signaal] = []
        for n in range(1, 6):
            if pd.notna(row[f'SIGNAAL_{n}']):
                sno = row[f'SIGNAAL_{n}']
                signals.append(Signaal(signal_number=sno,
                                       parameters=Signaal.get_signal_parameters(sno, row)))
        return signals

    @staticmethod
    def get_signal_parameters(signaal: int, row: pd.Series) -> [str] or None:
        param_count = Signaal.PARAMETERS[signaal]
        if param_count > 0:
            return [row[f'PARAMETER_{signaal}{n}'] for n in range(1, param_count + 1)]
        return None
