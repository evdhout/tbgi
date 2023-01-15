class SomtodayBestand:
    LEERLINGNUMMER = 'Leerlingnummer'
    VOLLEDIGE_NAAM = 'Naam'
    VOLLEDIGE_NAAM_XLSX = 'Volledige Naam'
    STAMGROEP = 'Stamgroep'
    DATUM_IN_NEDERLAND = 'DatumInNL'
    DATUM_IN_NEDERLAND_XLSX = 'Datum in Nederland'
    BSN = 'BSN'
    OWN = 'Onderwijsnummer'
    EERSTE_NATIONALITEIT = 'Nationaliteit'
    EERSTE_NATIONALITEIT_XLSX = 'Eerste Nationaliteit'
    BEKOSTIGING = 'Bekostiging'
    NIET_VERSTUREN_NAAR_BRON = 'BRON'
    NIET_VERSTUREN_NAAR_BRON_XLSX = 'Niet versturen naar BRON J/N'
    INSCHRIJFDATUM = 'Inschrijfdatum'
    UITSCHRIJFDATUM = 'Uitschrijfdatum'
    PLAATSING_ACTIEF = 'PlaatsingActief'
    PLAATSING_ACTIEF_XLSX = 'Plaatsing actief op peildatum'
    PLAATSING_VANAF_DATUM = 'PlaatsingVanafdatum'
    PLAATSING_VANAF_DATUM_XLSX = 'Plaatsing Vanafdatum'
    PLAATSING_TOT_DATUM = 'PlaatsingTotdatum'
    PLAATSING_TOT_DATUM_XLSX = 'Plaatsing Totdatum'

    COLUMNS = {LEERLINGNUMMER, VOLLEDIGE_NAAM_XLSX, STAMGROEP, DATUM_IN_NEDERLAND_XLSX, BSN, OWN,
               EERSTE_NATIONALITEIT_XLSX, BEKOSTIGING, NIET_VERSTUREN_NAAR_BRON_XLSX, INSCHRIJFDATUM, UITSCHRIJFDATUM,
               PLAATSING_ACTIEF_XLSX, PLAATSING_VANAF_DATUM_XLSX, PLAATSING_TOT_DATUM_XLSX}

    COLUMN_TYPES = {LEERLINGNUMMER: 'Int32',
                    VOLLEDIGE_NAAM_XLSX: str,
                    STAMGROEP: 'category',
                    BSN: 'Int64',
                    OWN: 'Int64',
                    EERSTE_NATIONALITEIT_XLSX: 'category',
                    BEKOSTIGING: 'category',
                    NIET_VERSTUREN_NAAR_BRON_XLSX: bool,
                    PLAATSING_ACTIEF_XLSX: bool,
                    }

    DATE_COLUMNS = [DATUM_IN_NEDERLAND_XLSX, INSCHRIJFDATUM, UITSCHRIJFDATUM,
                    PLAATSING_VANAF_DATUM_XLSX, PLAATSING_TOT_DATUM_XLSX]

    TRUE_VALUES = ['J', 'j', 1]
    FALSE_VALUES = ['N', 'n', 0]

    COLUMN_RENAME = {VOLLEDIGE_NAAM_XLSX: VOLLEDIGE_NAAM,
                     DATUM_IN_NEDERLAND_XLSX: DATUM_IN_NEDERLAND,
                     EERSTE_NATIONALITEIT_XLSX: EERSTE_NATIONALITEIT,
                     NIET_VERSTUREN_NAAR_BRON_XLSX: NIET_VERSTUREN_NAAR_BRON,
                     PLAATSING_ACTIEF_XLSX: PLAATSING_ACTIEF,
                     PLAATSING_VANAF_DATUM_XLSX: PLAATSING_VANAF_DATUM,
                     PLAATSING_TOT_DATUM_XLSX: PLAATSING_TOT_DATUM
                     }
