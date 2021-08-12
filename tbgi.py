#!python3

from models.options import Options
from controllers.compare_controller import Vergelijk
from controllers.options_controller import OptionsController
from controllers.tbgi_controller import TbgiController
from controllers.somtoday_controller import SomtodayController
from controllers.window_controller import WindowController
from views.app_view import AppView

if __name__ == '__main__':
    options = OptionsController(program_type='window').options
    windows = WindowController(options=options)
