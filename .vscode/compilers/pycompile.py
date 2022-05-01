#!/usr/bin/env python3

import os
import shutil
import subprocess
import sys

# ARGS
fileDirname = sys.argv[1]
fileBasename = sys.argv[2]
workspaceFolder = sys.argv[3]

# TRANSFORMATION
relativeFileDirname = fileDirname[len(workspaceFolder)+1:]
fileBasenameNoExtension = "".join(fileBasename.rsplit(".py", 1))
distpath = os.path.join(workspaceFolder, "output", relativeFileDirname)

# COMMAND GENERATOR
def construct():
    COMMAND = [
        "pyinstaller",
        "--onefile",
        "--clean",
        "--noconsole",
        "--distpath",
        distpath,
    ]

    for file in os.listdir(fileDirname):
        if file.endswith(".ico"):
            COMMAND.append("--icon")
            COMMAND.append(os.path.join(fileDirname, file))
            break
    COMMAND.append(fileBasename)
    return COMMAND

# CLEANER
def clean():
    path = os.path.join(fileDirname, "__pycache__")
    shutil.rmtree(path)
    path = os.path.join(fileDirname, "build")
    shutil.rmtree(path)

if __name__ == "__main__":
    COMMAND = construct()
    subprocess.check_call(COMMAND, cwd=fileDirname)
    clean()