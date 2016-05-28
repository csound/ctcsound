# -*- coding: utf-8 -*-
"""
Copyright (c) François Pinot, May 2016
"""

from IPython.core.getipython import get_ipython
from IPython.core.magic import magics_class, Magics, cell_magic

@magics_class
class CsoundMagics(Magics):
    def __init__(self, shell):
        Magics.__init__(self, shell)
        ip = get_ipython()
        self.csd = {}
        ip.user_ns["__csd"] = self.csd
        self.orc = {}
        ip.user_ns["__orc"] = self.orc
        self.sco = {}
        ip.user_ns["__sco"] = self.sco
        
    @cell_magic
    def csd(self, line, cell):
        """Store the cell in data as a csd"""
        if line == '':
            return "Usage: %%csd name"
        self.csd[line] = cell

    @cell_magic
    def orc(self, line, cell):
        """Store the cell in data as an orc"""
        if line == '':
            return "Usage: %%orc name"
        self.orc[line] = cell

    @cell_magic
    def sco(self, line, cell):
        """Store the cell in data as a sco"""
        if line == '':
            return "Usage: %%sco name"
        self.sco[line] = cell


import ctcsound

def runCsd(cs, csdName):
    ip = get_ipython()
    csd = ip.user_ns["__csd"][csdName]
    ret = cs.compileCsdText(csd)
    if ret == ctcsound.CSOUND_SUCCESS:
        cs.start()
        cs.perform()
        cs.reset()
        return 'OK'
    else:
        return 'Error'

def runOrcSco(cs, orcName, scoName):
    ip = get_ipython()
    orc = ip.user_ns["__orc"][orcName]
    ret = cs.compileOrc(orc)
    if ret != ctcsound.CSOUND_SUCCESS:
        return 'Error in orchestra'
    sco = ip.user_ns["__sco"][scoName]
    ret = cs.readScore(sco)
    if ret != ctcsound.CSOUND_SUCCESS:
        return 'Error in score'
    cs.start()
    cs.perform()
    cs.reset()
    return 'OK'


from IPython.core.display import display_javascript

def load_ipython_extension(ip):
    ip.magics_manager.register(CsoundMagics)
    ip.user_ns['runCsd'] = runCsd
    ip.user_ns['runOrcSco'] = runOrcSco
    js = "IPython.CodeCell.config_defaults.highlight_modes['magic_csound'] = {'reg':[/^%%csd/,/^%%orc/,/^%%sco/]};"
    display_javascript(js, raw=True)

