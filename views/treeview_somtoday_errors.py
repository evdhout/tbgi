import tkinter as tk
from tkinter import Tk, Toplevel, font
from tkinter import ttk
from datetime import datetime

import pandas as pd

from models.fout import Fout
from models.leerling import Leerling
from models.somtoday import Somtoday
from views.treeview_base import TreeviewBase, ColumnDef


class SomtodayErrorView(TreeviewBase):

    def __init__(self, master: Toplevel or Tk):
        columns: [ColumnDef] = [
            ColumnDef("LLNR", "LLnr", 50, tk.W),
            ColumnDef("NAME", "Naam", 200, tk.W),
            ColumnDef("GROUP", "Groep", 45, tk.W),
            ColumnDef("BSN", "BSN", 100, tk.W),
            ColumnDef("OWN", "OWN", 100, tk.W),
            ColumnDef("STAT", "Status", 150, tk.W),
            ColumnDef("DINL", "Datum in Nederland", 110, tk.W),
            ColumnDef("ERROR", "Foutmelding", 500, tk.W)
        ]
        super(SomtodayErrorView, self).__init__(master=master, columns=columns)

    def display_errors(self, fouten: [Fout]):
        # empty the current version of the tree
        self.empty_tree()

        # populate the error tree
        odd_row = True
        fout: Fout
        for fout in fouten:
            leerling: Somtoday = fout.leerling[0].somtoday

            tags = ('odd_row', ) if odd_row else ('even_row', )

            self.error_tree.insert(parent='', index='end',
                                   iid=str(leerling[Somtoday.LEERLINGNUMMER]),
                                   text=str(leerling[Somtoday.LEERLINGNUMMER]),
                                   values=(leerling[Somtoday.LEERLINGNUMMER],
                                           leerling[Somtoday.VOLLEDIGE_NAAM],
                                           leerling[Somtoday.STAMGROEP],
                                           leerling[Somtoday.BSN] if leerling.has_bsn() else '',
                                           leerling[Somtoday.OWN] if leerling.has_own() else '',
                                           leerling[Somtoday.CATEGORIE],
                                           leerling[Somtoday.DATUM_IN_NEDERLAND].strftime("%Y-%m-%d"),
                                           fout.MELDING[fout.fout]),
                                   tags=tags)

            odd_row = not odd_row

