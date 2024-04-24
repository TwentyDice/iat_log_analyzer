<<<<<<< HEAD
# Manage GUI interactions
# Create and destroy a window per function, because I don't know how to use this properly, and am scared of memory leaks
import tkinter as tk
from tkinter import filedialog

_TITLE = "20Dice IAT Log Analyzer"

def show_error_msgbox(msg=None):
    root = tk.Tk()
    root.withdraw()
    tk.messagebox.showerror(title=_TITLE, message=msg)
    root.destroy()

    return


def get_dir_with_info_msgbox(msg=None):

    root = tk.Tk()
    root.withdraw()
    tk.messagebox.showinfo(
        title=_TITLE, message=msg, )
    dir = filedialog.askdirectory()
    root.destroy()

    return dir
=======
# Manage GUI interactions
# Create and destroy a window per function, because I don't know how to use this properly, and am scared of memory leaks
import tkinter as tk
from tkinter import filedialog

_TITLE = "20Dice IAT Log Analyzer"

def show_error_msgbox(msg=None):
    root = tk.Tk()
    root.withdraw()
    tk.messagebox.showerror(title=_TITLE, message=msg)
    root.destroy()

    return


def get_dir_with_info_msgbox(msg=None):

    root = tk.Tk()
    root.withdraw()
    tk.messagebox.showinfo(
        title=_TITLE, message=msg, )
    dir = filedialog.askdirectory()
    root.destroy()

    return dir
>>>>>>> 936311e68c79d0d76d19439edc02c6445ddef2dc
