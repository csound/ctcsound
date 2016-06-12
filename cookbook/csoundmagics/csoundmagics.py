# -*- coding: utf-8 -*-

# Copyright (C) 2010, 2016 Francois Pinot, Andres Cabrera, Jacob Joaquin
#
# This code is free software; you can redistribute it
# and/or modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This code is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this code; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA
# 02111-1307 USA
#

# Using code by Andrés Cabrera from icsound
# http://nbviewer.ipython.org/gist/jacobjoaquin/5535792

# Using code by Jacob Joaquin from:
# http://nbviewer.ipython.org/gist/jacobjoaquin/5535792
# http://nbviewer.ipython.org/gist/jacobjoaquin/5550729

# See Francois Pinot's Journal article:
# http://csounds.com/journal/issue14/realtimeCsoundPython.html

from IPython.core.getipython import get_ipython
from IPython.core.magic import Magics, magics_class, cell_magic, line_cell_magic

maxSlotNum = 32
slots = [None for i in range(maxSlotNum+1)]

@magics_class
class CsoundMagics(Magics):
    """Implement magic commands for Csound."""
    def __init__(self, shell):
        Magics.__init__(self, shell)
        ip = get_ipython()
        self.csd = {}
        ip.user_ns["__csd"] = self.csd
        self.orc = {}
        ip.user_ns["__orc"] = self.orc
        self.sco = {}
        ip.user_ns["__sco"] = self.sco
    
    @line_cell_magic
    def csound(self, line, cell=None):
        """%csound and %%csound magics.
        
        %csound n, where n < 0, erases slot#abs(n) bound to an ICsound engine.
        It is normally followed by the 'del ics' command.
        %csound 0 erases slot#0 reserved to an ctcsound.Csound() instance used
        by the runCsd and runOrcSco functions. Il also deletes this instance.
        A call to runCsd or runOrcCsd will automatically create an
        ctcsound.Csound instance bound to slot#0.
        
        %%csound n where n is in [1 .. maxSlotNum] sends Csound code to the
        ICsound engine bound to slot#n. If n is omitted, slot#1 is used.
        """
        global slots, maxSlotNum
        # line magic
        if cell is None:
            try:
                slot = int(line)
                if slot > 0:
                    print("%csound needs a negative or null slot#")
                    return
                slot = -slot
                if slot <= maxSlotNum and slots[slot]:
                    if slot == 0:
                        del slots[slot]
                    else:
                        slots[slot] = None
                    print("Erasing slot#: {}".format(slot))
                    return
                print("No active ICsound engine at slot#: {}".format(slot))
                return1 
            except ValueError as e:
                print("Not a valid slot#: ", e.args[0])
                return
        # cell magic
        if line != '':
            try:
                slot = int(line)
                if slot <= 0 or slot > maxSlotNum:
                    print("slot# has to be in [1..{}]".format(maxSlotNum))
                    return
            except ValueError as e:
                print("Not a valid slot#: ", e.args[0])
                return
        else:
            slot = 1
        cur_ics = slots[slot]
        if not cur_ics:
            print("No active ICsound engine at slot#: {}".format(slot))
            return
        cur_ics.sendCode(str(cell))
        return
    
    @cell_magic
    def csd(self, line, cell):
        """Store the cell in user namespace as a csd under the name specified."""
        if line == '':
            return "Usage: %%csd name"
        self.csd[line] = cell

    @cell_magic
    def orc(self, line, cell):
        """Store the cell in user namespace as an orc under the name specified."""
        if line == '':
            return "Usage: %%orc name"
        self.orc[line] = cell

    @cell_magic
    def sco(self, line, cell):
        """Store the cell in user namespace as a sco under the name specified."""
        if line == '':
            return "Usage: %%sco name"
        self.sco[line] = cell


import ctcsound
import ctypes
from pylab import *
import socket

def runCsd(csdName):
    """Run a csd stored in the user namespace.
    
    One can store a csd in the user name space with the %%csd magic.
    """
    if slots[0] == None:
        slots[0] = ctcsound.Csound()
    cs = slots[0]
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

def runOrcSco(orcName, scoName):
    """Run an orc and sco stored in the user namespace.
    
    One can store an orc in the user namespace with the %%orc magic, and
    a sco with the %%sco magic as well.
    """
    if slots[0] == None:
        slots[0] = ctcsound.Csound()
    cs = slots[0]
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


class SlotError(Exception):
    def __init__(self, value):
        self.value = value
        
    def  __str__(self):
        return repr(self.value)


class ICsound(ctcsound.Csound):
    """Implement Andrés Cabrera's icsound module in csoundmagics.
    
    An ICsound object is a child of a ctcsound.Csound object. It is bound
    to a slot number. This slot number can be used to specify this ICsound
    object when calling a %csound or a %%csound magic command.
    """
    def __init__(self, sr=48000, ksmps=100, nchnls=2, zerodbfs=1.0, dac='dac',
                 adc='', port=0, bufferSize=0):
        """Create an instance of ICsound."""
        global slots, maxSlotNum
        self.slotNum = 0
        for i in range(maxSlotNum):
            if not slots[i+1]:
                self.slotNum = i+1
                break
        if self.slotNum == 0:
            raise SlotError("No more slot available for this engine")
        ctcsound.Csound.__init__(self)
        self._csPerf = None
        self._prevMsgNewLine = True
        self._log = ''
        self._verbose = False
        self._myfltSize = self.sizeOfMYFLT()
        self._clientAddr = None
        self._clientPort = None
        slots[self.slotNum] = self
        self.startEngine(sr, ksmps, nchnls, zerodbfs, dac, adc, port, bufferSize)
    
    def __del__(self):
        global slots, maxSlotNum
        if self._csPerf:
            self.stopEngine(reset=False)
        if slots[self.slotNum]:
            slots[self.slotNum] = None
    
    def listInterfaces(self, output=True):
        """List the audio devices available on the system."""
        lst = self.audioDevList(output)
        i = 1
        for dev in lst:
            print("{:2d}: {}".format(i, dev))
            i += 1
    
    def startClient(self, addr='127.0.0.1', port=12894):
        """Start the client feature of this engine.
        
        sendScore and sendCode method will send their data to the
        IP address and port specified.
        """
        self._clientAddr = addr
        self._clientPort = port
    
    def startEngine(self, sr=48000, ksmps=100, nchnls=2, zerodbfs=1.0, dac='dac',
                    adc='', port=0, bufferSize=0):
        """Start an ICsound engine.
        
        The user can specify values for sr, ksmps, nchnls, zerodbfs, dac, adc,
        a port number, and the messages buffer size. If a port number is given,
        this engine will listen to that port for csound code and events.
        """
        if self._csPerf:
            print("CsoundMagics: Csound already running")
            return
        if self._clientAddr or self._clientPort:
            self._clientAddr = None
            self._clientPort = None
            self._debugPrint("Closing existing client connection before starting engine")
        self._sr = sr
        self._ksmps = ksmps
        self._nchnls = nchnls
        self._0dbfs = zerodbfs
        self._dac = dac
        self._adc = adc
        self.createMessageBuffer(0)
        self.setOption('-o' + self._dac)
        self._bufferSize = bufferSize
        if self._adc:
            self.setOption('-i' + self._adc)
        if port > 0:
            self.setOption("--port={}".format(port))
        if self._bufferSize:
            self.setOption("-B{}".format(self._bufferSize))
            self.setOption("-b{}".format(self._bufferSize))
        orc = '''
        sr = {}
        ksmps = {}
        nchnls = {}
        0dbfs = {}
        '''.format(self._sr, self._ksmps, self._nchnls, self._0dbfs)
        self.compileOrc(orc)
        self.start()
        self._csPerf = ctcsound.CsoundPerformanceThread(self.csound())
        self._csPerf.play()
        self._flushMessages()
        if self._csPerf.status() == 0:
            print("Csound engine started at slot#: {}.".format(self.slotNum))
            if port > 0:
                print("Listening to port {}".format(port))
        else:
            print("Error starting server. Maybe port is in use?")
    
    def stopEngine(self, reset=True):
        """Stop the engine.
        
        The engine can be restarted with the startEngine method, eventually
        with new arguments.
        """
        if not self._csPerf:
            print("Engine is not running")
            return
        if self._csPerf.status() == 0:
            self._csPerf.stop()
        self._csPerf.join()
        self._csPerf = None
        self.clearLog()
        self.destroyMessageBuffer()
        if reset:
            self.reset()
        else:
            self.cleanup()
    
    def sendScore(self, score):
        """Send score events to the engine.
        
        If the startClient method had been called previously, the events
        will be sent to a server as UDP packets instead.
        """
        if self._clientAddr:
            self._sendToServer('scoreline_i {{' + score + '}}\n')
            return
        self._csPerf.inputMessage(score)
        self._flushMessages()
    
    def sendCode(self, code):
        """Send orchestra code to the engine.
        
        If the startClient method had been called previously, the code
        will be sent to a server as UDP packets instead.
        """
        if self._clientAddr:
            self._sendToServer(code)
            return
        self._flushMessages()
        ret = self.compileOrc(code)
        errorText = ''
        for i in range(self.messageCnt()):
            self._log += self.firstMessage()
            errorText += self.firstMessage()
            self.popFirstMessage()
        if ret:
            print(errorText)
    
    def makeTable(self, num, size, gen, *args):
        """Create a function table for this engine."""
        data = 'gitemp_ ftgen {}, 0, {}, {}, '.format(num, size, gen)
        data += ', '.join(map(str, list(args)))
        self._debugPrint(data)
        self.sendCode(data)
    
    def fillTable(self, num, arr):
        """Fill a table with GEN2 using the data in arr.
        
        If the table did not exist, it will be created. If the table existed
        but had the wrong size, it will be resized.
        """
        if type(arr) != np.ndarray and type(arr) != list and type(arr) != tuple:
            raise TypeError("Argument is not array, list, or tuple")
        if type(arr) == np.ndarray and arr.ndim > 1:
            raise TypeError("Only one dimensional arrays are valid")
        
        if self._clientAddr:
            data = ', '.join(map(str, arr))
            data = 'gitemp ftgen {}, 0, {}, -2, '.format(num, len(arr)) + data
            self.sendCode(data)
            return
        
        p = np.array(arr).astype(ctcsound.MYFLT)
        table = self.table(num)
        if (type(table) == np.ndarray) and (table.size == p.size):
            pass
        else:
            if type(table) == np.ndarray:
                self._debugPrint("Resizing table", num, "from", table.size, "to", p.size)
            else:
                self._debugPrint("Creating table ", num)
            self.makeTable(num, p.size, -2, 0)
            table = self.table(num)
        src = p.ctypes.data_as(ctypes.POINTER(ctcsound.MYFLT))
        dest = table.ctypes.data_as(ctypes.POINTER(ctcsound.MYFLT))
        ctypes.memmove(dest, src, p.size*self._myfltSize)
    
    def plotTable(self, num, reuse=False):
        """Plot a table using matplotlib with predefined styles."""
        if self._clientAddr:
            print("Operation not supported for client interface")
            return
        table = self.table(num)
        if not reuse:
            fix, ax = subplots(figsize=(10, 6))
        else:
            ax = gca()
        ax.hlines(0, 0, table.size)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.set_xticks(range(0, table.size+1, int(table.size/4)))
        ax.xaxis.set_ticks_position('bottom')
        ax.yaxis.set_ticks_position('left')
        ax.plot(table, color='black', lw=2)
        xlim(0, table.size)
    
    def setChannel(self, name, value):
        """Set a value on a control channel."""
        if self._clientAddr:
            print("Operation not supported for client interface")
            return
        self.setControlChannel(name, value)
    
    def channel(self, name):
        """Read a value from a control channel."""
        if self._clientAddr:
            print("Operation not supported for client interface")
            return
        return self.controlChannel(name)
    
    def startRecord(self, fileName, sampleBits=16, numBufs=4):
        """Start recording the audio output in an audio file."""
        if self._clientAddr:
            print("Operation not supported for client interface")
            return
        return self._csPerf.record(fileName, sampleBits, numBufs)
    
    def stopRecord(self):
        """Stop the recording of the audio output in an audio file."""
        if self._clientAddr:
            print("Operation not supported for client interface")
            return
        return self._csPerf.stopRecord()
    
    def printLog(self):
        """Display the messages in the csound message buffer."""
        self._flushMessages()
        if self._clientAddr:
            print("Operation not supported for client interface")
            return
        print(self._log)
    
    def clearLog(self):
        """Delete the messages in the csound message buffer."""
        self._flushMessages()
        self._log = ''
    
    def _flushMessages(self):
        for i in range(self.messageCnt()):
            self._log += self.firstMessage()
            self.popFirstMessage()
    
    def _debugPrint(self, *text):
        if self._verbose:
            print(text)
    
    def _sendToServer(self, message):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
        sock.sendto(ctcsound.cstring(message), (self._clientAddr, self._clientPort))


from IPython.core.display import display_javascript

def load_ipython_extension(ip):
    ip.magics_manager.register(CsoundMagics)
    ip.user_ns['runCsd'] = runCsd
    ip.user_ns['runOrcSco'] = runOrcSco
    ip.user_ns['ICsound'] = ICsound
    js = "IPython.CodeCell.config_defaults.highlight_modes['magic_csound'] = {'reg':[/^%%csound/, /^%%csd/, /^%%orc/, /^%%sco/]};"
    display_javascript(js, raw=True)

