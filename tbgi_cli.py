#!python3

from models.options import Settings
from controllers.compare_controller import Vergelijk
from controllers.options_controller import SettingsController
from controllers.tbgi_controller import TbgiController
from controllers.somtoday_controller import SomtodayController


if __name__ == '__main__':
    options: Settings = SettingsController(program_type='cli').settings
    if options.debug:
        print(options)

    options.message(f"Inlezen van '{options.data}'")
    tbgi = TbgiController(options).data
    options.message("TBGI ingelezen")

    options.message(f"Inlezen van '{options.data}'")
    somtoday = SomtodayController(options).data
    options.message("Somtoday ingelezen")

    vergelijk: Vergelijk = Vergelijk(somtoday=somtoday, tbgi=tbgi, options=options)
    vergelijk.check_tbgi()
    vergelijk.check_somtoday()
    vergelijk.print_results()

    print()
    print("PANDAS TELLING VOLGT TER CONTROLE")
    print("---")
    print("Telling TBGI")
    print(tbgi.data['categorie'].value_counts())
    print("---")
    print("Telling Somtoday")
    print(somtoday.data['categorie'].value_counts())
