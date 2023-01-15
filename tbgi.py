#!python3
from controllers.settings_controller import SettingsController
from controllers.window_controller import WindowController

if __name__ == '__main__':
    settings = SettingsController(program_type='window').settings
    windows = WindowController(settings=settings)
