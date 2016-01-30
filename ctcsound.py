from ctypes import *
import numpy as np
import sys

if sys.platform.startswith('linux'):
    libcsound = CDLL("libcsound64.so")
elif sys.platform.startswith('win'):
    libcsound = cdll.libcsound64
elif sys.platform.startswith('darwin'):
    libcsound = CDLL("libcsound64.dylib")
else:
    sys.exit("Don't know your system! Exiting...")

MYFLT = c_double

class CsoundParams(Structure):
    _fields_ = [("debug_mode", c_int),        # debug mode, 0 or 1
                ("buffer_frames", c_int),     # number of frames in in/out buffers
                ("hardware_buffer_frames", c_int), # ibid. hardware
                ("displays", c_int),          # graph displays, 0 or 1
                ("ascii_graphs", c_int),      # use ASCII graphs, 0 or 1
                ("postscript_graphs", c_int), # use postscript graphs, 0 or 1
                ("message_level", c_int),     # message printout control
                ("tempo", c_int),             # tempo ("sets Beatmode) 
                ("ring_bell", c_int),         # bell, 0 or 1
                ("use_cscore", c_int),        # use cscore for processing
                ("terminate_on_midi", c_int), # terminate performance at the end
                                              #   of midifile, 0 or 1
                ("heartbeat", c_int),         # print heart beat, 0 or 1
                ("defer_gen01_load", c_int),  # defer GEN01 load, 0 or 1
                ("midi_key", c_int),          # pfield to map midi key no
                ("midi_key_cps", c_int),      # pfield to map midi key no as cps
                ("midi_key_oct", c_int),      # pfield to map midi key no as oct
                ("midi_key_pch", c_int),      # pfield to map midi key no as pch
                ("midi_velocity", c_int),     # pfield to map midi velocity
                ("midi_velocity_amp", c_int), # pfield to map midi velocity as amplitude
                ("no_default_paths", c_int),  # disable relative paths from files, 0 or 1
                ("number_of_threads", c_int), # number of threads for multicore performance
                ("syntax_check_only", c_int), # do not compile, only check syntax
                ("csd_line_counts", c_int),   # csd line error reporting
                ("compute_weights", c_int),   # deprecated, kept for backwards comp. 
                ("realtime_mode", c_int),     # use realtime priority mode, 0 or 1
                ("sample_accurate", c_int),   # use sample-level score event accuracy
                ("sample_rate_override", MYFLT),  # overriding sample rate
                ("control_rate_override", MYFLT), # overriding control rate
                ("nchnls_override", c_int),   # overriding number of out channels
                ("nchnls_i_override", c_int), # overriding number of in channels
                ("e0dbfs_override", MYFLT),   # overriding 0dbfs
                ("daemon", c_int),            # daemon mode
                ("ksmps_override", c_int)]    # ksmps override

string64 = c_char * 64

class csoundAudioDevice(Structure):
    _fields_ = [("device_name", string64),
                ("device_id", string64),
                ("rt_module", string64),
                ("max_nchnls", c_int),
                ("isOutput", c_int)]

class CsoundRtAudioParams(Structure):
    _fields_ = [("devName", c_char_p),   # device name (NULL/empty: default)
                ("devNum", c_int),       # device number (0-1023), 1024: default
                ("bufSamp_SW", c_uint),  # buffer fragment size (-b) in sample frames
                ("bufSamp_HW", c_int),   # total buffer size (-B) in sample frames
                ("nChannels", c_int),    # number of channels
                ("sampleFormat", c_int), # sample format (AE_SHORT etc.)
                ("sampleRate", c_float)] # sample rate in Hz

libcsound.csoundCreate.restype = c_void_p
libcsound.csoundCreate.argtypes = [py_object]

libcsound.csoundDestroy.argtypes = [c_void_p]

libcsound.csoundParseOrc.restype = c_void_p
libcsound.csoundParseOrc.argtypes = [c_void_p, c_char_p]

libcsound.csoundCompileTree.argtypes = [c_void_p, c_void_p]
libcsound.csoundDeleteTree.argtypes = [c_void_p, c_void_p]
libcsound.csoundCompileOrc.argtypes = [c_void_p, c_char_p]

libcsound.csoundEvalCode.restype = MYFLT
libcsound.csoundEvalCode.argtypes = [c_void_p, c_char_p]

libcsound.csoundCompileArgs.argtypes = [c_void_p, c_int, POINTER(c_char_p)]
libcsound.csoundStart.argtypes = [c_void_p]
libcsound.csoundCompile.argtypes = [c_void_p, c_int, POINTER(c_char_p)]
libcsound.csoundCompileCsd.argtypes = [c_void_p, c_char_p]

libcsound.csoundPerform.argtypes = [c_void_p]
libcsound.csoundPerformKsmps.argtypes = [c_void_p]
libcsound.csoundPerformBuffer.argtypes = [c_void_p]
libcsound.csoundStop.argtypes = [c_void_p]
libcsound.csoundCleanup.argtypes = [c_void_p]
libcsound.csoundReset.argtypes = [c_void_p]

libcsound.csoundGetSr.restype = MYFLT
libcsound.csoundGetSr.argtypes = [c_void_p]
libcsound.csoundGetKr.restype = MYFLT
libcsound.csoundGetKr.argtypes = [c_void_p]
libcsound.csoundGetKsmps.restype = c_uint32
libcsound.csoundGetKsmps.argtypes = [c_void_p]
libcsound.csoundGetNchnls.restype = c_uint32
libcsound.csoundGetNchnls.argtypes = [c_void_p]
libcsound.csoundGetNchnlsInput.restype = c_uint32
libcsound.csoundGetNchnlsInput.argtypes = [c_void_p]
libcsound.csoundGet0dBFS.restype = MYFLT
libcsound.csoundGet0dBFS.argtypes = [c_void_p]
libcsound.csoundGetCurrentTimeSamples.restype = c_int64
libcsound.csoundGetCurrentTimeSamples.argtypes = [c_void_p]
libcsound.csoundGetHostData.restype = py_object
libcsound.csoundGetHostData.argtypes = [c_void_p]
libcsound.csoundSetHostData.argtypes = [c_void_p, py_object]
libcsound.csoundSetOption.argtypes = [c_void_p, c_char_p]
libcsound.csoundSetParams.argtypes = [c_void_p, POINTER(CsoundParams)]
libcsound.csoundGetParams.argtypes = [c_void_p, POINTER(CsoundParams)]
libcsound.csoundGetDebug.argtypes = [c_void_p]
libcsound.csoundSetDebug.argtypes = [c_void_p, c_int]

libcsound.csoundGetOutputName.restype = c_char_p
libcsound.csoundGetOutputName.argtypes = [c_void_p]
libcsound.csoundSetOutput.argtypes = [c_void_p, c_char_p, c_char_p, c_char_p]
libcsound.csoundSetInput.argtypes = [c_void_p, c_char_p]
libcsound.csoundSetMIDIInput.argtypes = [c_void_p, c_char_p]
libcsound.csoundSetMIDIFileInput.argtypes = [c_void_p, c_char_p]
libcsound.csoundSetMIDIOutput.argtypes = [c_void_p, c_char_p]
libcsound.csoundSetMIDIFileOutput.argtypes = [c_void_p, c_char_p]

FILEOPENFUNC = CFUNCTYPE(None, c_void_p, c_char_p, c_int, c_int, c_int)
libcsound.csoundSetFileOpenCallback.argtypes = [c_void_p, FILEOPENFUNC]

libcsound.csoundSetRTAudioModule.argtypes = [c_void_p, c_char_p]
libcsound.csoundGetModule.argtypes = [c_void_p, c_int, POINTER(c_char_p), POINTER(c_char_p)]
libcsound.csoundGetInputBufferSize.restype = c_long
libcsound.csoundGetInputBufferSize.argtypes = [c_void_p]
libcsound.csoundGetOutputBufferSize.restype = c_long
libcsound.csoundGetOutputBufferSize.argtypes = [c_void_p]
libcsound.csoundGetInputBuffer.restype = POINTER(MYFLT)
libcsound.csoundGetInputBuffer.argtypes = [c_void_p]
libcsound.csoundGetOutputBuffer.restype = POINTER(MYFLT)
libcsound.csoundGetOutputBuffer.argtypes = [c_void_p]
libcsound.csoundGetSpin.restype = POINTER(MYFLT)
libcsound.csoundGetSpin.argtypes = [c_void_p]
libcsound.csoundAddSpinSample.argtypes = [c_void_p, c_int, c_int, MYFLT]
libcsound.csoundGetSpout.restype = POINTER(MYFLT)
libcsound.csoundGetSpout.argtypes = [c_void_p]
libcsound.csoundGetSpoutSample.argtypes = [c_void_p, c_int, c_int]
libcsound.csoundGetRtRecordUserData.restype = POINTER(c_void_p)
libcsound.csoundGetRtRecordUserData.argtypes = [c_void_p]
libcsound.csoundGetRtPlayUserData.restype = POINTER(c_void_p)
libcsound.csoundGetRtPlayUserData.argtypes = [c_void_p]
libcsound.csoundSetHostImplementedAudioIO.argtypes = [c_void_p, c_int, c_int]
libcsound.csoundGetAudioDevList.argtypes = [c_void_p, c_void_p, c_int]
PLAYOPENFUNC = CFUNCTYPE(c_int, c_void_p, POINTER(CsoundRtAudioParams))
libcsound.csoundSetPlayopenCallback.argtypes = [c_void_p, PLAYOPENFUNC]

def cstring(s):
    if sys.version_info[0] >= 3:
        return bytes(s, 'utf-8')
    return s

def pstring(s):
    if sys.version_info[0] >= 3:
        return str(s, 'utf-8')
    return s

def csoundArgList(lst):
    argc = len(lst)
    argv = (POINTER(c_char_p) * argc)()
    for i in range(argc):
        v = cstring(lst[i])
        argv[i] = cast(pointer(create_string_buffer(v)), POINTER(c_char_p))
    return c_int(argc), cast(argv, POINTER(c_char_p))

class Csound:
    CSOUND_SUCCESS = 0           # Completed successfully.
    CSOUND_ERROR = -1            # Unspecified failure.
    CSOUND_INITIALIZATION = -2   # Failed during initialization.
    CSOUND_PERFORMANCE = -3      # Failed during performance.
    CSOUND_MEMORY = -4           # Failed to allocate requested memory.
    CSOUND_SIGNAL = -5           # Termination requested by SIGINT or SIGTERM.
    
    # Instantiation
    def __init__(self, hostData=None):
        """Creates an instance of Csound.
       
        Returns an opaque pointer that must be passed to most Csound API
        functions. The hostData parameter can be None, or it can be any
        sort of data; these data can be accessed from the Csound instance
        that is passed to callback routines.
        """
        self.cs = libcsound.csoundCreate(py_object(hostData))
        # We keep a reference of callbacks so that they won't be garbage
        # collected.
        self.fileOpenCb = None
        self.playOpenCb = None
    
    def __del__(self):
        """Destroys an instance of Csound."""
        libcsound.csoundDestroy(self.cs)

    def version(self):
        """Returns the version number times 1000 (5.00.0 = 5000)."""
        return libcsound.csoundGetVersion(self.cs)
    
    def APIVersion(self):
        """Returns the API version number times 100 (1.00 = 100)."""
        return libcsound.csoundGetAPIVersion(self.cs)
    
    #Performance
    def parseOrc(self, orc):
        """Parse the given orchestra from an ASCII string into a TREE.
        
        This can be called during performance to parse new code.
        """
        return libcsound.csoundParseOrc(self.cs, cstring(orc))
    
    def compileTree(self, tree):
        """Compile the given TREE node into structs for Csound to use.
        
        This can be called during performance to compile a new TREE.
        """
        return libcsound.csoundCompileTree(self.cs, tree)
    
    def deleteTree(self, tree):
        """Free the resources associated with the TREE tree.
        
        This function should be called whenever the TREE was
        created with parseOrc and memory can be deallocated.
        """
        libcsound.csoundDeleteTree(self.cs, tree)

    def compileOrc(self, orc):
        """Parse, and compile the given orchestra from an ASCII string.
        
        Also evaluating any global space code (i-time only).
        This can be called during performance to compile a new orchestra.
        
            orc = "instr 1 \n a1 rand 0dbfs/4 \n out a1 \n"
            cs.compileOrc(orc)
        """
        return libcsound.csoundCompileOrc(self.cs, cstring(orc))
    
    def evalCode(self, code):
        """Parse and compile an orchestra given on an string.
        
        Evaluating any global space code (i-time only).
        On SUCCESS it returns a value passed to the
        'return' opcode in global space.
        
            code = "i1 = 2 + 2 \n return i1 \n"
            retval = cs.evalCode(code)
        """
        return libcsound.csoundEvalCode(self.cs, cstring(code))
    
    #def initializeCscore(insco, outsco):
    
    def compileArgs(self, *args):
        """Compile args.
        
        Read arguments, parse and compile an orchestra,
        read, process and load a score.
        """
        argc, argv = csoundArgList(args)
        return libcsound.csoundCompileArgs(self.cs, argc, argv)
    
    def start(self):
        """Prepares Csound for performance after compilation.
        
        Using one or more of the above functions.
        NB: this is called internally by compile_(), therefore
        it is only required if performance is started without
        a call to that function.
        """
        return libcsound.csoundStart(self.cs)
    
    def compile_(self, *args):
        """Compile Csound input files (such as an orchestra and score).
        
        As directed by the supplied command-line arguments,
        but does not perform them. Returns a non-zero error code on failure.
        This function cannot be called during performance, and before a
        repeated call, reset() needs to be called.
        In this (host-driven) mode, the sequence of calls should be as follows:
        
            cs.compile_(args)
            while (cs.performBuffer() == 0)
                pass
            cs.cleanup()
            cs.reset()
        
        Calls start() internally.
        """
        argc, argv = csoundArgList(args)
        return libcsound.csoundCompile(self.cs, argc, argv)
    
    def compileCsd(csd):
        """Compile a Csound input file (.csd file).
        
        The input file includes command-line arguments, but does not
        perform the file. Return a non-zero error code on failure.
        In this (host-driven) mode, the sequence of calls should be
        as follows:
        
            cs.compileCsd(args)
            while (cs.performBuffer() == 0)
                pass
            cs.cleanup()
            cs.reset()
        
        NB: this function can be called during performance to
        replace or add new instruments and events.
        """
        return libcsound.csoundCompileCsd(self.cs, cstring(csd))
    
    def perform(self):
        """Sense input events and performs audio output.
        
        This is done until the end of score is reached (positive return value),
        an error occurs (negative return value), or performance is stopped by
        calling stop() from another thread (zero return value).
        Note that compile_(), or compileOrc(), readScore(), start() must be
        called first.
        In the case of zero return value, perform() can be called again
        to continue the stopped performance. Otherwise, reset() should be
        called to clean up after the finished or failed performance.
        """
        return libcsound.csoundPerform(self.cs)
    
    def performKsmps(self):
        """Sense input events, and performs audio output.
        
        This is done for one control sample worth (ksmps).
        Note that compile_(), or compileOrc(), readScore(), start() must be
        called first.
        Returns False during performance, and True when performance is
        finished. If called until it returns True, will perform an entire
        score.
        Enables external software to control the execution of Csound,
        and to synchronize performance with audio input and output.
        """
        return libcsound.csoundPerformKsmps(self.cs)
    
    def performBuffer(self):
        """Perform Csound, sensing real-time and score events.
        
        Processing one buffer's worth (-b frames) of interleaved audio.
        Note that compile_ must be called first, then call
        outputBuffer() and inputBuffer() to get the pointer
        to csound's I/O buffers.
        Returns false during performance, and true when performance is finished.
        """
        return libcsound.csoundBuffer(self.cs)
    
    def stop(self):
        """Stop a perform() running in another thread.
        
        Note that it is not guaranteed that perform() has already stopped
        when this function returns.
        """
        return libcsound.csoundStop(self.cs)
    
    def cleanup(self):
        """Print information and closes audio and MIDI devices.
        
        The information is about the end of a performance.
        Note: after calling cleanup(), the operation of the perform
        functions is undefined.
        """
        return libcsound.csoundCleanup(self.cs)
    
    def reset(self):
        """Reset all internal memory and state.
        
        In preparation for a new performance.
        Enable external software to run successive Csound performances
        without reloading Csound. Implies cleanup(), unless already called.
        """
        return libcsound.csoundReset(self.cs)
    
    # Attibutes
    def sr(self):
        """Return the number of audio sample frames per second."""
        return libcsound.csoundGetSr(self.cs)
    
    def kr(self):
        """Return the number of control samples per second."""
        return libcsound.csoundGetKr(self.cs)
    
    def ksmps(self):
        """Return the number of audio sample frames per control sample."""
        return libcsound.csoundGetKsmps(self.cs)
    
    def nchnls(self):
        """Return the number of audio output channels.
        
        Set through the nchnls header variable in the csd file.
        """
        return libcsound.csoundGetNchnls(self.cs)
    
    def nchnlsInput(self): 
        """Return the number of audio input channels.
        
        Set through the nchnls_i header variable in the csd file. If this
        variable is not set, the value is taken from nchnls.
        """
        return libcsound.csoundGetNchnlsInput(self.cs)
    
    def get0dBFS(self):
        """Return the 0dBFS level of the spin/spout buffers."""
        return libcsound.csoundGet0dBFS(self.cs)
    
    def currentTimeSamples(self):
        """Return the current performance time in samples."""
        return libcsound.csoundGetCurrentTimeSamples(self.cs)
    
    def sizeOfMYFLT(self):
        """Return the size of MYFLT in bytes."""
        return libcsound.csoundGetSizeOfMYFLT()
    
    def hostData(self):
        """Return host data."""
        return libcsound.csoundGetHostData(self.cs)
    
    def setHostData(self, data):
        """Set host data."""
        libcsound.csoundSetHostData(self.cs, py_object(data))
    
    def setOption(self, option):
        """Set a single csound option (flag).
        
        Returns CSOUND_SUCCESS on success.
        NB: blank spaces are not allowed.
        """
        libcsound.csoundSetOption(self.cs, cstring(option))
    
    def setParams(self, params):
        """Configure Csound with a given set of parameters.
        
        These parameters are defined in the CsoundParams structure.
        They are the part of the OPARMS struct that are configurable through
        command line flags.
        The CsoundParams structure can be obtained using params().
        These options should only be changed before performance has started.
        """
        libcsound.csoundSetParams(self.cs, byref(params))
    
    def params(self, params):
        """Get the current set of parameters from a CSOUND instance.
        
        These parameters are in a CsoundParams structure. See setParams().
        
            p = CsoundParams()
            cs.params(p)
        """
        libcsound.csoundGetParams(self.cs, byref(params))
    
    def debug(self):
        """Return whether Csound is set to print debug messages.
        
        Those messages are sent through the DebugMsg() internal API function.
        """
        return libcsound.csoundGetDebug(self.cs) != 0
    
    def setDebug(self, debug):
        """Set whether Csound prints debug messages.
        
        The debug argument must have value True or False.
        Those messaged come from the DebugMsg() internal API function.
        """
        libcsound.csoundSetDebug(self.cs, c_int(debug))

    # General Input/Output
    def outputName(self):
        """Return the output audio output name (-o)"""
        s = libcsound.csoundGetOutputName(self.cs)
        return pstring(s)
    
    def setOutput(self, name, type_, format):
        """Set output destination, type and format.
        
        type_ can be one of  "wav", "aiff", "au", "raw", "paf", "svx", "nist",
        "voc", "ircam", "w64", "mat4", "mat5", "pvf", "xi", "htk", "sds",
        "avr", "wavex", "sd2", "flac", "caf", "wve", "ogg", "mpc2k", "rf64",
        or NULL (use default or realtime IO).
        format can be one of "alaw", "schar", "uchar", "float", "double",
        "long", "short", "ulaw", "24bit", "vorbis", or NULL (use default or
        realtime IO).
        For RT audio, use device_id from CS_AUDIODEVICE for a given audio
        device.
        """
        n = cstring(name)
        t = cstring(type_)
        f = cstring(format)
        libcsound.csoundSetOutput(self.cs, n, t, f)
    
    def setInput(self, name):
        """Set input source."""
        libcsound.csoundSetInput(self.cs, cstring(name))
    
    def setMIDIInput(self, name):
        """Set MIDI input device name/number."""
        libcsound.csoundSetMidiInput(self.cs, cstring(name))
    
    def setMIDIFileInput(self, name):
        """Set MIDI file input name."""
        libcsound.csoundSetMIDIFileInput(self.cs, cstring(name))
    
    def setMIDIOutput(self, name):
        """Set MIDI output device name/number."""
        libcsound.csoundSetMIDIOutput(self.cs, cstring(name))
    
    def setMIDIFileOutput(self, name):
        """Set MIDI file output name."""
        libcsound.csoundSetMIDIFileOutput(self.cs, cstring(name))

    def setFileOpenCallback(self, function):
        """Set a callback for receiving notices whenever Csound opens a file.
        
        The callback is made after the file is successfully opened.
        The following information is passed to the callback:
           bytes  pathname of the file; either full or relative to current dir
           int    a file type code from the enumeration CSOUND_FILETYPES
           int    1 if Csound is writing the file, 0 if reading
           int    1 if a temporary file that Csound will delete; 0 if not
           
        Pass NULL to disable the callback.
        This callback is retained after a csoundReset() call.
        """
        self.fileOpenCb = FILEOPENFUNC(function)
        libcsound.csoundSetFileOpenCallback(self.cs, self.fileOpenCb)

    # Realtime Audio I/O
    def setRTAudioModule(self, module):
        """Set the current RT audio module."""
        libcsound.csoundSetRTAudioModule(self.cs, cstring(module))
    
    def module(self, number):
        """Retrieve a module name and type given a number.
        
        Type is "audio" or "midi". Modules are added to list as csound loads
        them. Return CSOUND_SUCCESS on success and CSOUND_ERROR if module
        number was not found.
        
            n = 0
            while True:
                name, type, err = cs.module(n)
                if err == CSOUND_ERROR:
                    break
                print("Module %d:%s (%s)\n" % (n, name, type)
                n += 1
        """
        name = pointer(c_char_p(cstring("dummy")))
        type_ = pointer(c_char_p(cstring("dummy")))
        err = libcsound.csoundGetModule(self.cs, number, name, type_)
        if err == self.CSOUND_ERROR:
            return None, None, err
        n = pstring(string_at(name.contents))
        t = pstring(string_at(type_.contents))
        return n, t, err
    
    def inputBufferSize(self):
        """Return the number of samples in Csound's input buffer."""
        return libcsound.csoundGetInputBufferSize(self.cs)
    
    def outputBufferSize(self):
        """Return the number of samples in Csound's output buffer."""
        return libcsound.csoundGetOutputBufferSize(self.cs)
    
    def inputBuffer(self):
        """Return the Csound audio input buffer as a numpy array.
        
        Enable external software to write audio into Csound before
        calling performBuffer.
        """
        buf = libcsound.csoundGetInputBuffer(self.cs)
        size = libcsound.csoundGetInputBufferSize(self.cs)
        arrayType = np.ctypeslib.ndpointer(MYFLT, 1, (size,), 'C_CONTIGUOUS')
        p = cast(addressof(buf), arrayType)
        return np.ctypeslib.as_array(p)
    
    def outputBuffer(self):
        """Return the Csound audio output buffer as a numpy array.
        
        Enable external software to read audio from Csound after
        calling performBuffer.
        """
        buf = libcsound.csoundGetOutputBuffer(self.cs)
        size = libcsound.csoundGetOutputBufferSize(self.cs)
        arrayType = np.ctypeslib.ndpointer(MYFLT, 1, (size,), 'C_CONTIGUOUS')
        p = cast(addressof(buf), arrayType)
        return np.ctypeslib.as_array(p)
    
    def spin(self):
        """Return the Csound audio input working buffer (spin) as a numpy array.
        
        Enables external software to write audio into Csound before
        calling performKsmps.
        """
        buf = libcsound.csoundGetSpin(self.cs)
        size = self.ksmps() * self.nchnlsInput()
        arrayType = np.ctypeslib.ndpointer(MYFLT, 1, (size,), 'C_CONTIGUOUS')
        p = cast(addressof(buf), arrayType)
        return np.ctypeslib.as_array(p)
    
    def addSpinSample(self, frame, channel, sample):
        """Add the indicated sample into the audio input working buffer (spin).
        
        This only ever makes sense before calling performKsmps(). The frame
        and channel must be in bounds relative to ksmps and nchnlsInput.
        """
        libcsound.csoundAddSpinSample(self.cs, frame, channel, sample)
    
    def spout(self):
        """Return the address of the Csound audio output working buffer (spout).
        
        Enable external software to read audio from Csound after
        calling performKsmps.
        """
        buf = libcsound.csoundGetSpout(self.cs)
        size = self.ksmps() * self.nchnls()
        arrayType = np.ctypeslib.ndpointer(MYFLT, 1, (size,), 'C_CONTIGUOUS')
        p = cast(addressof(buf), arrayType)
        return np.ctypeslib.as_array(p)
    
    def spoutSample(self, frame, channel):
        """Return one sample from the Csound audio output working buf (spout).
        
        Only ever makes sense after calling performKsmps(). The frame and
        channel must be in bounds relative to ksmps and nchnls.
        """
        return libcsound.csoundGetSpoutSample(self.cs, frame, channel)
    
    def rtRecordUserData(self):
        """Return pointer to user data pointer for real time audio input."""
        return libcsound.csoundGetRtRecordUserData(self.cs)

    def rtPlaydUserData(self):
        """Return pointer to user data pointer for real time audio output."""
        return libcsound.csoundGetRtPlayUserData(self.cs)

    def setHostImplementedAudioIO(self, state, bufSize):
        """Set user handling of sound I/O.
        
        Calling this function with a non-zero 'state' value between creation of
        the Csound object and the start of performance will disable all default
        handling of sound I/O by the Csound library, allowing the host
        application to use the spin/spout/input/output buffers directly.
        If 'bufSize' is greater than zero, the buffer size (-b) will be
        set to the integer multiple of ksmps that is nearest to the value
        specified.
        """
        libcsound.csoundSetHostImplementedAudioIO(self.cs, state, bufSize)

    def audioDevList(self, isOutput):
        """Return a list of available input or output audio devices.
        
        Each item in the list is a dictionnary representing a device. The
        dictionnary keys are "device_name", "device_id", "rt_module" (value
        type string), "max_nchnls" (value type int), and "output" (value 
        type boolean). Must be called after an orchestra has been compiled
        to get meaningful information.
        """
        n = libcsound.csoundGetAudioDevList(self.cs, None, c_int(isOutput))
        devs = (csoundAudioDevice * n)()
        libcsound.csoundGetAudioDevList(self.cs, byref(devs), c_int(isOutput))
        lst = []
        for dev in devs:
            d = {}
            d["device_name"] = pstring(dev.device_name)
            d["device_id"] = pstring(dev.device_id)
            d["rt_module"] = pstring(dev.rt_module)
            d["max_nchnls"] = dev.max_nchnls
            d["output"] = (dev.isOutput == 1)
            lst.append(d)
        return lst

    def setPlayOpenCallback(self, function):
        """Set a callback for opening real-time audio playback."""
        self.playOpenCb = PLAYOPENFUNC(function)
        libcsound.csoundSetPlayopenCallback(self.cs, self.playOpenCb)

