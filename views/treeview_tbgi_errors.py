import tkinter as tk
from tkinter import Tk, Toplevel
from tkinter import ttk

import pandas as pd

from models.fout import Fout
from models.tbgi import Tbgi
from views.treeview_base import TreeviewBase, ColumnDef


class TbgiErrorView(TreeviewBase):

    def __init__(self, master: Toplevel or Tk):
        columns: [ColumnDef] = [
            ColumnDef("ROWNO", "Regel", 50, tk.W),
            ColumnDef("BSN", "BSN", 100, tk.W),
            ColumnDef("OWN", "OWN", 100, tk.W),
            ColumnDef("LLnr", "LLnr", 50, tk.W),
            ColumnDef("ERROR", "Foutmelding", 400, tk.W, True)
        ]
        super(TbgiErrorView, self).__init__(master=master, columns=columns)

        self.tbgi: {str: Tbgi} = {}

        self.bind_detail_view(self.show_tbgi_detail)

    def show_tbgi_detail(self, _event):
        tbgi = self.tbgi[int(self.error_tree.selection()[0])]
        detail_frame = self.create_detail_window(title=f"TBG-I details regel {tbgi['REGEL_NUMMER']}")

        row_number = 1

        for tbgi_field in [x for x in [Tbgi.CATEGORIE] + Tbgi.CSV_HEADER]:
            tbgi_value = tbgi[tbgi_field]
            if not pd.isna(tbgi_value):
                value: str
                if tbgi_field in Tbgi.BOOL_COLUMNS:
                    value = "J" if tbgi_value else "N"
                else:
                    value = str(tbgi_value)

                label: str
                if tbgi_field == Tbgi.CATEGORIE:
                    label = 'Categorie o.b.v. TBG-i'
                else:
                    label = str(tbgi_field)
                ttk.Label(master=detail_frame, text=label,
                          width=30, style='TableHeader.TLabel', anchor=tk.NE
                          ).grid(row=row_number, column=0, padx=1, pady=1, sticky=tk.NSEW)
                ttk.Label(master=detail_frame, text=value,
                          width=50, style='TableDataOdd.TLabel', anchor=tk.NW,
                          wraplength=450, justify=tk.LEFT
                          ).grid(row=row_number, column=1, padx=1, pady=1, sticky=tk.NSEW)
                row_number += 1

    def display_errors(self, fouten: [Fout]):
        self.empty_tree()
        self.tbgi = {}

        # populate the error tree
        odd_row = True
        for fout in fouten:
            tbgi = fout.tbgi[0]
            fout_regel = tbgi[Tbgi.REGEL_NUMMER]
            fout_bsn = tbgi[Tbgi.BSN]
            fout_own = tbgi[Tbgi.OWN]

            self.tbgi[fout_regel] = tbgi

            bsn = '' if pd.isna(fout_bsn) else fout_bsn
            own = '' if pd.isna(fout_own) else fout_own
            ll_nr = ''

            if len(fout.leerling) > 0:
                ll_nr = ', '.join([str(ll.ll_nr) for ll in fout.leerling])

            tags = ('odd_row', ) if odd_row else ('even_row', )
            self.error_tree.insert(parent='', index='end',
                                   iid=fout_regel,
                                   text=fout_regel,
                                   values=(fout_regel, bsn, own, ll_nr, fout.MELDING[fout.fout]),  # str(fout)
                                   tags=tags)

            odd_row = not odd_row
