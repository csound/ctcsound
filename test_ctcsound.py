'''
    test_ctcsound.py:
    
    Copyright (C) 2016 Francois Pinot
    
    This file is part of Csound.
    
    This code is free software; you can redistribute it
    and/or modify it under the terms of the GNU Lesser General Public
    License as published by the Free Software Foundation; either
    version 2.1 of the License, or (at your option) any later version.
    
    Csound is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Lesser General Public License for more details.
    
    You should have received a copy of the GNU Lesser General Public
    License along with Csound; if not, write to the Free Software
    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA
    02111-1307 USA
'''

import ctcsound, numpy as np, ctypes as ct
from csoundSession import *
import unittest

cs = None

def setUpModule():
    global cs
    cs = CsoundSession("simple.csd")
    print("coucou")

def tearDownModule():
    global cs
    cs.stopPerformance()
    print("caca")


class TestIntanstiation(unittest.TestCase):
    '''    @classmethod
    def setUpClass(self):
        self.initialData = {"string": "mydata", "number": 1956.2705, "boolean": True} 
        self.cs = ctcsound.Csound(self.initialData)
    
    def test_hostData(self):
        ret = self.cs.hostData()
        self.assertEqual(self.initialData, ret)
        data = [5, 4, 10.9]
        self.cs.setHostData(data)
        ret = self.cs.hostData()
        self.assertEqual(data, ret)
        self.cs.setHostData("dummy")
        self.assertEqual("dummy", self.cs.hostData())
        self.cs.setHostData(7)
        self.assertEqual(7, self.cs.hostData())
    '''    
    def test_versions(self):
        self.assertTrue(ctcsound.csoundGetVersion() >= 6050)
        self.assertTrue(ctcsound.csoundGetAPIVersion() >= 300)

'''
class TestPerformance(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.cs = ctcsound.Csound()
    
    def test_tree(self):
        orc = """
        instr 100
        a1 init 0.5
           out  a1
        endin"""
        tree = self.cs.parseOrc(orc)
        self.assertTrue(tree != None)
        ret = self.cs.compileTree(tree)
        self.assertTrue(ret == 0)
        self.cs.deleteTree(tree)
    
    def test_compileOrc_EvalCode(self):
        orc = """
        sr = 44100
        ksmps = 32
        nchnls = 2
        0dbfs = 1
        instr 1 
        aout vco2 0.5, 440
        outs aout, aout
        endin"""
        ret = self.cs.compileOrc(orc)
        self.assertTrue(ret == 0)
        code = "i1 = 2 + 2 \n return i1\n"
        ret = self.cs.evalCode(code)
        self.assertEqual(ret, 4)
    
class TestAttributes(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.cs = ctcsound.Csound()
    
    def test_setOption(self):
        self.cs.reset()
        self.cs.setOption("--sample-rate=96000")
        self.cs.setOption("-k 9600")
        self.cs.compile_("csound", "analogSynth01.csd")
        self.assertEqual(96000, self.cs.sr())
        self.assertEqual(9600, self.cs.kr())
    
    def test_params(self):
        p = ctcsound.CsoundParams()
        self.cs.setDebug(True)
        self.cs.params(p)
        self.assertEqual(1, p.debug_mode)
        self.cs.setDebug(False)
        self.cs.params(p)
        self.assertEqual(0, p.debug_mode)
        p.debug_mode = 1
        self.cs.setParams(p)
        self.assertTrue(self.cs.debug())

class TestRealtimeAudio(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.cs = ctcsound.Csound()
    
    def test_modules(self):
        n = 0
        while True:
            name, type_, err = self.cs.module(n)
            if err == ctcsound.CSOUND_ERROR:
                break
            print("Module %d:%s (%s)\n" % (n, name, type_))
            n += 1
'''    
#if __name__ == '__main__':
#    unittest.main()
