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

class CsoundAudioDevice(Structure):
    _fields_ = [("device_name", string64),
                ("device_id", string64),
                ("rt_module", string64),
                ("max_nchnls", c_int),
                ("isOutput", c_int)]

class CsoundMidiDevice(Structure):
    _fields_ = [("device_name", string64),
                ("interface_name", string64),
                ("device_id", string64),
                ("midi_module", string64),
                ("isOutput", c_int)]

class CsoundRtAudioParams(Structure):
    _fields_ = [("devName", c_char_p),   # device name (NULL/empty: default)
                ("devNum", c_int),       # device number (0-1023), 1024: default
                ("bufSamp_SW", c_uint),  # buffer fragment size (-b) in sample frames
                ("bufSamp_HW", c_int),   # total buffer size (-B) in sample frames
                ("nChannels", c_int),    # number of channels
                ("sampleFormat", c_int), # sample format (AE_SHORT etc.)
                ("sampleRate", c_float)] # sample rate in Hz

class OpcodeListEntry(Structure):
    _fields_ = [("opname", c_char_p),
                ("outypes", c_char_p),
                ("intypes", c_char_p),
                ("flags", c_int)]

# PVSDATEXT is a variation on PVSDAT used in the pvs bus interface
class PvsdatExt(Structure):
    _fields_ = [("N", c_int32),
                ("sliding", c_int),      # Flag to indicate sliding case
                ("NB", c_int32),
                ("overlap", c_int32),
                ("winsize", c_int32),
                ("wintype", c_int),
                ("format", c_int32),
                ("framecount", c_uint32),
                ("frame", POINTER(c_float))]

# This structure holds the parameter hints for control channels
class ControlChannelHints(Structure):
    _fields_ = [("behav", c_int),
                ("dflt", MYFLT),
                ("min", MYFLT),
                ("max", MYFLT),
                ("x", c_int),
                ("y", c_int),
                ("width", c_int),
                ("height", c_int),
                # This member must be set explicitly to None if not used
                ("attributes", c_char_p)]

class ControlChannelInfo(Structure):
    _fields_ = [("name", c_char_p),
                ("type", c_int),
                ("hints", ControlChannelHints)]

CAPSIZE  = 60

class Windat(Structure):
    _fields_ = [("windid", POINTER(c_uint)),    # set by makeGraph()
                ("fdata", POINTER(MYFLT)),      # data passed to drawGraph()
                ("npts", c_int32),              # size of above array
                ("caption", c_char * CAPSIZE),  # caption string for graph
                ("waitflg", c_int16 ),          # set =1 to wait for ms after Draw
                ("polarity", c_int16),          # controls positioning of X axis
                ("max", MYFLT),                 # workspace .. extrema this frame
                ("min", MYFLT),
                ("absmax", MYFLT),              # workspace .. largest of above
                ("oabsmax", MYFLT),             # Y axis scaling factor
                ("danflag", c_int),             # set to 1 for extra Yaxis mid span
                ("absflag", c_int)]             # set to 1 to skip abs check

# Symbols for Windat.polarity field
NOPOL = 0
NEGPOL = 1
POSPOL = 2
BIPOL = 3

class NamedGen(Structure):
    pass

NamedGen._fields_ = [
    ("name", c_char_p),
    ("genum", c_int),
    ("next", POINTER(NamedGen))]

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
libcsound.csoundCompileCsdText.argtypes = [c_void_p, c_char_p]

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
libcsound.csoundGetSpoutSample.restype = MYFLT
libcsound.csoundGetSpoutSample.argtypes = [c_void_p, c_int, c_int]
libcsound.csoundGetRtRecordUserData.restype = POINTER(c_void_p)
libcsound.csoundGetRtRecordUserData.argtypes = [c_void_p]
libcsound.csoundGetRtPlayUserData.restype = POINTER(c_void_p)
libcsound.csoundGetRtPlayUserData.argtypes = [c_void_p]
libcsound.csoundSetHostImplementedAudioIO.argtypes = [c_void_p, c_int, c_int]
libcsound.csoundGetAudioDevList.argtypes = [c_void_p, c_void_p, c_int]
PLAYOPENFUNC = CFUNCTYPE(c_int, c_void_p, POINTER(CsoundRtAudioParams))
libcsound.csoundSetPlayopenCallback.argtypes = [c_void_p, PLAYOPENFUNC]
RTPLAYFUNC = CFUNCTYPE(None, c_void_p, POINTER(MYFLT), c_int)
libcsound.csoundSetRtplayCallback.argtypes = [c_void_p, RTPLAYFUNC]
RECORDOPENFUNC = CFUNCTYPE(c_int, c_void_p, POINTER(CsoundRtAudioParams))
libcsound.csoundSetRecopenCallback.argtypes = [c_void_p, RECORDOPENFUNC]
RTRECORDFUNC = CFUNCTYPE(c_int, c_void_p, POINTER(MYFLT), c_int)
libcsound.csoundSetRtrecordCallback.argtypes = [c_void_p, RTRECORDFUNC]
RTCLOSEFUNC = CFUNCTYPE(None, c_void_p)
libcsound.csoundSetRtcloseCallback.argtypes = [c_void_p, RTCLOSEFUNC]
AUDIODEVLISTFUNC = CFUNCTYPE(c_int, c_void_p, POINTER(CsoundAudioDevice), c_int)
libcsound.csoundSetAudioDeviceListCallback.argtypes = [c_void_p, AUDIODEVLISTFUNC]

libcsound.csoundSetMIDIModule.argtypes = [c_void_p, c_char_p]
libcsound.csoundSetHostImplementedMIDIIO.argtypes = [c_void_p, c_int]
libcsound.csoundGetMIDIDevList.argtypes = [c_void_p, c_void_p, c_int]
MIDIINOPENFUNC = CFUNCTYPE(c_int, c_void_p, POINTER(c_void_p), c_char_p)
libcsound.csoundSetExternalMidiInOpenCallback.argtypes = [c_void_p, MIDIINOPENFUNC]
MIDIREADFUNC = CFUNCTYPE(c_int, c_void_p, c_void_p, c_char_p, c_int)
libcsound.csoundSetExternalMidiReadCallback.argtypes = [c_void_p, MIDIREADFUNC]
MIDIINCLOSEFUNC = CFUNCTYPE(c_int, c_void_p, c_void_p)
libcsound.csoundSetExternalMidiInCloseCallback.argtypes = [c_void_p, MIDIINCLOSEFUNC]
MIDIOUTOPENFUNC = CFUNCTYPE(c_int, c_void_p, POINTER(c_void_p), c_char_p)
libcsound.csoundSetExternalMidiOutOpenCallback.argtypes = [c_void_p, MIDIOUTOPENFUNC]
MIDIWRITEFUNC = CFUNCTYPE(c_int, c_void_p, c_void_p, c_char_p, c_int)
libcsound.csoundSetExternalMidiWriteCallback.argtypes = [c_void_p, MIDIWRITEFUNC]
MIDIOUTCLOSEFUNC = CFUNCTYPE(c_int, c_void_p, c_void_p)
libcsound.csoundSetExternalMidiOutCloseCallback.argtypes = [c_void_p, MIDIOUTCLOSEFUNC]
MIDIERRORFUNC = CFUNCTYPE(c_char_p, c_int)
libcsound.csoundSetExternalMidiErrorStringCallback.argtypes = [c_void_p, MIDIERRORFUNC]
MIDIDEVLISTFUNC = CFUNCTYPE(c_int, c_void_p, POINTER(CsoundMidiDevice), c_int)
libcsound.csoundSetMIDIDeviceListCallback.argtypes = [c_void_p, MIDIDEVLISTFUNC]

libcsound.csoundReadScore.argtypes = [c_void_p, c_char_p]
libcsound.csoundGetScoreTime.restype = c_double
libcsound.csoundGetScoreTime.argtypes = [c_void_p]
libcsound.csoundIsScorePending.argtypes = [c_void_p]
libcsound.csoundSetScorePending.argtypes = [c_void_p, c_int]
libcsound.csoundGetScoreOffsetSeconds.restype = MYFLT
libcsound.csoundGetScoreOffsetSeconds.argtypes = [c_void_p]
libcsound.csoundSetScoreOffsetSeconds.argtypes = [c_void_p, MYFLT]
libcsound.csoundRewindScore.argtypes = [c_void_p]
CSCOREFUNC = CFUNCTYPE(None, c_void_p)
libcsound.csoundSetCscoreCallback.argtypes = [c_void_p, CSCOREFUNC]

libcsound.csoundMessage.argtypes = [c_void_p, c_char_p, c_char_p]
libcsound.csoundMessageS.argtypes = [c_void_p, c_int, c_char_p, c_char_p]
libcsound.csoundSetMessageLevel.argtypes = [c_void_p, c_int]
libcsound.csoundCreateMessageBuffer.argtypes = [c_void_p, c_int]
libcsound.csoundGetFirstMessage.restype = c_char_p
libcsound.csoundGetFirstMessage.argtypes = [c_void_p]
libcsound.csoundGetFirstMessageAttr.argtypes = [c_void_p]
libcsound.csoundPopFirstMessage.argtypes = [c_void_p]
libcsound.csoundGetMessageCnt.argtypes = [c_void_p]
libcsound.csoundDestroyMessageBuffer.argtypes = [c_void_p]

libcsound.csoundGetChannelPtr.argtypes = [c_void_p, POINTER(POINTER(MYFLT)), c_char_p, c_int]
libcsound.csoundListChannels.argtypes = [c_void_p, POINTER(POINTER(ControlChannelInfo))]
libcsound.csoundDeleteChannelList.argtypes = [c_void_p, POINTER(ControlChannelInfo)]
libcsound.csoundSetControlChannelHints.argtypes = [c_void_p, c_char_p, ControlChannelHints]
libcsound.csoundGetControlChannelHints.argtypes = [c_void_p, c_char_p, POINTER(ControlChannelHints)]
libcsound.csoundGetChannelLock.restype = POINTER(c_int)
libcsound.csoundGetChannelLock.argtypes = [c_void_p, c_char_p]
libcsound.csoundGetControlChannel.restype = MYFLT
libcsound.csoundGetControlChannel.argtypes = [c_void_p, c_char_p, POINTER(c_int)]
libcsound.csoundSetControlChannel.argtypes = [c_void_p, c_char_p, MYFLT]
libcsound.csoundGetAudioChannel.argtypes = [c_void_p, c_char_p, POINTER(c_int)]
libcsound.csoundSetAudioChannel.argtypes = [c_void_p, c_char_p, POINTER(c_int)]
libcsound.csoundGetStringChannel.argtypes = [c_void_p, c_char_p, c_char_p]
libcsound.csoundSetStringChannel.argtypes = [c_void_p, c_char_p, c_char_p]
libcsound.csoundGetChannelDatasize.argtypes = [c_void_p, c_char_p]
CHANNELFUNC = CFUNCTYPE(None, c_void_p, c_char_p, c_void_p, c_void_p)
libcsound.csoundSetInputChannelCallback.argtypes = [c_void_p, CHANNELFUNC]
libcsound.csoundSetOutputChannelCallback.argtypes = [c_void_p, CHANNELFUNC]
libcsound.csoundSetPvsChannel.argtypes = [c_void_p, POINTER(PvsdatExt), c_char_p]
libcsound.csoundGetPvsChannel.argtypes = [c_void_p, POINTER(PvsdatExt), c_char_p]
libcsound.csoundScoreEvent.argtypes = [c_void_p, c_char, POINTER(MYFLT), c_long]
libcsound.csoundScoreEventAbsolute.argtypes = [c_void_p, c_char, POINTER(MYFLT), c_long, c_double]
libcsound.csoundInputMessage.argtypes = [c_void_p, c_char_p]
libcsound.csoundKillInstance.argtypes = [c_void_p, MYFLT, c_char_p, c_int, c_int]
SENSEFUNC = CFUNCTYPE(None, c_void_p, py_object)
libcsound.csoundRegisterSenseEventCallback.argtypes = [c_void_p, SENSEFUNC, py_object]
libcsound.csoundKeyPress.argtypes = [c_void_p, c_char]
KEYBOARDFUNC = CFUNCTYPE(c_int, py_object, c_void_p, c_uint)
libcsound.csoundRegisterKeyboardCallback.argtypes = [c_void_p, KEYBOARDFUNC, py_object, c_uint]
libcsound.csoundRemoveKeyboardCallback.argtypes = [c_void_p, KEYBOARDFUNC]

libcsound.csoundTableLength.argtypes = [c_void_p, c_int]
libcsound.csoundTableGet.restype = MYFLT
libcsound.csoundTableGet.argtypes = [c_void_p, c_int, c_int]
libcsound.csoundTableSet.argtypes = [c_void_p, c_int, c_int, MYFLT]
libcsound.csoundTableCopyOut.argtypes = [c_void_p, c_int, POINTER(MYFLT)]
libcsound.csoundTableCopyIn.argtypes = [c_void_p, c_int, POINTER(MYFLT)]
libcsound.csoundGetTable.argtypes = [c_void_p, POINTER(POINTER(MYFLT)), c_int]
libcsound.csoundGetTableArgs.argtypes = [c_void_p, POINTER(POINTER(MYFLT)), c_int]

libcsound.csoundSetIsGraphable.argtypes = [c_void_p, c_int]
MAKEGRAPHFUNC = CFUNCTYPE(None, c_void_p, POINTER(Windat), c_char_p)
libcsound.csoundSetMakeGraphCallback.argtypes = [c_void_p, MAKEGRAPHFUNC]
DRAWGRAPHFUNC = CFUNCTYPE(None, c_void_p, POINTER(Windat))
libcsound.csoundSetDrawGraphCallback.argtypes = [c_void_p, DRAWGRAPHFUNC]
KILLGRAPHFUNC = CFUNCTYPE(None, c_void_p, POINTER(Windat))
libcsound.csoundSetKillGraphCallback.argtypes = [c_void_p, KILLGRAPHFUNC]
EXITGRAPHFUNC = CFUNCTYPE(c_int, c_void_p)
libcsound.csoundSetExitGraphCallback.argtypes = [c_void_p, EXITGRAPHFUNC]

libcsound.csoundGetNamedGens.restype = c_void_p
libcsound.csoundGetNamedGens.argtypes = [c_void_p]
libcsound.csoundNewOpcodeList.argtypes = [c_void_p, POINTER(POINTER(OpcodeListEntry))]
libcsound.csoundDisposeOpcodeList.argtypes = [c_void_p, POINTER(OpcodeListEntry)]
OPCODEFUNC = CFUNCTYPE(c_int, c_void_p, c_void_p)
libcsound.csoundAppendOpcode.argtypes = [c_void_p, c_char_p, c_int, c_int, c_int, \
                                         c_char_p, c_char_p, OPCODEFUNC, OPCODEFUNC, OPCODEFUNC]

def cstring(s):
    if sys.version_info[0] >= 3 and s != None:
        return bytes(s, 'utf-8')
    return s

def pstring(s):
    if sys.version_info[0] >= 3and s != None:
        return str(s, 'utf-8')
    return s

def csoundArgList(lst):
    argc = len(lst)
    argv = (POINTER(c_char_p) * argc)()
    for i in range(argc):
        v = cstring(lst[i])
        argv[i] = cast(pointer(create_string_buffer(v)), POINTER(c_char_p))
    return c_int(argc), cast(argv, POINTER(c_char_p))

# message types (only one can be specified)
CSOUNDMSG_DEFAULT = 0x0000       # standard message
CSOUNDMSG_ERROR = 0x1000         # error message (initerror, perferror, etc.)
CSOUNDMSG_ORCH = 0x2000          # orchestra opcodes (e.g. printks)
CSOUNDMSG_REALTIME = 0x3000      # for progress display and heartbeat characters
CSOUNDMSG_WARNING = 0x4000       # warning messages

# format attributes (colors etc.), use the bitwise OR of any of these:
CSOUNDMSG_FG_BLACK = 0x0100
CSOUNDMSG_FG_RED = 0x0101
CSOUNDMSG_FG_GREEN = 0x0102
CSOUNDMSG_FG_YELLOW = 0x0103
CSOUNDMSG_FG_BLUE = 0x0104
CSOUNDMSG_FG_MAGENTA = 0x0105
CSOUNDMSG_FG_CYAN = 0x0106
CSOUNDMSG_FG_WHITE = 0x0107

CSOUNDMSG_FG_BOLD = 0x0008
CSOUNDMSG_FG_UNDERLINE = 0x0080

CSOUNDMSG_BG_BLACK = 0x0200
CSOUNDMSG_BG_RED = 0x0210
CSOUNDMSG_BG_GREEN = 0x0220
CSOUNDMSG_BG_ORANGE = 0x0230
CSOUNDMSG_BG_BLUE = 0x0240
CSOUNDMSG_BG_MAGENTA = 0x0250
CSOUNDMSG_BG_CYAN = 0x0260
CSOUNDMSG_BG_GREY = 0x0270

CSOUNDMSG_TYPE_MASK = 0x7000
CSOUNDMSG_FG_COLOR_MASK = 0x0107
CSOUNDMSG_FG_ATTR_MASK = 0x0088
CSOUNDMSG_BG_COLOR_MASK = 0x0270


# ERROR DEFINITIONS
CSOUND_SUCCESS = 0               # Completed successfully.
CSOUND_ERROR = -1                # Unspecified failure.
CSOUND_INITIALIZATION = -2       # Failed during initialization.
CSOUND_PERFORMANCE = -3          # Failed during performance.
CSOUND_MEMORY = -4               # Failed to allocate requested memory.
CSOUND_SIGNAL = -5               # Termination requested by SIGINT or SIGTERM.

# Constants used by the bus interface (csoundGetChannelPtr() etc.).
CSOUND_CONTROL_CHANNEL = 1
CSOUND_AUDIO_CHANNEL  = 2
CSOUND_STRING_CHANNEL = 3
CSOUND_PVS_CHANNEL = 4
CSOUND_VAR_CHANNEL = 5

CSOUND_CHANNEL_TYPE_MASK = 15

CSOUND_INPUT_CHANNEL = 16
CSOUND_OUTPUT_CHANNEL = 32

CSOUND_CONTROL_CHANNEL_NO_HINTS  = 0
CSOUND_CONTROL_CHANNEL_INT  = 1
CSOUND_CONTROL_CHANNEL_LIN  = 2
CSOUND_CONTROL_CHANNEL_EXP  = 3

class Csound:
    # Instantiation
    def __init__(self, hostData=None):
        """Creates an instance of Csound.
       
        Get an opaque pointer that must be passed to most Csound API
        functions. The hostData parameter can be None, or it can be any
        sort of data; these data can be accessed from the Csound instance
        that is passed to callback routines.
        """
        self.cs = libcsound.csoundCreate(py_object(hostData))
    
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
    
    def compileCsd(self, csd_filename):
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
        return libcsound.csoundCompileCsd(self.cs, cstring(csd_filename))
    
    def compileCsdText(self, csd_text):
        """Compile a Csound input file contained in a string of text.
        
        The string of text includes command-line arguments, orchestra, score,
        etc., but it is not performed. Returns a non-zero error code on failure.
        In this (host-driven) mode, the sequence of calls should be as follows:
        
            cs.compileCsdText(csd_text);
            while (cs.performBuffer() == 0)
                pass
            cs.cleanup()
            cs.reset()
        
        NB: a temporary file is created, the csd_text is written to the
        temporary file, and compileCsd is called with the name of the temporary
        file, which is deleted after compilation. Behavior may vary by platform.
        """
        return libcsound.csoundCompileCsdText(self.cs, cstring(csd_text))

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
    
    # Attributes
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
        return libcsound.csoundSetOption(self.cs, cstring(option))
    
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
        libcsound.csoundSetFileOpenCallback(self.cs, FILEOPENFUNC(function))

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
                name, type_, err = cs.module(n)
                if err == ctcsound.CSOUND_ERROR:
                    break
                print("Module %d:%s (%s)\n" % (n, name, type_))
                n = n + 1
        """
        name = pointer(c_char_p(cstring("dummy")))
        type_ = pointer(c_char_p(cstring("dummy")))
        err = libcsound.csoundGetModule(self.cs, number, name, type_)
        if err == CSOUND_ERROR:
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
        
        Calling this function with a True 'state' value between creation of
        the Csound object and the start of performance will disable all default
        handling of sound I/O by the Csound library, allowing the host
        application to use the spin/spout/input/output buffers directly.
        If 'bufSize' is greater than zero, the buffer size (-b) will be
        set to the integer multiple of ksmps that is nearest to the value
        specified.
        """
        libcsound.csoundSetHostImplementedAudioIO(self.cs, c_int(state), bufSize)

    def audioDevList(self, isOutput):
        """Return a list of available input or output audio devices.
        
        Each item in the list is a dictionnary representing a device. The
        dictionnary keys are "device_name", "device_id", "rt_module" (value
        type string), "max_nchnls" (value type int), and "isOutput" (value 
        type boolean). Must be called after an orchestra has been compiled
        to get meaningful information.
        """
        n = libcsound.csoundGetAudioDevList(self.cs, None, c_int(isOutput))
        devs = (CsoundAudioDevice * n)()
        libcsound.csoundGetAudioDevList(self.cs, byref(devs), c_int(isOutput))
        lst = []
        for dev in devs:
            d = {}
            d["device_name"] = pstring(dev.device_name)
            d["device_id"] = pstring(dev.device_id)
            d["rt_module"] = pstring(dev.rt_module)
            d["max_nchnls"] = dev.max_nchnls
            d["isOutput"] = (dev.isOutput == 1)
            lst.append(d)
        return lst

    def setPlayOpenCallback(self, function):
        """Set a callback for opening real-time audio playback."""
        libcsound.csoundSetPlayopenCallback(self.cs, PLAYOPENFUNC(function))

    def setRtPlayCallback(self, function):
        """Set a callback for performing real-time audio playback."""
        libcsound.csoundSetRtplayCallback(self.cs, RTPLAYFUNC(function))
  
    def setRecordOpenCallback(self, function):
        """Set a callback for opening real-time audio recording."""
        libcsound.csoundSetRecopenCallback(self.cs, RECORDOPENFUNC(function))

    def setRtRecordCallback(self, function):
        """Set a callback for performing real-time audio recording."""
        libcsound.csoundSetRtrecordCallback(self.cs, RTRECORDFUNC(function))
    
    def setRtCloseCallback(self, function):
        """Set a callback for closing real-time audio playback and recording."""
        libcsound.csoundSetRtcloseCallback(self.cs, RTCLOSEFUNC(function))
    
    def setAudioDevListCallback(self, function):
        """Set a callback for obtaining a list of audio devices.
        
        This should be set by rtaudio modules and should not be set by hosts.
        (See audioDevList()).
        """
        libcsound.csoundSetAudioDeviceListCallback(self.cs, AUDIODEVLISTFUNC(function))
    
    #Realtime MIDI I/O
    def setMIDIModule(self, module):
        """Sets the current MIDI IO module."""
        libcsound.csoundSetMIDIModule(self.cs, cstring(module))
    
    def setHostImplementedMIDIIO(self, state):
        """Called with state True if the host is implementing via callbacks."""
        libcsound.csoundSetHostImplementedMIDIIO(self.cs, c_int(state))
    
    def midiDevList(self, isOutput):
        """Return a list of available input or output midi devices.
        
        Each item in the list is a dictionnary representing a device. The
        dictionnary keys are "device_name", "interface_name", "device_id",
        "midi_module" (value type string), "isOutput" (value type boolean).
        Must be called after an orchestra has been compiled
        to get meaningful information.
        """
        n = libcsound.csoundGetMIDIDevList(self.cs, None, c_int(isOutput))
        devs = (csoundMidiDevice * n)()
        libcsound.csoundGetMIDIDevList(self.cs, byref(devs), c_int(isOutput))
        lst = []
        for dev in devs:
            d = {}
            d["device_name"] = pstring(dev.device_name)
            d["interface_name"] = pstring(dev.max_nchnlsinterface_name)
            d["device_id"] = pstring(dev.device_id)
            d["midi_module"] = pstring(dev.midi_module)
            d["isOutput"] = (dev.isOutput == 1)
            lst.append(d)
        return lst

    def setExternalMidiInOpenCallback(self, function):
        """Set a callback for opening real-time MIDI input."""
        libcsound.csoundSetExternalMidiInOpenCallback(self.cs, MIDIINOPENFUNC(function))

    def setExternalMidiReadCallback(self, function):
        """Set a callback for reading from real time MIDI input."""
        libcsound.csoundSetExternalMidiReadCallback(self.cs, MIDIREADFUNC(function))
    
    def setExternalMidiInCloseCallback(self, function):
        """Set a callback for closing real time MIDI input."""
        libcsound.csoundSetExternalMidiInCloseCallback(self.cs, MIDIINCLOSEFUNC(function))
    
    def setExternalMidiOutOpenCallback(self, function):
        """Set a callback for opening real-time MIDI input."""
        libcsound.csoundSetExternalMidiOutOpenCallback(self.cs, MIDIOUTOPENFUNC(function))

    def setExternalMidiWriteCallback(self, function):
        """Set a callback for reading from real time MIDI input."""
        libcsound.csoundSetExternalMidiWriteCallback(self.cs, MIDIWRITEFUNC(function))
    
    def setExternalMidiOutCloseCallback(self, function):
        """Set a callback for closing real time MIDI input."""
        libcsound.csoundSetExternalMidiOutCloseCallback(self.cs, MIDIOUTCLOSEFUNC(function))

    def setExternalMidiErrorStringCallback(self, function):
        """ Set a callback for converting MIDI error codes to strings."""
        libcsound.csoundSetExternalMidiErrorStringCallback(self.cs, MIDIERRORFUNC(function))
    
    def setMidiDevListCallback(self, function):
        """Set a callback for obtaining a list of MIDI devices.
        
        This should be set by IO plugins and should not be set by hosts.
        (See midiDevList()).
        """
        libcsound.csoundSetMIDIDeviceListCallback(self.cs, MIDIDEVLISTFUNC(function))

    #Score Handling
    def readScore(self, sco):
        """Read, preprocess, and load a score from an ASCII string.
        
        It can be called repeatedly, with the new score events
        being added to the currently scheduled ones.
        """
        return libcsound.csoundReadScore(self.cs, cstring(sco))
    
    def scoreTime(self):
        """Returns the current score time.
        
        The return value is the time in seconds since the beginning of
        performance.
        """
        return libcsound.csoundGetScoreTime(self.cs)
    
    def isScorePending(self):
        """Tell whether Csound score events are performed or not.
        
        Independently of real-time MIDI events (see setScorePending()).
        """
        return libcsound.csoundIsScorePending(self.cs)
    
    def setScorePending(self, pending):
        """Set whether Csound score events are performed or not.
        
        Real-time events will continue to be performed. Can be used by external
        software, such as a VST host, to turn off performance of score events
        (while continuing to perform real-time events), for example to mute
        a Csound score while working on other tracks of a piece, or to play
        the Csound instruments live.
        """
        libcsound.csoundSetScorePending(self.cs, c_int(pending))
    
    def scoreOffsetSeconds(self):
        """Return the score time beginning midway through a Csound score.
        
        At this time score events will actually immediately be performed
        (see setScoreOffsetSeconds()).
        """
        return libcsound.csoundGetScoreOffsetSeconds(self.cs)

    def setScoreOffsetSeconds(self, time):
        """Csound score events prior to the specified time are not performed.
        
        Performance begins immediately at the specified time (real-time events
        will continue to be performed as they are received). Can be used by
        external software, such as a VST host, to begin score performance
        midway through a Csound score, for example to repeat a loop in a
        sequencer, or to synchronize other events with the Csound score.
        """
        libcsound.csoundSetScoreOffsetSeconds(self.cs, MYFLT(time))
    
    def rewindScore(self):
        """Rewinds a compiled Csound score.
        
        It is rewinded to the time specified with setScoreOffsetSeconds().
        """
        libcsound.csoundRewindScore(self.cs)
    
    def setCscoreCallback(self, function):
        """Set an external callback for Cscore processing.
        
        Pass None to reset to the internal cscore() function (which does
        nothing). This callback is retained after a reset() call.
        """
        libcsound.csoundSetCscoreCallback(self.cs, CSCOREFUNC(function))
    
    #def scoreSort(self, inFile, outFile):
    
    #def scoreExtract(self, inFile, outFile, extractFile)
    
    #Messages and Text
    def message(self, fmt, *args):
        """Display an informational message.
        
        This is a workaround because ctypes does not support variadic functions.
        The arguments are formatted in a string, using the python way, either
        old style or new style, and then this formatted string is passed to
        the csound display message system.
        """
        if fmt[0] == '{':
            s = fmt.format(*args)
        else:
            s = fmt % args
        libcsound.csoundMessage(self.cs, cstring("%s"), cstring(s))
    
    def messageS(self, attr, fmt, *args):
        """Print message with special attributes.
        
        (See msg_attr for the list of available attributes). With attr=0,
        messageS() is identical to message().
        This is a workaround because ctypes does not support variadic functions.
        The arguments are formatted in a string, using the python way, either
        old style or new style, and then this formatted string is passed to
        the csound display message system.
        """
        if fmt[0] == '{':
            s = fmt.format(*args)
        else:
            s = fmt % args
        libcsound.csoundMessageS(self.cs, attr, cstring("%s"), cstring(s))

    #def setDefaultMessageCallback():
    
    #def setMessageCallback():
    
    def setMessageLevel(self, messageLevel):
        """Set the Csound message level (from 0 to 231)."""
        libcsound.csoundSetMessageLevel(self.cs, messageLevel)
    
    def createMessageBuffer(self, toStdOut):
        """Create a buffer for storing messages printed by Csound.
        
        Should be called after creating a Csound instance and the buffer
        can be freed by calling destroyMessageBuffer() before deleting the
        Csound instance. You will generally want to call cleanup() to make
        sure the last messages are flushed to the message buffer before
        destroying Csound.
        If 'toStdOut' is True, the messages are also printed to
        stdout and stderr (depending on the type of the message),
        in addition to being stored in the buffer.
        Using the message buffer ties up the internal message callback, so
        setMessageCallback should not be called after creating the
        message buffer.
        """
        libcsound.csoundCreateMessageBuffer(self.cs,  c_int(toStdOut))
    
    def firstMessage(self):
        """Return the first message from the buffer."""
        s = libcsound.csoundGetFirstMessage(self.cs)
        return pstring(s)
    
    def firstMessageAttr(self):
        """Return the attribute parameter of the first message in the buffer."""
        return libcsound.csoundGetFirstMessageAttr(self.cs)
    
    def popFirstMessage(self):
        """Remove the first message from the buffer."""
        libcsound.csoundPopFirstMessage(self.cs)
    
    def messageCnt(self):
        """Return the number of pending messages in the buffer."""
        return libcsound.csoundGetMessageCnt(self.cs)
    
    def destroyMessageBuffer(self):
        """Release all memory used by the message buffer."""
        libcsound.csoundDestroyMessageBuffer(self.cs)
    
    #Channels, Control and Events
    def channelPtr(self, name, type_):
        """Return a pointer to the specified channel and an error message.
        
        If the channel is a control or an audio channel, the pointer is
        translated to an ndarray of MYFLT. If the channel is a string channel,
        the pointer is casted to c_char_p. The error message is either an empty
        string or a string describing the error that occured.
        
        The channel is created first if it does not exist yet.
        'type_' must be the bitwise OR of exactly one of the following values,
          CSOUND_CONTROL_CHANNEL
            control data (one MYFLT value)
          CSOUND_AUDIO_CHANNEL
            audio data (csoundGetKsmps(csound) MYFLT values)
          CSOUND_STRING_CHANNEL
            string data (MYFLT values with enough space to store
            csoundGetChannelDatasize() characters, including the
            NULL character at the end of the string)
        and at least one of these:
          CSOUND_INPUT_CHANNEL
          CSOUND_OUTPUT_CHANNEL
        If the channel already exists, it must match the data type
        (control, audio, or string), however, the input/output bits are
        OR'd with the new value. Note that audio and string channels
        can only be created after calling csoundCompile(), because the
        storage size is not known until then.

        In the C API, return value is zero on success, or a negative error code,
          CSOUND_MEMORY  there is not enough memory for allocating the channel
          CSOUND_ERROR   the specified name or type is invalid
        or, if a channel with the same name but incompatible type
        already exists, the type of the existing channel. In the case
        of any non-zero return value, *p is set to NULL.
        Note: to find out the type of a channel without actually
        creating or changing it, set 'type' to zero, so that the return
        value will be either the type of the channel, or CSOUND_ERROR
        if it does not exist.
        
        Operations on the pointer are not thread-safe by default. The host is
        required to take care of threadsafety by retrieving the channel lock
        with channelLock() and using spinLock() and spinUnLock() to protect
        access to the pointer.
        See Top/threadsafe.c in the Csound library sources for
        examples.  Optionally, use the channel get/set functions
        provided below, which are threadsafe by default.
        """
        length = 0
        chanType = type_ & CSOUND_CHANNEL_TYPE_MASK
        if chanType == CSOUND_CONTROL_CHANNEL:
            length = 1
        elif chanType == CSOUND_AUDIO_CHANNEL:
            length = libcsound.csoundGetKsmps(self.cs)
        ptr = pointer(MYFLT(0.0))
        err = ''
        ret = libcsound.csoundGetChannelPtr(self.cs, byref(ptr), cstring(name), type_)
        if ret == CSOUND_SUCCESS:
            if chanType == CSOUND_STRING_CHANNEL:
                return cast(ptr, c_char_p), err
            else:
                arrayType = np.ctypeslib.ndpointer(MYFLT, 1, (length,), 'C_CONTIGUOUS')
                p = cast(addressof(ptr), arrayType)
                return np.ctypeslib.as_array(p), err
        elif ret == CSOUND_MEMORY:
            err = 'Not enough memory for allocating channel'
        elif ret == CSOUND_ERROR:
            err = 'The specified channel name or type is not valid'
        elif ret == CSOUND_CONTROL_CHANNEL:
            err = 'A control channel named {} already exists'.format(name)
        elif ret == CSOUND_AUDIO_CHANNEL:
            err = 'An audio channel named {} already exists'.format(name)
        elif ret == CSOUND_STRING_CHANNEL:
            err = 'A string channel named {} already exists'.format(name)
        else:
            err = 'Unknown error'
        return None, err
    
    def listChannels(self):
        """Return a pointer and an error message.
        
        The pointer points to a list of ControlChannelInfo objects for allocated
        channels. A ControlChannelInfo object contains the channel
        characteristics. The error message indicates if there is not enough
        memory for allocating the list or it is an empty string if there is no
        error. In the case of no channels or an error, the pointer is None.

        Notes: the caller is responsible for freeing the list returned by the
        C API with deleteChannelList(). The name pointers may become invalid
        after calling reset().
        """
        cInfos = None
        err = ''
        ptr = cast(pointer(MYFLT(0.0)), POINTER(ControlChannelInfo))
        n = libcsound.csoundListChannels(self.cs, byref(ptr))
        if n == CSOUND_MEMORY :
            err = 'There is not enough memory for allocating the list'
        if n > 0:
            cInfos = cast(ptr, POINTER(ControlChannelInfo * n)).contents
        return cInfos, err

    def deleteChannelList(self, lst):
        """Release a channel list previously returned by listChannels()."""
        ptr = cast(lst, POINTER(ControlChannelInfo))
        libcsound.csoundDeleteChannelList(self.cs, ptr)
    
    def setControlChannelHints(self, name, hints):
        """Set parameters hints for a control channel.
        
        These hints have no internal function but can be used by front ends to
        construct GUIs or to constrain values. See the ControlChannelHints
        structure for details.
        Returns zero on success, or a non-zero error code on failure:
          CSOUND_ERROR:  the channel does not exist, is not a control channel,
                         or the specified parameters are invalid
          CSOUND_MEMORY: could not allocate memory
        """
        return libcsound.csoundSetControlChannelHints(self.cs, cstring(name), hints)

    def controlChannelHints(self, name):
        """Return special parameters (if any) of a control channel.
        
        Those parameters have been previously set with setControlChannelHints()
        or the chnparams opcode.
       
        The return values are a ControlChannelHints structure and CSOUND_SUCCESS
        if the channel exists and is a control channel, otherwise, None and an
        error code are returned.
        """
        hints = ControlChannelHints()
        ret = libcsound.csoundGetControlChannelHints(self.cs, cstring(name), byref(hints))
        if ret != CSOUND_SUCCESS:
            hints = None
        return hints, ret
    
    def channelLock(self, name):
        """Recover a pointer to a lock for the specified channel called 'name'.
        
        
        The returned lock can be locked/unlocked  with the spinLock() and
        spinUnLock() functions.
        Return the address of the lock or NULL if the channel does not exist.
        """
        return libcsound.csoundGetChannelLock(self.cs, cstring(name))
    
    def controlChannel(self, name):
        """Retrieve the value of control channel identified by name.
        
        A second value is returned, which the error (or success) code
        finding or accessing the channel.
        """
        err = c_int(0)
        ret = libcsound.csoundGetControlChannel(self.cs, cstring(name), byref(err))
        return ret, err
    
    def setControlChannel(self, name, val):
        """Set the value of control channel identified by name."""
        libcsound.csoundSetControlChannel(self.cs, cstring(name), MYFLT(val))
    
    def audioChannel(self, name, samples):
        """Copy the audio channel identified by name into ndarray samples.
        
        samples should contain enough memory for ksmps MYFLTs.
        """
        ptr = samples.ctypes.data_as(POINTER(MYFLT))
        libcsound.csoundGetAudioChannel(self.cs, cstring(name), ptr)
    
    def setAudioChannel(self, name, samples):
        """Set the audio channel 'name' with data from ndarray 'samples'.
        
        'samples' should contain at least ksmps MYFLTs.
        """
        ptr = samples.ctypes.data_as(POINTER(MYFLT))
        libcsound.csoundSetAudioChannel(self.cs, cstring(name), ptr)
    
    def stringChannel(self, name, string):
        """Copy the string channel identified by name into string.
        
        string should contain enough memory for the string
        (see channelDatasize() below).
        """
        libcsound.csoundGetStringChannel(self.cs, cstring(name), cstring(string))

    def setStringChannel(self, name, string):
        """Set the string channel identified by name with string."""
        libcsound.csoundSetStringChannel(self.cs, cstring(name), cstring(string))
    
    def channelDatasize(self, name):
        """Return the size of data stored in a channel.
        
        For string channels this might change if the channel space gets
        reallocated. Since string variables use dynamic memory allocation in
        Csound6, this function can be called to get the space required for
        stringChannel().
        """
        return libcsound.csoundGetChannelDatasize(self.cs, cstring(name))

    def setInputChannelCallback(self, function):
        """Set the function to call whenever the invalue opcode is used."""
        libcsound.csoundSetInputChannelCallback(self.cs, CHANNELFUNC(function))
    
    def setOutputChannelCallback(self, function):
        """Set the function to call whenever the outvalue opcode is used."""
        libcsound.csoundSetOutputChannelCallback(self.cs, CHANNELFUNC(function))

    def setPvsChannel(self, fin, name):
        """Send a PvsdatExt fin to the pvsin opcode (f-rate) for channel 'name'.
        
        Return zero on success, CSOUND_ERROR if the index is invalid or
        fsig framesizes are incompatible.
        CSOUND_MEMORY if there is not enough memory to extend the bus.
        """
        return libcsound.csoundSetPvsChannel(self.cs, byref(fin), cstring(name))
    
    def pvsChannel(self, fout, name):
        """Receive a PvsdatExt fout from the pvsout opcode (f-rate) at channel 'name'.
        
        Return zero on success, CSOUND_ERROR if the index is invalid or
        if fsig framesizes are incompatible.
        CSOUND_MEMORY if there is not enough memory to extend the bus.
        """
        return libcsound.csoundGetPvsChannel(self.cs, byref(fout), cstring(name))
    
    def scoreEvent(self, type_, pFields):
        """Send a new score event.
        
        'type_' is the score event type ('a', 'i', 'q', 'f', or 'e').
        'pFields' is an ndarray of MYFLTs with all the pfields for this event,
        starting with the p1 value specified in pFields[0].
        """
        ptr = pFields.ctypes.data_as(POINTER(MYFLT))
        numFields = c_long(pFields.size)
        return libcsound.csoundScoreEvent(self.cs, c_char(type_), ptr, numFields)
    
    def scoreEventAbsolute(self, type_, pFields, timeOffset):
        """Like scoreEvent(), this function inserts a score event.
        
        The event is inserted at absolute time with respect to the start of
        performance, or from an offset set with timeOffset.
        """
        ptr = pFields.ctypes.data_as(POINTER(MYFLT))
        numFields = c_long(pFields.size)
        return libcsound.csoundScoreEventAbsolute(self.cs, c_char(type_), ptr, numFields, c_double(timeOffset))
    
    def inputMessage(self, message):
        """Input a NULL-terminated string (as if from a console).
        
        Used for line events.
        """
        libcsound.csoundInputMessage(self.cs, cstring(message))
    
    def killInstance(self, instr, instrName, mode, allowRelease):
        """Kills off one or more running instances of an instrument.
        
        The instances are identified by instr (number) or instrName (name).
        If instrName is None, the instrument number is used.
        Mode is a sum of the following values:
        0, 1, 2: kill all instances (0), oldest only (1), or newest (2)
        4: only turnoff notes with exactly matching (fractional) instr number
        8: only turnoff notes with indefinite duration (p3 < 0 or MIDI).
        If allowRelease is True, the killed instances are allowed to release.
        """
        return libcsound.csoundKillInstance(self.cs, MYFLT(instr), cstring(instrName), mode, c_int(allowRelease))
    
    def registerSenseEventCallback(self, function, userData):
        """Register a function to be called by sensevents().
        
        This function will be called once in every control period. Any number
        of functions may be registered, and will be called in the order of
        registration.
        The callback function takes two arguments: the Csound instance
        pointer, and the userData pointer as passed to this function.
        This facility can be used to ensure a function is called synchronously
        before every csound control buffer processing. It is important
        to make sure no blocking operations are performed in the callback.
        The callbacks are cleared on cleanup().
        Return zero on success.
        """
        return libcsound.csoundRegisterSenseEventCallback(self.cs, SENSEFUNC(function), py_object(userData))
    
    def kerPress(self, c):
        """Set the ASCII code of the most recent key pressed.
        
        This value is used by the 'sensekey' opcode if a callback for
        returning keyboard events is not set (see registerKeyboardCallback()).
        """
        libcsound.csoundKeyPress(self.cs, c_char(c))
    
    def registerKeyboardCallback(self, function, userData, type_):
        """Registers general purpose callback functions for keyboard events.
        
        These callbacks are called on every control period by the sensekey
        opcode.
        The callback is preserved on reset(), and multiple
        callbacks may be set and will be called in reverse order of
        registration. If the same function is set again, it is only moved
        in the list of callbacks so that it will be called first, and the
        user data and type mask parameters are updated. 'type_' can be the
        bitwise OR of callback types for which the function should be called,
        or zero for all types.
        Returns zero on success, CSOUND_ERROR if the specified function
        pointer or type mask is invalid, and CSOUND_MEMORY if there is not
        enough memory.
        
        The callback function takes the following arguments:
          userData
            the "user data" pointer, as specified when setting the callback
          p
            data pointer, depending on the callback type
          type_
            callback type, can be one of the following (more may be added in
            future versions of Csound):
              CSOUND_CALLBACK_KBD_EVENT
              CSOUND_CALLBACK_KBD_TEXT
                called by the sensekey opcode to fetch key codes. The data
                pointer is a pointer to a single value of type 'int', for
                returning the key code, which can be in the range 1 to 65535,
                or 0 if there is no keyboard event.
                For CSOUND_CALLBACK_KBD_EVENT, both key press and release
                events should be returned (with 65536 (0x10000) added to the
                key code in the latter case) as unshifted ASCII codes.
                CSOUND_CALLBACK_KBD_TEXT expects key press events only as the
                actual text that is typed.
        The return value should be zero on success, negative on error, and
        positive if the callback was ignored (for example because the type is
        not known).
        """
        return libcsound.csoundRegisterKeyboardCallback(self.cs, KEYBOARDFUNC(function), py_object(userData), c_uint(type_))
    
    def removeKeyboardCallback(self, function):
        """Remove a callback previously set with registerKeyboardCallback()."""
        libcsound.csoundRemoveKeyboardCallback(self.cs, KEYBOARDFUNC(function))
    
    #Tables
    def tableLength(self, table):
        """Return the length of a function table.
        
        (not including the guard point).
        If the table does not exist, return -1.
        """
        return libcsound.csoundTableLength(self.cs, table)
    
    def tableGet(self, table, index):
        """Return the value of a slot in a function table.
        
        The table number and index are assumed to be valid.
        """
        return libcsound.csoundTableGet(self.cs, table, index)
    
    def tableSet(self, table, index, value):
        """Set the value of a slot in a function table.
        
        The table number and index are assumed to be valid.
        """
        libcsound.csoundTableSet(self.cs, table, index, MYFLT(value))
    
    def tableCopyOut(self, table, dest):
        """Copy the contents of a function table into a supplied ndarray dest.
        
        The table number is assumed to be valid, and the destination needs to
        have sufficient space to receive all the function table contents.
        """
        ptr = dest.ctypes.data_as(POINTER(MYFLT))
        libcsound.csoundTableCopyOut(self.cs, table, ptr)
    
    def tableCopyIn(self, table, src):
        """Copy the contents of an ndarray src into a given function table.
        
        The table number is assumed to be valid, and the table needs to
        have sufficient space to receive all the array contents.
        """
        ptr = src.ctypes.data_as(POINTER(MYFLT))
        libcsound.csoundTableCopyIn(self.cs, table, ptr)
    
    def table(self, tableNum):
        """Return a pointer to function table 'tableNum' as an ndarray.
        
        The ndarray does not include the guard point. If the table does not
        exist, None is returned.
        """
        ptr = pointer(MYFLT(0.0))
        size = libcsound.csoundGetTable(self.cs, byref(ptr), tableNum)
        if size < 0:
            return None
        arrayType = np.ctypeslib.ndpointer(MYFLT, 1, (size,), 'C_CONTIGUOUS')
        p = cast(addressof(ptr), arrayType)
        return np.ctypeslib.as_array(p)
        
    def tableArgs(self, tableNum):
        """Return a pointer to the args used to generate a function table.
        
        The pointer is returned as an ndarray. If the table does not exist,
        None is returned.
        NB: the argument list starts with the GEN number and is followed by
        its parameters. eg. f 1 0 1024 10 1 0.5  yields the list
        {10.0, 1.0, 0.5}
        """
        ptr = pointer(MYFLT(0.0))
        size = libcsound.csoundGetTableArgs(self.cs, byref(ptr), tableNum)
        if size < 0:
            return None
        arrayType = np.ctypeslib.ndpointer(MYFLT, 1, (size,), 'C_CONTIGUOUS')
        p = cast(addressof(ptr), arrayType)
        return np.ctypeslib.as_array(p)
    
    #Function table display
    def setIsGraphable(self, isGraphable):
        """Tell Csound whether external graphic table display is supported.
        
        Return the previously set value (initially False).
        """
        ret = libcsound.csoundSetIsGraphable(self.cs, c_int(isGraphable))
        return (ret != 0)
    
    def setMakeGraphCallback(self, function):
        """Called by external software to set Csound's MakeGraph function."""
        libcsound.csoundSetMakeGraphCallback(self.cs, MAKEGRAPHFUNC(function))
        
    def setDrawGraphCallback(self, function):
        """Called by external software to set Csound's DrawGraph function."""
        libcsound.csoundSetDrawGraphCallback(self.cs, DRAWGRAPHFUNC(function))
    
    def setKillGraphCallback(self, function):
        """Called by external software to set Csound's KillGraph function."""
        libcsound.csoundSetKillGraphCallback(self.cs, KILLGRAPHFUNC(function))
    
    def setExitGraphCallback(self, function):
        """Called by external software to set Csound's ExitGraph function."""
        libcsound.csoundSetExitGraphCallback(self.cs, EXITGRAPHFUNC(function))
    
    #Opcodes
    def namedGens(self):
        """Find the list of named gens."""
        lst = []
        ptr = libcsound.csoundGetNamedGens(self.cs)
        ptr = cast(ptr, POINTER(NamedGen))
        while (ptr):
            ng = ptr.contents
            lst.append((pstring(ng.name), int(ng.genum)))
            ptr = ng.next
        return lst
    
    def newOpcodeList(self):
        """Get an alphabetically sorted list of all opcodes.
        
        Should be called after externals are loaded by compile_().
        Return a pointer to the list of OpcodeListEntry structures and the
        number of opcodes, or a negative error code on  failure.
        Make sure to call disposeOpcodeList() when done with the list.
        """
        opcodes = None
        ptr = cast(pointer(MYFLT(0.0)), POINTER(OpcodeListEntry))
        n = libcsound.csoundNewOpcodeList(self.cs, byref(ptr))
        if n > 0:
            opcodes = cast(ptr, POINTER(OpcodeListEntry * n)).contents
        return opcodes, n
    
    def disposeOpcodeList(self, lst):
        """Release an opcode list."""
        ptr = cast(lst, POINTER(OpcodeListEntry))
        libcsound.csoundDisposeOpcodeList(self.cs, ptr)

    def appendOpcode(self, opname, dsblksiz, flags, thread, outypes, intypes, iopfunc, kopfunc, aopfunc):
        """Appends an opcode implemented by external software.
        
        This opcode is added to Csound's internal opcode list.
        The opcode list is extended by one slot, and the parameters are copied
        into the new slot.
        Return zero on success.
        """
        return libcsound.csoundAppendOpcode(self.cs, cstring(opname), dsblksiz, flags, thread,\
                                            cstring(outypes), cstring(intypes),\
                                            OPCODEFUNC(iopfunc),\
                                            OPCODEFUNC(kopfunc),
                                            OPCODEFUNC(aopfunc))
    
