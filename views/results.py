import tkinter as tk
from tkinter import Tk, Toplevel, Text
from tkinter import ttk

from views.telling import TellingView


class ResultsView:
    def __init__(self, master: Toplevel or Tk,
                 row: int = 1, column: int = 0,
                 width: int = 800, height: int = 400):
        self.master = master

        self.notebook = ttk.Notebook(self.master, width=width, height=height)
        self.count_frame = ttk.Frame(self.notebook)

        self.tbgi_frame = ttk.Frame(self.notebook)
        self.somtoday_frame = ttk.Frame(self.notebook)

        self.notebook.add(self.count_frame, text='Telling')
        self.notebook.add(self.tbgi_frame, text='TBGI')
        self.notebook.add(self.somtoday_frame, text='Somtoday')

        self.notebook.grid(row=row, column=column)

        self.tbgi_text = Text(self.tbgi_frame, state='disabled', width=100, height=24, wrap='none')
        self.tbgi_text_ys = ttk.Scrollbar(self.tbgi_frame, orient='vertical', command=self.tbgi_text.yview)
        self.tbgi_text_xs = ttk.Scrollbar(self.tbgi_frame, orient='horizontal', command=self.tbgi_text.xview)
        self.tbgi_text['xscrollcommand'] = self.tbgi_text_xs.set
        self.tbgi_text['yscrollcommand'] = self.tbgi_text_ys.set

        self.tbgi_text.grid(row=0, column=0)
        self.tbgi_text_xs.grid(row=1, column=0, sticky=tk.NS)
        self.tbgi_text_ys.grid(row=0, column=1, sticky=tk.EW)

        self.somtoday_text = Text(self.somtoday_frame, state='disabled', width=100, height=24, wrap='none')
        self.somtoday_text_ys = ttk.Scrollbar(self.somtoday_frame, orient='vertical',
                                              command=self.somtoday_text.yview)
        self.somtoday_text_xs = ttk.Scrollbar(self.somtoday_frame, orient='horizontal',
                                              command=self.somtoday_text.xview)
        self.somtoday_text['xscrollcommand'] = self.somtoday_text_xs.set
        self.somtoday_text['yscrollcommand'] = self.somtoday_text_ys.set

        self.somtoday_text.grid(row=0, column=0)
        self.somtoday_text_xs.grid(row=1, column=0, sticky=tk.NS)
        self.somtoday_text_ys.grid(row=0, column=1, sticky=tk.EW)

        self.telling = TellingView(master=self.count_frame)

    def display_results(self, telling, fouten):
        self.telling.display_telling(telling)

        aantal_tbgi_fouten = len(fouten['tbgi'])
        self.notebook.tab(1, text=f'TBGI ({aantal_tbgi_fouten})')
        self.tbgi_text.configure(state='normal')
        self.tbgi_text.delete('1.0', 'end')
        for fout in fouten['tbgi']:
            self.tbgi_text.insert('end', f'{fout}\n')
        self.tbgi_text.configure(state='disabled')

        aantal_somtoday_fouten = len(fouten['somtoday'])
        self.notebook.tab(2, text=f'Somtoday ({aantal_somtoday_fouten})')
        self.somtoday_text.configure(state='normal')
        self.somtoday_text.delete('1.0', 'end')
        for fout in fouten['somtoday']:
            self.somtoday_text.insert('end', f'{fout}\n')
        self.somtoday_text.configure(state='disabled')
