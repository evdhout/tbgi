#!python3


from controllers.compare_controller import Vergelijk
from controllers.settings_controller import SettingsController
from controllers.tbgi_csv_controller import TbgiCsvController
from controllers.somtoday_csv_controller import SomtodayCsvController


if __name__ == '__main__':
    settings = SettingsController(program_type='cli').settings
    settings.message(settings)

    settings.message(f"Inlezen van '{settings.tbgi}'")
    tbgi = TbgiCsvController(settings=settings)

    settings.message(f"Inlezen van '{settings.somtoday}'")
    somtoday = SomtodayCsvController(settings=settings)

    vergelijk: Vergelijk = Vergelijk(somtoday=somtoday.somtoday, tbgi=tbgi.tbgi, options=settings)
    vergelijk.check_somtoday()
    vergelijk.check_tbgi()
    vergelijk.print_results()

    print()
    print("PANDAS TELLING VOLGT TER CONTROLE")
    print("---")
    print("Telling TBGI")
    print(tbgi.tbgi.data['categorie'].value_counts())
    print("---")
    print("Telling Somtoday")
    print(somtoday.somtoday.data['categorie'].value_counts())
