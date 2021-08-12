#!python3

from models.options import Options
from controllers.compare_controller import Vergelijk
from controllers.options_controller import OptionsController
from controllers.tbgi_controller import TbgiController
from controllers.somtoday_controller import SomtodayController


if __name__ == '__main__':
    options: Options = OptionsController(program_type='cli').options
    if options.verbose:
        print(options)

    options.message(f"Inlezen van '{options.tbgi}'")
    tbgi = TbgiController(options).tbgi
    options.message("TBGI ingelezen")

    options.message(f"Inlezen van '{options.somtoday}'")
    somtoday = SomtodayController(options).somtoday
    options.message("Somtoday ingelezen")

    vergelijk: Vergelijk = Vergelijk(somtoday=somtoday, tbgi=tbgi, options=options)
    vergelijk.check_tbgi()
    vergelijk.check_somtoday()
    vergelijk.print_results()

    print()
    print("PANDAS TELLING VOLGT TER CONTROLE")
    print("---")
    print("Telling TBGI")
    print(tbgi.tbgi['categorie'].value_counts())
    print("---")
    print("Telling Somtoday")
    print(somtoday.somtoday['categorie'].value_counts())
