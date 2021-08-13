from tkinter import messagebox


class MessageBox:
    def __init__(self):
        pass

    @staticmethod
    def show_error(message: str, title: str = 'Foutmelding', detail: str = None,):
        messagebox.showerror(message=message, title=title, icon='error', detail=detail)
