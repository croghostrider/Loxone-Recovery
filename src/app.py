#!/usr/bin/env python3
"""
The methods for loading the Gui.

I have tried to add as much documentation as possible
to keep it understandable.
"""

import os
import tkinter as tk
from tkinter import filedialog, ttk

from recovery import lox_backup


def select_sourcefolder():
    """Generate a manifest from a legacy module."""
    path = filedialog.askdirectory(
        title="Select Source Folder",
        initialdir=os.environ["USERPROFILE"]
        + "\\Documents\\Loxone\\Loxone Config\\Backups",
    )
    source_entry.configure(state="NORMAL")
    source_entry.delete(0, "end")  # deletes the current value
    source_entry.insert(0, path)  # inserts new value assigned by 2nd parameter
    source_entry.configure(state="readonly")
    if len(destination_entry.get()) > 0 and len(source_entry.get()) > 0:
        start_button.state(["NORMAL"])


def select_destinationfolder():
    """Generate a manifest from a legacy module."""
    path = filedialog.askdirectory(
        title="Select Destination Folder",
        initialdir=os.environ["USERPROFILE"]
        + "\\Documents\\Loxone\\Loxone Config\\Backups",
    )
    destination_entry.configure(state="NORMAL")
    destination_entry.delete(0, "end")  # deletes the current value
    destination_entry.insert(0, path)  # inserts new value assigned by 2nd parameter
    destination_entry.configure(state="readonly")
    if len(destination_entry.get()) > 0 and len(source_entry.get()) > 0:
        start_button.config(state="normal")


def list_files():
    """Generate a manifest from a legacy module."""
    # files = [f for f in os.listdir(source_entry.get()) if os.path.isfile(f)]
    start_button.state(["disabled"])
    start_button.update()
    filelist = [
        filename
        for filename in os.listdir(source_entry.get())
        if filename.startswith("sps_") and (filename.endswith(".zip"))
    ]
    for filename in filelist:
        lox_backup(filename, source_entry.get(), destination_entry.get())


# root window
root = tk.Tk()
root.title("Select the prog Folder from the Backup")
root.resizable(0, 0)

# configure the grid
root.columnconfigure(0, weight=5)
root.columnconfigure(1, weight=1)

# source
source_button = ttk.Button(root, text="Source", command=select_sourcefolder)
source_button.grid(column=1, row=0, sticky=tk.E, padx=5, pady=5)

source_entry = ttk.Entry(root, width=50, state="readonly")
source_entry.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)

# destination
destination_button = ttk.Button(
    root, text="Destination", command=select_destinationfolder
)
destination_button.grid(column=1, row=1, sticky=tk.E, padx=5, pady=5)

destination_entry = ttk.Entry(root, width=50, state="readonly")
destination_entry.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)

# start button
start_button = ttk.Button(root, text="Start", command=list_files)
start_button.grid(column=1, row=3, sticky=tk.E, padx=5, pady=5)
start_button.state(["disabled"])

root.mainloop()
