from views.app_view import AppView
from views.messagebox import MessageBox
from models.options import Options
from controllers.tbgi_controller import TbgiController, Tbgi
from controllers.somtoday_controller import SomtodayController, Somtoday
from controllers.compare_controller import Vergelijk
from functions.path_checks import file_exists


class WindowController:
    def __init__(self, options: Options):
        self.options = options
        self.app_view = AppView(options=self.options)
        self.app_view.vergelijk_button.configure(command=self.compare)
        self.app_view.mainloop()
        self.vergelijk: Vergelijk or None = None
        self.tbgi: Tbgi or None = None
        self.somtoday: Somtoday or None = None

    def compare(self, part: int = 0):
        if part == 0:
            self.app_view.disable_all_input()
            settings: dict = self.app_view.get_input()
            try:
                settings['tbgi'] = file_exists(settings['tbgi'])
                settings['somtoday'] = file_exists(settings['somtoday'])
            except FileNotFoundError as e:
                MessageBox.show_error(str(e))
                return

            self.options.update_settings(**settings)

            self.app_view.update_progress(message='Inlezen TBGI bestand', percentage=5)
        elif part == 1:
            self.tbgi = TbgiController(options=self.options).tbgi
            self.app_view.update_progress(message='Inlezen Somtoday bestand', percentage=20)
        elif part == 2:
            self.somtoday = SomtodayController(options=self.options).somtoday
            self.app_view.update_progress(message='Initialiseren van vergelijking', percentage=40)
        elif part == 3:
            self.vergelijk = Vergelijk(tbgi=self.tbgi, somtoday=self.somtoday, options=self.options)
            self.app_view.update_progress(message='TBGI met Somtoday vergelijken', percentage=60)
        elif part == 4:
            self.vergelijk.check_tbgi()
            self.app_view.update_progress(message='Somtoday met TBGI vergelijken', percentage=80)
        elif part == 5:
            self.vergelijk.check_somtoday()
            self.app_view.update_progress(message='Vergelijking afgerond', percentage=100)
            self.app_view.display(self.vergelijk.telling, self.vergelijk.fouten)
            self.app_view.enable_all_input()
            self.vergelijk = None
            self.tbgi = None
            self.somtoday = None
        if part < 6:
            self.app_view.after(10, lambda: self.compare(part=part + 1))
