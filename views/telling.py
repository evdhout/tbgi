import tkinter as tk
from tkinter import Tk, Toplevel, font
from tkinter import ttk

from models.telling_status import TellingStatus as ts


class TellingView:
    ROWS = [ts.CATEGORIE_1, ts.CATEGORIE_2, ts.REGULIER, ts.REGULIER_NL, ts.NIET_BEKOSTIGBAAR,
            ts.NIET_INGESCHREVEN, ts.NIET_NAAR_BRON, ts.UITWISSELING, ts.INBURGERING]

    def __init__(self, master: Toplevel or Tk):
        self.master = master

        style = ttk.Style(self.master)
        table_font = font.nametofont(style.lookup(style='TLabel', option='font')).copy()
        table_font.configure(weight='bold')
        style.configure('TableHeader.TLabel', background='grey', foreground='white',
                        font=table_font, padding=[2, 5, 2, 5])
        style.configure('TableDataOdd.TLabel', padding=[2, 5, 2, 5], background='white')
        style.configure('TableDataEven.TLabel', padding=[2, 5, 2, 5], background='#ccc')

        style.configure('Table.TFrame', background="black")
        self.table_frame = ttk.Frame(self.master, style='Table.TFrame')
        self.table_frame.grid(row=0, column=0, padx=5, pady=5, sticky=tk.NE)

        self.header_empty = ttk.Label(master=self.table_frame, text='', width=20,
                                      style='TableHeader.TLabel', anchor=tk.CENTER)
        self.header_tbgi = ttk.Label(master=self.table_frame, text='TBGI', width=10,
                                     style='TableHeader.TLabel', anchor=tk.CENTER)
        self.header_somtoday = ttk.Label(master=self.table_frame, text='Somtoday', width=10,
                                         style='TableHeader.TLabel', anchor=tk.CENTER)
        self.header_empty.grid(row=0, column=0, padx=1, pady=1, sticky=tk.NSEW)
        self.header_tbgi.grid(row=0, column=1, padx=1, pady=1, sticky=tk.NSEW)
        self.header_somtoday.grid(row=0, column=2, padx=1, pady=1, sticky=tk.NSEW)

        self.rows: {str: {str: ttk.Label}} = {}
        for i in range(len(TellingView.ROWS)):
            label = TellingView.ROWS[i]
            self.rows[label] = {}
            self.rows[label]['header'] = (ttk.Label(master=self.table_frame,
                                                    text=TellingView.ROWS[i], style='TableHeader.TLabel'))
            self.rows[label]['header'].grid(row=i+1, column=0, padx=1, pady=1, sticky=tk.NSEW)

            if i % 2 == 0:
                style = 'TableDataEven.TLabel'
            else:
                style = 'TableDataOdd.TLabel'

            self.rows[label]['tbgi'] = ttk.Label(master=self.table_frame, width=20, text=' ',
                                                 style=style, anchor=tk.CENTER)
            self.rows[label]['tbgi'].grid(row=i+1, column=1, padx=1, pady=1, sticky=tk.NSEW)
            self.rows[label]['somtoday'] = ttk.Label(master=self.table_frame, width=20, text=' ',
                                                     style=style, anchor=tk.CENTER)
            self.rows[label]['somtoday'].grid(row=i+1, column=2, padx=1, pady=1, sticky=tk.NSEW)

    def display_telling(self, telling: {str: {str: int}}):
        for i in range(len(TellingView.ROWS)):
            label = TellingView.ROWS[i]

            self.rows[label]['tbgi'].configure(text=telling['tbgi'].get(label, ' '))
            self.rows[label]['somtoday'].configure(text=telling['somtoday'].get(label, ' '))
