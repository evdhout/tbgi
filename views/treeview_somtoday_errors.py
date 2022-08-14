import tkinter as tk
from tkinter import Tk, Toplevel, font
from tkinter import ttk

import pandas as pd

from models.fout import Fout
from models.leerling import Leerling
from views.treeview_base import TreeviewBase, ColumnDef


class SomtodayErrorView(TreeviewBase):

    def __init__(self, master: Toplevel or Tk):
        columns: [ColumnDef] = [
            ColumnDef("LLNO", "LLno", 50, tk.W),
            ColumnDef("NAME", "Naam", 200, tk.W),
            ColumnDef("GROUP", "Groep", 45, tk.W),
            ColumnDef("BSN", "BSN", 100, tk.W),
            ColumnDef("OWN", "OWN", 100, tk.W),
            ColumnDef("STAT", "Status", 150, tk.W),
            ColumnDef("ERROR", "Foutmelding", 400, tk.W)
        ]
        super(SomtodayErrorView, self).__init__(master=master, columns=columns)

    def display_errors(self, fouten: [Fout]):
        # empty the current version of the tree
        self.empty_tree()

        # populate the error tree
        odd_row = True
        fout: Fout
        for fout in fouten:
            somtoday: Leerling = fout.leerling[0]

            tags = ('odd_row', ) if odd_row else ('even_row', )
            self.error_tree.insert(parent='', index='end',
                                   iid=str(somtoday.llno),
                                   text=str(somtoday.llno),
                                   values=(somtoday.llno,
                                           somtoday.naam,
                                           somtoday.stam,
                                           somtoday.BSN if not pd.isna(somtoday.BSN) else '',
                                           somtoday.OWN if not pd.isna(somtoday.OWN) is not None else '',
                                           somtoday.categorie,
                                           fout.MELDING[fout.fout]),
                                   tags=tags)

            odd_row = not odd_row

