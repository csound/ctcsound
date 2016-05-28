# -*- coding: utf-8 -*-
"""
Copyright (c) François Pinot, May 2016
"""

from IPython.paths import get_ipython_dir
import notebook
import os.path
import shutil

# Copy csoundmagics in ipython dir
dest = os.path.join(get_ipython_dir(), "extensions")
shutil.copy("csoundmagics.py", dest)

# Copy csound mode in codemirror
dest = os.path.join(notebook.DEFAULT_STATIC_FILES_PATH, "components", "codemirror", "mode", "csound")
if not os.path.exists(dest):
    os.mkdir(dest)
shutil.copy("csound.js", dest)

