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


def show_key_value_list(display_dict=None):

    root = tk.Tk()
    root.state('zoomed')
    lb = tk.Listbox(root)
    lb.grid()

    for key in display_dict:
        lb.insert(tk.END, 'File: {} Reason: {}'.format(key, display_dict[key]))

    lb.pack(padx=10,pady=10,fill='both',expand=True)

    root.mainloop()

    return


def show_info_msgbox(msg=None):
    root = tk.Tk()
    root.withdraw()
    tk.messagebox.showinfo(title=_TITLE, message=msg)
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
