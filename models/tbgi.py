import pandas as pd

from models.options import Options
from models.telling_status import TellingStatus
from models.signaal import Signaal


class Tbgi:
    COLUMN_TYPES = {"REGEL_NUMMER": 'Int64',
                    "BSN": 'Int64',
                    "OWN": 'Int64',
                    "SOORT_TELDATUM": 'category',
                    "BEKOSTIGINGSJAAR": 'Int16',
                    "VESTIGING": 'category',
                    "OPLEIDINGCODE": 'category',
                    "LEERJAAR": 'category',
                    "BEKOSTIGINGSSTATUS": 'category',
                    "CATEGORIE_NK": 'category',
                    "SIGNAAL_1": 'category',
                    "SL_OMSCHRIJVING_1": 'category',
                    "PARAMETER_11": 'string',
                    "PARAMETER_12": 'string',
                    "PARAMETER_13": 'string',
                    "PARAMETER_14": 'string',
                    "PARAMETER_15": 'string',
                    "SIGNAAL_2": 'category',
                    "SL_OMSCHRIJVING_2": 'category',
                    "PARAMETER_21": 'string',
                    "PARAMETER_22": 'string',
                    "PARAMETER_23": 'string',
                    "PARAMETER_24": 'string',
                    "PARAMETER_25": 'string',
                    "SIGNAAL_3": 'category',
                    "SL_OMSCHRIJVING_3": 'category',
                    "PARAMETER_31": 'string',
                    "PARAMETER_32": 'string',
                    "PARAMETER_33": 'string',
                    "PARAMETER_34": 'string',
                    "PARAMETER_35": 'string',
                    "SIGNAAL_4": 'category',
                    "SL_OMSCHRIJVING_4": 'category',
                    "PARAMETER_41": 'string',
                    "PARAMETER_42": 'string',
                    "PARAMETER_43": 'string',
                    "PARAMETER_44": 'string',
                    "PARAMETER_45": 'string',
                    "SIGNAAL_5": 'category',
                    "SL_OMSCHRIJVING_5": 'category',
                    "PARAMETER_51": 'string',
                    "PARAMETER_52": 'string',
                    "PARAMETER_53": 'string',
                    "PARAMETER_54": 'string',
                    "PARAMETER_55": 'string',
                    }
    DATE_COLUMNS = ["TELDATUM", "DATUM_BINNENKOMST_IN_NL"]
    BOOL_COLUMNS = ["INDICATIE_BEKOSTIGBAAR", "INDICATIE_NK_KORTER_DAN_JAAR"]
    LOCATION = '03XF05'

    def __init__(self, tbgi: pd.DataFrame):
        self.tbgi = tbgi
