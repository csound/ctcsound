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
import unittest


class TestAttributes(unittest.TestCase):
    @classmethod
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

    def test_setOption(self):
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


class TestGeneralIO(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.cs = ctcsound.Csound()
    
    def test_inputOutputbuffer(self):
        self.cs.compile_("csound", "bufferInOut.csd")
        ibuf = self.cs.inputBuffer()
        obuf = self.cs.outputBuffer()
        ilen, olen = len(ibuf), len(obuf)
        self.assertEqual(ilen, olen)
        self.cs.performBuffer()
        self.assertTrue(np.array_equal(obuf, ibuf/3.0))


class TestCsoundPerformanceThread(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.cs = ctcsound.Csound()
        self.cs.compile_("csoundPerformanceThread", "simple.csd")
        self.pt = ctcsound.CsoundPerformanceThread(self.cs.csound())
    
    @classmethod
    def tearDownClass(self):
        self.pt.stop()
        self.pt.join()
        
    def test_csoundPerformanceThread(self):
        self.pt.play()
        self.assertTrue(self.pt.isRunning())
        self.assertEqual(self.pt.status(), 0)

    def test_scoreEvent(self):
        self.assertEqual(self.cs.tableLength(1), -1)
        self.pt.scoreEvent(False, 'f', (1, 0, 4096, 10, 1))
        self.cs.sleep(1000)
        self.assertEqual(self.cs.tableLength(1), 4096)

if __name__ == '__main__':
    unittest.main()
