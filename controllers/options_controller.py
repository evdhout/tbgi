import argparse
import configparser
from datetime import date

from models.options import Options
from functions.path_checks import argparse_file_exists, directory_exists


class OptionsController:
    def __init__(self, program_type: str = 'cli'):
        self.call_type = program_type

        if 'cli' == program_type:
            args = OptionsController.parse_arguments()
        else:
            args = OptionsController.read_ini()
        self.options = Options(**args)

    @staticmethod
    def read_ini():
        options = {}
        config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
        config.read('tbgi.ini')

        options['verbose'] = config.getboolean('DEFAULT', 'verbose', fallback=False)
        options['verbose'] = True
        initial_directory = config.get('DEFAULT', 'initial directory', fallback=None)
        if initial_directory is not None:
            options['initial directory'] = directory_exists(initial_directory)
        tbgi_file = config.get('DEFAULT', 'tbgi', fallback=None)
        if tbgi_file is not None:
            options['tbgi'] = tbgi_file
        somtoday_file = config.get('DEFAULT', 'somtoday', fallback=None)
        if somtoday_file is not None:
            options['somtoday'] = somtoday_file
        return options

    @staticmethod
    def parse_arguments():
        parser = argparse.ArgumentParser(description="Lees de TBGI, bereken aantallen en vergelijk met Somtoday.",
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
        parser.add_argument('-v', '--verbose',
                            help="toon extra informatie tijdens verwerking",
                            action="store_true")
        parser.add_argument('tbgi',
                            type=argparse_file_exists,
                            help="het csv-bestand met de tbgi")
        parser.add_argument('somtoday',
                            type=argparse_file_exists,
                            help="het csv-bestand met de export uit somtoday")
        args = parser.parse_args()
        return vars(args)
