import platform
import tkinter as tk
from tkinter import Tk, StringVar, IntVar, filedialog, font
from tkinter import ttk
from views.icon import b64icon

from models.settings import Settings
from views.results import ResultsView


class AppView(Tk):
    def __init__(self, settings: Settings):
        super().__init__()
        self.settings = settings
        self.initial_directory = settings.initial_directory
        self.active_file_selectors = False
        self.iconphoto(True, tk.PhotoImage(data=b64icon))

        self.title("Vergelijk TBG-I met Somtoday")

        # setup styling
        style = ttk.Style()

        # use classic theme if not on windows
        if platform.system != 'Windows':
            style.theme_use('classic')

        # set up table layout, with striping.
        table_font = font.nametofont(style.lookup(style='TLabel', option='font')).copy()
        table_font.configure(weight='bold')
        style.configure('TableHeader.TLabel', background='grey', foreground='white',
                        font=table_font, padding=[2, 5, 2, 5])
        style.configure('TableDataOdd.TLabel', padding=[2, 5, 2, 5], background='white')
        style.configure('TableDataEven.TLabel', padding=[2, 5, 2, 5], background='#ccc')
        style.configure('Table.TFrame', background="black")

        # set up treeview layout
        style.configure("Treeview",
                        background="white",
                        foreground="black",
                        rowheight=25,
                        fieldbackground="white")
        style.map('Treeview',
                  background=[('selected', '#3677A8')],
                  foreground=[('selected', 'white')])

        self.columnconfigure(index=0, weight=1)
        self.rowconfigure(index=0, weight=1)

        res_x = self.winfo_screenwidth()
        res_y = self.winfo_screenheight()
        win_x = 1320 if res_x > 1320 else res_x
        win_y = res_y - 200
        self.settings.message(f'Windows size / screen resolution = {win_x} x {win_y} / {res_x}x{res_y} ')

        self.app_frame = ttk.Frame(self, width=win_x, height=win_y)
        self.app_frame.columnconfigure(index=0, weight=1)
        self.app_frame.rowconfigure(index=0, weight=0)  # do not extend config frame
        self.app_frame.rowconfigure(index=1, weight=1)  # do extend result frame

        self.app_frame.grid(column=0, row=0, sticky="NSEW", padx=5, pady=5)
        self.app_frame.grid_propagate(False)

        self.config_frame = ttk.LabelFrame(self.app_frame, text='Instellingen vergelijking', height=250)
        self.config_frame.grid(column=0, row=0, sticky="EW")
        self.config_frame.grid_propagate(False)

        self.tbgi_label = ttk.Label(master=self.config_frame, text='TBGI bestand:')
        self.tbgi_filename_string = StringVar(master=self, name='TBGI filename')
        self.tbgi_filename_string.set(self.settings.get('tbgi', 'Kies TBGI bestand'))
        self.tbgi_filename_string.trace('w', self.validate)
        self.tbgi_filename_label = ttk.Label(master=self.config_frame, textvariable=self.tbgi_filename_string)
        self.tbgi_label.grid(row=0, column=0, sticky="E")
        self.tbgi_filename_label.grid(row=0, column=1, sticky="W")

        self.somtoday_label = ttk.Label(master=self.config_frame, text='Somtoday bestand:', style='Bold.TLabel')
        self.somtoday_filename_string = StringVar(self, name='Somtoday filename')
        self.somtoday_filename_string.set(self.settings.get('somtoday', 'Kies Somtoday bestand'))
        self.somtoday_filename_string.trace('w', self.validate)
        self.somtoday_filename_label = ttk.Label(master=self.config_frame, textvariable=self.somtoday_filename_string)
        self.somtoday_label.grid(row=1, column=0, sticky="E")
        self.somtoday_filename_label.grid(row=1, column=1, sticky="W")

        self.soort_teldatum_label = ttk.Label(master=self.config_frame, text='Soort teldatum:')
        self.soort_teldatum_string = StringVar(self, name='Soort teldatum')
        self.soort_teldatum_string.set(settings.soort)
        self.soort_teldatum_string.trace('w', self.change_soort_teldatum)
        self.soort_teldatum_frame = ttk.Frame(master=self.config_frame)
        self.soort_teldatum_nieuwkomer = ttk.Radiobutton(master=self.soort_teldatum_frame, text=Settings.NIEUWKOMER,
                                                         variable=self.soort_teldatum_string, value=Settings.NIEUWKOMER)
        self.soort_teldatum_regulier = ttk.Radiobutton(master=self.soort_teldatum_frame, text=Settings.REGULIER,
                                                       variable=self.soort_teldatum_string, value=Settings.REGULIER)
        self.soort_teldatum_label.grid(row=2, column=0, sticky="E")
        self.soort_teldatum_frame.grid(row=2, column=1, sticky="W")
        self.soort_teldatum_nieuwkomer.grid(row=0, column=0, sticky="W")
        self.soort_teldatum_regulier.grid(row=0, column=1, sticky="W")

        self.bekostigingsjaar_label = ttk.Label(master=self.config_frame, text='Bekostigingsjaar:')
        self.bekostigingsjaar_string = StringVar(self, name='Bekostigingsjaar')
        self.bekostigingsjaar_string.set(str(settings.bekostigingsjaar))
        self.bekostigingsjaar_spinbox = ttk.Spinbox(master=self.config_frame,
                                                    from_=2018, to=2100, increment=1,
                                                    textvariable=self.bekostigingsjaar_string)
        self.bekostigingsjaar_label.grid(row=3, column=0, sticky="E")
        self.bekostigingsjaar_spinbox.grid(row=3, column=1, sticky="W")

        self.teldatum_frame = ttk.Frame(master=self.config_frame)
        self.teldatum_label = ttk.Label(master=self.config_frame, text='Teldatum:')
        self.teldatum_int = IntVar(master=self, name='Teldatum')
        self.teldatum_int.set(settings.teldatum.month)
        self.teldatum_jan = ttk.Radiobutton(master=self.teldatum_frame, text=Settings.MAAND_NAAM[Settings.JANUARI],
                                            variable=self.teldatum_int, value=Settings.JANUARI)
        self.teldatum_apr = ttk.Radiobutton(master=self.teldatum_frame, text=Settings.MAAND_NAAM[Settings.APRIL],
                                            variable=self.teldatum_int, value=Settings.APRIL)
        self.teldatum_jul = ttk.Radiobutton(master=self.teldatum_frame, text=Settings.MAAND_NAAM[Settings.JULI],
                                            variable=self.teldatum_int, value=Settings.JULI)
        self.teldatum_okt = ttk.Radiobutton(master=self.teldatum_frame, text=Settings.MAAND_NAAM[Settings.OKTOBER],
                                            variable=self.teldatum_int, value=Settings.OKTOBER)
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

        self.results_notebook = ResultsView(master=self.app_frame, width=win_x, height=win_y - 450)

        self.enable_all_input()

    def validate(self, *_args):
        if self.tbgi_filename_string.get() != 'Kies TBGI bestand' \
                and self.somtoday_filename_string.get() != 'Kies Somtoday bestand':
            self.vergelijk_button.state(['!disabled', '!active', '!focus', '!hover'])
        else:
            self.vergelijk_button.state(['disabled', '!active', '!focus', '!hover'])

    def change_soort_teldatum(self, *_args):
        if self.soort_teldatum_string.get() == Settings.REGULIER:
            self.teldatum_jan.configure(state=tk.DISABLED)
            self.teldatum_apr.configure(state=tk.DISABLED)
            self.teldatum_jul.configure(state=tk.DISABLED)
            self.teldatum_int.set(Settings.OKTOBER)
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
        if filename:
            filename_string.set(filename)

    def update_progress(self, message: str, percentage: int):
        self.settings.message(message)
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
