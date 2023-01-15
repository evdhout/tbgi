class TellingStatus:
    NIET_INGESCHREVEN = "Niet ingeschreven"
    NIET_BEKOSTIGBAAR = "Niet bekostigbaar"
    NIET_NAAR_BRON = "Niet verzenden naar BRON"
    NIET_NAAR_BRON_NIET_BEKOSTIGBAAR = "Niet naar BRON en niet bekostigbaar"
    DUBBELE_INSCHRIJVING = "Niet bekostigbaar, dubbele inschrijving"
    INBURGERING = "Inburgering"
    UITWISSELING = "Uitwisseling"
    REGULIER_NL = "Regulier NL"
    REGULIER = "Regulier"
    CATEGORIE_1 = "Categorie 1"
    CATEGORIE_2 = "Categorie 2"

    TBGI_ONBEKEND = "Onbekend"

    ALT_NIET_INGESCHREVEN = [NIET_INGESCHREVEN, INBURGERING, UITWISSELING]
    ALT_REGULIER = [REGULIER, REGULIER_NL]

    @staticmethod
    def is_gelijk(s1: str, s2: str) -> bool:
        if s1 == s2:
            return True
        elif s1 in TellingStatus.ALT_REGULIER and s2 in TellingStatus.ALT_REGULIER:
            return True
        elif s1 in TellingStatus.ALT_NIET_INGESCHREVEN and s2 in TellingStatus.ALT_NIET_INGESCHREVEN:
            return True
        else:
            return False

    @staticmethod
    def is_actief(categorie: str) -> bool:
        return categorie not in TellingStatus.ALT_NIET_INGESCHREVEN
