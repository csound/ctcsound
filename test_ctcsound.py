import ctcsound
import unittest

class TestIntanstiation(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.cs = ctcsound.Csound()
    
    def test_versions(self):
        self.assertTrue(self.cs.version() >= 6050)
        self.assertTrue(self.cs.APIVersion() >= 300)
    
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
        sr = 48000
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
    
    def test_hostData(self):
        data = {"string": "mydata", "number": 1956.2705, "boolean": True}
        cs = ctcsound.Csound(data)
        ret = cs.hostData()
        self.assertEqual(data, ret)
        data = [5, 4, 10.9]
        cs.setHostData(data)
        ret = cs.hostData()
        self.assertEqual(data, ret)
        cs.setHostData("dummy")
        self.assertEqual("dummy", cs.hostData())
        cs.setHostData(7)
        self.assertEqual(7, cs.hostData())
    
    def test_setOption(self):
        self.cs.setOption("--sample-rate=48000")
        self.cs.setOption("-k 4800")
        self.cs.start()
        self.assertEqual(48000, self.cs.sr())
    
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
        
if __name__ == '__main__':
    unittest.main()
