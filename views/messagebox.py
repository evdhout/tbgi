from tkinter import messagebox


class MessageBox:
    def __init__(self):
        pass

    @staticmethod
    def show_error(message: str):
        messagebox.showerror(message=message)
