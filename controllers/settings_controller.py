import argparse
import configparser
from datetime import date

from models.settings import Settings
from functions.path_checks import argparse_file_exists, directory_exists


class SettingsController:
    def __init__(self, program_type: str = 'cli'):
        self.call_type = program_type

        if 'cli' == program_type:
            args = SettingsController.parse_arguments()
        else:
            args = SettingsController.read_ini()
        self.settings = Settings(**args)

    @staticmethod
    def read_ini():
        ini_settings = {}
        config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
        config.read('tbgi.ini')

        ini_settings['debug'] = config.getboolean('TBGI', 'debug', fallback=False)
        ini_settings['debug'] = True
        initial_directory = config.get('TBGI', 'initial directory', fallback=None)
        if initial_directory is not None:
            ini_settings['initial directory'] = directory_exists(initial_directory)
        tbgi_file = config.get('TBGI', 'tbgi', fallback=None)
        if tbgi_file is not None:
            ini_settings['tbgi'] = tbgi_file
        somtoday_file = config.get('TBGI', 'somtoday', fallback=None)
        if somtoday_file is not None:
            ini_settings['somtoday'] = somtoday_file
        ini_settings['vestiging'] = config.get('TBGI', 'vestiging', fallback=None)
        return ini_settings

    @staticmethod
    def parse_arguments():
        parser = argparse.ArgumentParser(description="Lees de TBG-i, bereken aantallen en vergelijk met Somtoday.",
                                         add_help=False)
        parser.add_argument('-h', '--help', action='help', help='toon dit bericht en stop')
        parser.add_argument('-s', '--soort',
                            choices=['regulier', 'r', 'nieuwkomer', 'n'],
                            default='nieuwkomer',
                            help='verwerk reguliere of nieuwkomer bekostiging')
        parser.add_argument('-t', '--teldatum',
                            choices=['okt', 'jan', 'apr', 'jul'],
                            default='okt',
                            help='welke teldatum moet verwerkt worden?')
        parser.add_argument('-b', '--bekostigingsjaar',
                            default=date.today().year,
                            type=int,
                            help='in welk jaar ligt de teldatum?')
        parser.add_argument('-v', '--vestiging',
                            type=str,
                            help='de vestiging (BRIN+2) waarvoor de TBG-i moet worden verwerkt')
        parser.add_argument('-d', '--debug',
                            help="toon extra informatie tijdens verwerking",
                            action="store_true")
        parser.add_argument('tbgi',
                            type=argparse_file_exists,
                            help="het csv-bestand met de TBG-i")
        parser.add_argument('somtoday',
                            type=argparse_file_exists,
                            help="het csv-bestand met de export uit Somtoday")
        args = parser.parse_args()
        return vars(args)
