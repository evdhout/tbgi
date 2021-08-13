#!python3
from controllers.options_controller import OptionsController
from controllers.window_controller import WindowController

if __name__ == '__main__':
    options = OptionsController(program_type='window').options
    windows = WindowController(options=options)
