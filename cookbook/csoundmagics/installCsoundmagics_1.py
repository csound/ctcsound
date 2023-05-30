# -*- coding: utf-8 -*-
"""
Copyright (c) François Pinot, May 2016
"""
import nbclassic
import os.path
import shutil
import site

import notebook

def copy_file(filename, dest):
    print("Copying file {} into {}\n".format(filename, dest))
    try:
        shutil.copy(filename, dest)
    except PermissionError:
        os.system('sudo cp "{}" "{}"'.format(filename, dest))

# Copy csoundmagics in site-packages dir
dest = site.getsitepackages()[0]
copy_file("csoundmagics.py", dest)

# Copy csound mode in codemirror
dest = nbclassic.__path__[0]
dest = os.path.join(dest, "static", "components", "codemirror", "mode", "csound")
if not os.path.exists(dest):
    os.mkdir(dest)
copy_file("csound.js", dest)

# Copy custom.js in jupyter dir
dest = os.path.join(notebook.extensions.jupyter_config_dir(), "custom")
if not os.path.exists(dest):
    os.mkdir(dest)
copy_file("custom.js", dest)
