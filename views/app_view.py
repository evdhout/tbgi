import tkinter as tk
from tkinter import Tk, StringVar, IntVar, filedialog
from tkinter import ttk

from models.options import Options
from views.results import ResultsView


class AppView(Tk):
    def __init__(self, options: Options):
        super().__init__()
        self.options = options
        self.initial_directory = options.initial_directory
        self.active_file_selectors = False

        self.title("Vergelijk TBGI met Somtoday")

        self.app_frame = ttk.Frame(self)
        self.app_frame.grid(column=0, row=0, sticky="N", padx=5, pady=5)

        self.config_frame = ttk.LabelFrame(self.app_frame, text='Instellingen vergelijking', width=800, height=250)
        self.config_frame.grid(column=0, row=0, sticky="N")
        self.config_frame.grid_propagate(0)

        self.tbgi_label = ttk.Label(master=self.config_frame, text='TBGI bestand:')
        self.tbgi_filename_string = StringVar(master=self, name='TBGI filename')
        self.tbgi_filename_string.set(self.options.get('tbgi', 'Kies TBGI bestand'))
        self.tbgi_filename_string.trace('w', self.validate)
        self.tbgi_filename_label = ttk.Label(master=self.config_frame, textvariable=self.tbgi_filename_string)
        self.tbgi_label.grid(row=0, column=0, sticky="E")
        self.tbgi_filename_label.grid(row=0, column=1, sticky="W")

        self.somtoday_label = ttk.Label(master=self.config_frame, text='Somtoday bestand:', style='Bold.TLabel')
        self.somtoday_filename_string = StringVar(self, name='Somtoday filename')
        self.somtoday_filename_string.set(self.options.get('somtoday', 'Kies Somtoday bestand'))
        self.somtoday_filename_string.trace('w', self.validate)
        self.somtoday_filename_label = ttk.Label(master=self.config_frame, textvariable=self.somtoday_filename_string)
        self.somtoday_label.grid(row=1, column=0, sticky="E")
        self.somtoday_filename_label.grid(row=1, column=1, sticky="W")

        self.soort_teldatum_label = ttk.Label(master=self.config_frame, text='Soort teldatum:')
        self.soort_teldatum_string = StringVar(self, name='Soort teldatum')
        self.soort_teldatum_string.set(options.soort)
        self.soort_teldatum_string.trace('w', self.change_soort_teldatum)
        self.soort_teldatum_frame = ttk.Frame(master=self.config_frame)
        self.soort_teldatum_nieuwkomer = ttk.Radiobutton(master=self.soort_teldatum_frame, text=Options.NIEUWKOMER,
                                                         variable=self.soort_teldatum_string, value=Options.NIEUWKOMER)
        self.soort_teldatum_regulier = ttk.Radiobutton(master=self.soort_teldatum_frame, text=Options.REGULIER,
                                                       variable=self.soort_teldatum_string, value=Options.REGULIER)
        self.soort_teldatum_label.grid(row=2, column=0, sticky="E")
        self.soort_teldatum_frame.grid(row=2, column=1, sticky="W")
        self.soort_teldatum_nieuwkomer.grid(row=0, column=0, sticky="W")
        self.soort_teldatum_regulier.grid(row=0, column=1, sticky="W")

        self.bekostigingsjaar_label = ttk.Label(master=self.config_frame, text='Bekostigingsjaar:')
        self.bekostigingsjaar_string = StringVar(self, name='Bekostigingsjaar')
        self.bekostigingsjaar_string.set(options.bekostigingsjaar)
        self.bekostigingsjaar_spinbox = ttk.Spinbox(master=self.config_frame,
                                                    from_=2018, to=2100, increment=1,
                                                    textvariable=self.bekostigingsjaar_string)
        self.bekostigingsjaar_label.grid(row=3, column=0, sticky="E")
        self.bekostigingsjaar_spinbox.grid(row=3, column=1, sticky="W")

        self.teldatum_frame = ttk.Frame(master=self.config_frame)
        self.teldatum_label = ttk.Label(master=self.config_frame, text='Teldatum:')
        self.teldatum_int = IntVar(master=self, name='Teldatum')
        self.teldatum_int.set(options.teldatum.month)
        self.teldatum_jan = ttk.Radiobutton(master=self.teldatum_frame, text=Options.MAAND_NAAM[Options.JANUARI],
                                            variable=self.teldatum_int, value=Options.JANUARI)
        self.teldatum_apr = ttk.Radiobutton(master=self.teldatum_frame, text=Options.MAAND_NAAM[Options.APRIL],
                                            variable=self.teldatum_int, value=Options.APRIL)
        self.teldatum_jul = ttk.Radiobutton(master=self.teldatum_frame, text=Options.MAAND_NAAM[Options.JULI],
                                            variable=self.teldatum_int, value=Options.JULI)
        self.teldatum_okt = ttk.Radiobutton(master=self.teldatum_frame, text=Options.MAAND_NAAM[Options.OKTOBER],
                                            variable=self.teldatum_int, value=Options.OKTOBER)
        self.teldatum_label.grid(row=4, column=0, sticky="E")
        self.teldatum_frame.grid(row=4, column=1, sticky="W")
        self.teldatum_jan.grid(row=0, column=1, sticky="W")
        self.teldatum_apr.grid(row=0, column=2, sticky="W", pady=2)
        self.teldatum_jul.grid(row=0, column=3, sticky="W", pady=2)
        self.teldatum_okt.grid(row=0, column=4, sticky="W", pady=2)

        self.vergelijk_button = ttk.Button(master=self.config_frame, text="Vergelijk")
        self.vergelijk_button.grid(row=10, column=1, sticky="W")

        self.loading_string = StringVar(master=self, name='Loading text')
        self.loading_string.set('')
        self.loading_label = ttk.Label(master=self.config_frame, textvariable=self.loading_string)
        self.loading_progress_percentage = IntVar(master=self, name='Progress')
        self.loading_progress_percentage.set(0)
        self.loading_progress = ttk.Progressbar(master=self.config_frame, orient=tk.HORIZONTAL,
                                                length=500, mode='determinate',
                                                variable=self.loading_progress_percentage)
        self.loading_label.grid(row=11, column=1, sticky="W")
        self.loading_progress.grid(row=12, column=1, sticky="W")

        self.results_notebook = ResultsView(master=self.app_frame, width=800, height=400)

        self.enable_all_input()

    def validate(self, *args):
        if self.tbgi_filename_string.get() != 'Kies TBGI bestand' \
                and self.somtoday_filename_string.get() != 'Kies Somtoday bestand':
            self.vergelijk_button.state(['!disabled'])
        else:
            self.vergelijk_button.state(['disabled'])

    def change_soort_teldatum(self, *args):
        if self.soort_teldatum_string.get() == Options.REGULIER:
            self.teldatum_jan.configure(state=tk.DISABLED)
            self.teldatum_apr.configure(state=tk.DISABLED)
            self.teldatum_jul.configure(state=tk.DISABLED)
            self.teldatum_int.set(Options.OKTOBER)
        else:
            self.teldatum_jan.configure(state=tk.NORMAL)
            self.teldatum_apr.configure(state=tk.NORMAL)
            self.teldatum_jul.configure(state=tk.NORMAL)

    def toggle_file_selectors(self, active: bool = True):
        if active and not self.active_file_selectors:
            self.somtoday_filename_label.bind("<Button-1>",
                                              lambda e: self.set_filename(filename_string=self.somtoday_filename_string,
                                                                          title='Kies Somtoday bestand',
                                                                          filetype='somtoday'))
            self.tbgi_filename_label.bind("<Button-1>",
                                          lambda e: self.set_filename(filename_string=self.tbgi_filename_string,
                                                                      title='Kies TBGI bestand',
                                                                      filetype='tbgi'))
        elif not active and self.active_file_selectors:
            self.somtoday_filename_label.bind("Button-1>", None)
            self.tbgi_filename_label.bind("<Button-1>", None)

        self.active_file_selectors = active

    def disable_all_input(self):
        self.vergelijk_button.state([tk.DISABLED])
        self.toggle_file_selectors(active=False)
        self.soort_teldatum_regulier.configure(state=tk.DISABLED)
        self.soort_teldatum_nieuwkomer.configure(state=tk.DISABLED)
        self.teldatum_jan.configure(state=tk.DISABLED)
        self.teldatum_apr.configure(state=tk.DISABLED)
        self.teldatum_jul.configure(state=tk.DISABLED)
        self.teldatum_okt.configure(state=tk.DISABLED)
        self.bekostigingsjaar_spinbox.configure(state=tk.DISABLED)

    def enable_all_input(self):
        self.toggle_file_selectors(active=True)
        self.soort_teldatum_regulier.configure(state=tk.NORMAL)
        self.soort_teldatum_nieuwkomer.configure(state=tk.NORMAL)
        self.bekostigingsjaar_spinbox.configure(state=tk.NORMAL)
        self.teldatum_okt.configure(state=tk.NORMAL)
        self.change_soort_teldatum()
        self.validate()

    def set_filename(self, filename_string: StringVar, title: str = 'Kies bestand',
                     filetype: str = 'tbgi'):
        if filetype == 'tbgi':
            filetypes = [('TBGI', '.csv'), ('Alle bestanden', "*.*")]
        else:
            filetypes = [('Somtoday', '.xlsx'), ('Alle bestanden', "*.*")]
        filename = filedialog.askopenfilename(filetypes=filetypes,
                                              title=title,
                                              initialdir=self.initial_directory)
        print(filename)
        if filename:
            filename_string.set(filename)

    def update_progress(self, message: str, percentage: int):
        self.options.message(message)
        self.loading_string.set(message)
        self.loading_progress_percentage.set(percentage)

    def get_tbgi_filename(self) -> str:
        return self.tbgi_filename_string.get()

    def get_somtoday_filename(self) -> str:
        return self.somtoday_filename_string.get()

    def get_bekostigingsjaar(self) -> str:
        return self.bekostigingsjaar_string.get()

    def get_soort_teldatum(self) -> str:
        return self.soort_teldatum_string.get()

    def get_teldatum(self) -> int:
        return self.teldatum_int.get()

    def get_input(self) -> dict:
        return {'bekostigingsjaar': self.bekostigingsjaar_string.get(),
                'soort': self.soort_teldatum_string.get(),
                'teldatum': self.teldatum_int.get(),
                'tbgi': self.tbgi_filename_string.get(),
                'somtoday': self.somtoday_filename_string.get()}

    def display(self, telling, fouten):
        self.results_notebook.display_results(telling, fouten)
