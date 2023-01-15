import tkinter as tk
from tkinter import Tk, Toplevel, font
from tkinter import ttk

import pandas as pd

from models.fout import Fout


class ColumnDef:
    def __init__(self, col_id: str, col_label: str, col_width: int, col_align: str, col_stretch: bool = False):
        self.id: str = col_id
        self.width: int = col_width
        self.label: str = col_label
        self.align: str = col_align
        self.stretch: bool = col_stretch


class TreeviewBase:
    def __init__(self, master: Toplevel or Tk, columns: [ColumnDef]):
        self.master = master

        self.error_frame = ttk.Frame(master)
        self.error_frame.pack()

        error_scroll_y = tk.Scrollbar(self.error_frame)
        error_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        error_scroll_x = tk.Scrollbar(self.error_frame)
        error_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

        self.error_tree: ttk.Treeview = ttk.Treeview(self.error_frame,
                                                     columns=[c.id for c in columns],
                                                     selectmode="browse",
                                                     show="headings",
                                                     yscrollcommand=error_scroll_y.set,
                                                     xscrollcommand=error_scroll_x.set)

        for c in columns:
            self.error_tree.column(c.id, anchor=c.align, width=c.width, stretch=c.stretch)
            self.error_tree.heading(c.id, text=c.label, anchor=c.align)

        self.error_tree.tag_configure('odd_row', background="white")
        self.error_tree.tag_configure('even_row', background='#E8E8E8')

        self.error_tree.pack(pady=20)

        error_scroll_y.config(command=self.error_tree.yview)
        error_scroll_x.config(command=self.error_tree.xview)

        # self.error_tree.insert(parent='', index='end', iid="empty", values=("-", "-", "-"))

    def bind_detail_view(self, detail_function):
        self.error_tree.bind("<Double-1>", detail_function)

    def empty_tree(self):
        self.error_tree.delete(*self.error_tree.get_children())

    def create_detail_window(self, title: str) -> ttk.Frame:
        detail_view = Toplevel(self.master)
        detail_view.title(title)
        detail_view.geometry("800x600")

        detail_canvas = tk.Canvas(detail_view, background='grey')
        detail_frame = ttk.Frame(detail_canvas, style='Table.TFrame', padding=(5, 0))
        detail_scroll = tk.Scrollbar(detail_canvas, orient="vertical", command=detail_canvas.yview)
        detail_canvas.configure(yscrollcommand=detail_scroll.set)
        detail_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        detail_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        detail_canvas.create_window((4, 4), window=detail_frame, anchor=tk.NW)
        detail_frame.bind("<Configure>",
                          lambda e, canvas=detail_canvas: canvas.configure(scrollregion=canvas.bbox("all")))

        # return the frame to which the details will be added
        return detail_frame
