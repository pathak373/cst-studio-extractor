import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd 
import os

from extractor import dataExtractor

root=tk.Tk()
root.iconbitmap("./assets/favicon.ico")
root.title("CST Studio 2022 Data Extractor")

root.geometry("500x300")

s11_file_var=tk.StringVar()
gain_file_var=tk.StringVar()
save_file_var=tk.StringVar()

gain_split_var=tk.IntVar()
s11_split_var=tk.IntVar()

error_box = tk.StringVar()

def submit():

    s11_file=s11_file_var.get()
    gain_file=gain_file_var.get()
    save_file=save_file_var.get()

    gain_split=gain_split_var.get()
    s11_split=s11_split_var.get()
    
    try:
        dataExtractor(
            gain_file=gain_file, 
            s11_file=s11_file, 
            save_file=save_file,
            gain_split=gain_split,
            s11_split=s11_split)

    except Exception as e:
        error_box.set(str(e))

    s11_file_var.set("")
    gain_file_var.set("")
    save_file_var.set("")

    gain_split_var.set(0)
    s11_split_var.set(0)

def open_s11(): 
  
    filetypes = (('text files', '*.txt'), 
                 ('All files', '*.*')) 
  
    f = fd.askopenfile(filetypes=filetypes, 
                       initialdir="D:/Downloads")
    if f:
        filepath = os.path.abspath(f.name)
        s11_file_var.set(filepath)

def open_gain(): 
  
    filetypes = (('text files', '*.txt'), 
                 ('All files', '*.*')) 
  
    f = fd.askopenfile(filetypes=filetypes, 
                       initialdir="D:/Downloads")
    if f:
        filepath = os.path.abspath(f.name)
        gain_file_var.set(filepath)

FontSize = 12
Font='serif'

s11_label = ttk.Label(root, text = 'S11 Filename', anchor="e", font=(Font, FontSize, 'normal'))
s11_entry = ttk.Entry(root,textvariable = s11_file_var, font=(Font, FontSize,'normal'))

gain_label = ttk.Label(root, text = 'Gain Filename', anchor="e", font=(Font, FontSize, 'normal'))
gain_entry = ttk.Entry(root,textvariable = gain_file_var,font=(Font, FontSize,'normal'))

savefile_label = ttk.Label(root, text = 'Save Filename', anchor="e", font=(Font, FontSize, 'normal'))
savefile_entry = ttk.Entry(root,textvariable = save_file_var,font=(Font, FontSize,'normal'))

gain_split_label = ttk.Label(root, text = 'Gain Split Number', anchor="e", font=(Font, FontSize, 'normal'))
gain_split_entry = ttk.Entry(root,textvariable = gain_split_var, font=(Font, FontSize,'normal'))

s11_split_label = ttk.Label(root, text = 'S11 Split Number', anchor="e", font=(Font, FontSize, 'normal'))
s11_split_entry = ttk.Entry(root,textvariable = s11_split_var, font=(Font, FontSize,'normal'))

error_entry = ttk.Entry(root,textvariable = error_box, width=380, font=(Font, FontSize,'normal'))

gain_open_button = ttk.Button(root, text='Open Gain File', command=open_gain) 
s11_open_button = ttk.Button(root, text='Open S11 File', command=open_s11) 

sub_btn=ttk.Button(root,text = 'Extract', command = submit)

s11_label.pack()
s11_entry.pack()

gain_label.pack()
gain_entry.pack()

savefile_label.pack()
savefile_entry.pack()

gain_split_label.pack()
gain_split_entry.pack()

s11_split_label.pack()
s11_split_entry.pack()

s11_open_button.place(relx=0.75, rely=0.07)
gain_open_button.place(relx=0.75, rely=0.23)

sub_btn.place(relx=0.75, rely=0.39)

error_entry.place(relx=0, rely=0.9)

root.mainloop()
