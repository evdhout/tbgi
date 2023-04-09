import tkinter as tk
from tkinter import Tk, Toplevel, Text
from tkinter import ttk

from views.telling import TellingView
from views.treeview_tbgi_errors import TbgiErrorView
from views.treeview_somtoday_errors import SomtodayErrorView


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

        self.notebook.grid(row=row, column=column, sticky="NSEW")

        self.telling = TellingView(master=self.count_frame)
        self.tbgi = TbgiErrorView(master=self.tbgi_frame)
        self.somtoday = SomtodayErrorView(master=self.somtoday_frame)

    def display_results(self, telling, fouten):
        self.telling.display_telling(telling)

        aantal_tbgi_fouten = len(fouten['tbgi'])
        self.notebook.tab(1, text=f'TBGI ({aantal_tbgi_fouten})')
        self.tbgi.display_errors(fouten=fouten['tbgi'])

        aantal_somtoday_fouten = len(fouten['somtoday'])
        self.notebook.tab(2, text=f'Somtoday ({aantal_somtoday_fouten})')
        self.somtoday.display_errors(fouten=fouten['somtoday'])


