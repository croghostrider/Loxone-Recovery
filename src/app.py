#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import struct
import zipfile
import zlib
import os

def select_sourcefolder():
    path= filedialog.askdirectory(title="Select Source Folder", initialdir=os.environ["USERPROFILE"] + "\\Documents\\Loxone\\Loxone Config\\Backups")
    source_entry.configure(state="NORMAL")
    source_entry.delete(0, "end") #deletes the current value
    source_entry.insert(0, path) #inserts new value assigned by 2nd parameter
    source_entry.configure(state="readonly")
    if len(destination_entry.get()) > 0 and len(source_entry.get()) > 0:
        start_button.state(["NORMAL"])

def select_destinationfolder():
    path= filedialog.askdirectory(title="Select Destination Folder", initialdir=os.environ["USERPROFILE"] + "\\Documents\\Loxone\\Loxone Config\\Backups")
    destination_entry.configure(state="NORMAL")
    destination_entry.delete(0, "end") #deletes the current value
    destination_entry.insert(0, path) #inserts new value assigned by 2nd parameter
    destination_entry.configure(state="readonly")
    if len(destination_entry.get()) > 0 and len(source_entry.get()) > 0:
        start_button.config(state="normal")

def lox_backup(filename):
    #with open(filename, "wb") as f:
    #   f.write(download_file.read())

    zf = zipfile.ZipFile(source_entry.get() + "/" + filename)
    with zf.open("sps0.LoxCC") as f: 
        header, = struct.unpack("<L", f.read(4))
        if header == 0xaabbccee:    # magic word to detect a compressed file
            compressedSize,uncompressedSize,checksum, = struct.unpack("<LLL", f.read(12))
            data = f.read(compressedSize)
            index = 0
            resultStr = bytearray()
            while index<len(data):
                # the first byte contains the number of bytes to copy in the upper
                # nibble. If this nibble is 15, then another byte follows with
                # the remainder of bytes to copy. (Comment: it might be possible that
                # it follows the same scheme as below, which means: if more than
                # 255+15 bytes need to be copied, another 0xff byte follows and so on)
                byte, = struct.unpack("<B", data[index:index+1])
                index += 1
                copyBytes = byte >> 4
                byte &= 0xf
                if copyBytes == 15:
                    while True:
                        addByte = data[index]
                        copyBytes += addByte
                        index += 1
                        if addByte != 0xff:
                            break
                if copyBytes > 0:
                    resultStr += data[index:index+copyBytes]
                    index += copyBytes
                if index >= len(data):
                    break
                # Reference to data which already was copied into the result.
                # bytesBack is the offset from the end of the string
                bytesBack, = struct.unpack("<H", data[index:index+2])
                index += 2
                # the number of bytes to be transferred is at least 4 plus the lower
                # nibble of the package header.
                bytesBackCopied = 4 + byte
                if byte == 15:
                    # if the header was 15, then more than 19 bytes need to be copied.
                    while True:
                        val, = struct.unpack("<B", data[index:index+1])
                        bytesBackCopied += val
                        index += 1
                        if val != 0xff:
                            break
                # Duplicating the last byte in the buffer multiple times is possible,
                # so we need to account for that.
                while bytesBackCopied > 0:
                    if -bytesBack+1 == 0:
                        resultStr += resultStr[-bytesBack:]
                    else:
                        resultStr += resultStr[-bytesBack:-bytesBack+1]
                    bytesBackCopied -= 1
            if checksum != zlib.crc32(resultStr):
                print("Checksum is wrong")
                exit(1)
            if len(resultStr) != uncompressedSize:
                print("Uncompressed filesize is wrong %d != %d" % (len(resultStr),uncompressedSize))
                exit(1)
            newfilename = filename[:13]  + "-" + filename[13:][:2] + "-" +filename[15:][:2] + "-" +filename[17:][:6]
            print(newfilename)
            with open(destination_entry.get() + "/" + newfilename + ".Loxone", "wb") as f:
                f.write(resultStr)

def list_files():
    # files = [f for f in os.listdir(source_entry.get()) if os.path.isfile(f)]
    start_button.state(["disabled"])
    filelist = []
    for filename in os.listdir(source_entry.get()):
        if filename.startswith("sps_") and (filename.endswith(".zip")):
            filelist.append(filename)
    for filename in filelist:
        print(filename)
        lox_backup(filename)

# root window
root = tk.Tk()
root.title("Select the prog Folder from the Backup")
root.resizable(0, 0)

# configure the grid
root.columnconfigure(0, weight=5)
root.columnconfigure(1, weight=1)

# event

var=tk.StringVar(root)

# source
source_button = ttk.Button(root, text="Source", command=select_sourcefolder)
source_button.grid(column=1, row=0, sticky=tk.E, padx=5, pady=5)

source_entry = ttk.Entry(root, width=50, state="readonly")
source_entry.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)

# destination
destination_button = ttk.Button(root, text="Destination", command=select_destinationfolder)
destination_button.grid(column=1, row=1, sticky=tk.E, padx=5, pady=5)

destination_entry = ttk.Entry(root, width=50, state="readonly")
destination_entry.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)

# start button
start_button = ttk.Button(root, text="Start", command=list_files)
start_button.grid(column=1, row=3, sticky=tk.E, padx=5, pady=5)
start_button.state(["disabled"])

root.mainloop()