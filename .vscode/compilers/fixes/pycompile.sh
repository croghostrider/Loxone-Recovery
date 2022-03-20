#!/bin/bash

chckusr=$(id -u);

if [ $chckusr = "0" ] ; then
    echo "Pip, setuptools and pyinstaller upgrading";
    pip install --upgrade pip;
    pip install --upgrade setuptools;
    pip uninstall pyinstaller;
    pip install https://github.com/pyinstaller/pyinstaller/archive/develop.tar.gz;
    echo "Now you can run pyinstaller";
    exit;
else
    echo "You need to run this script as root";
fi

read -p "Press enter to exit";