// CodeMirror, copyright (c) by Marijn Haverbeke and others, and Francois Pinot
// Distributed under an MIT license: http://codemirror.net/LICENSE

(function(mod) {
  if (typeof exports == "object" && typeof module == "object") // CommonJS
    mod(require("../../lib/codemirror"));
  else if (typeof define == "function" && define.amd) // AMD
    define(["../../lib/codemirror"], mod);
  else // Plain browser env
    mod(CodeMirror);
})(function(CodeMirror) {
"use strict";

CodeMirror.defineMode("csound", function(config) {
  var isOperatorChar = /[+\-*\/%^|&=<>!:?]/;
  
  var headers = {
    "0dbfs":true, "ctrlinit":true, "ftgen":true, "kr": true, "ksmps":true,
    "massign":true, "nchnls":true, "nchnls_i":true, "pgmassign":true,
    "pset":true, "sr":true, "strset":true
  };    
  
  var blockStatements = {
    "instr":true, "endin":true, "opcode":true, "endop":true
  };
  
  var atoms = {
    "cggoto":true, "cigoto":true, "ckgoto":true, "cngoto":true, "cogoto":true,
    "else":true, "elseif":true, "goto":true, "if":true, "igoto":true,
    "iholf":true, "kgoto":true, "loop_ge":true, "loop_gt":true, "loop_le":true,
    "loop_lt":true, "reinit":true, "rigoto":true, "rireturn":true, "then":true,
    "tigoto":true, "timout":true, "tival":true, "until":true, "do":true,
    "od":true, "while":true, "#define":true, "#include":true, "#undef":true
  };
  
  var keywords = {
    "cpuprc":true, "exitnow":true,
    "getcfg":true, "init":true, "insglobal":true, "insremot":true,
    "jack_transport":true,
    "maxalloc":true, "midglobal":true, "midremot":true, "mute":true,
    "prealloc":true,
    "remoteport":true, "remove":true, "seed":true,
    "setksmps":true, "turnoff":true,
    "turnoff2":true, "turnon":true,
    "abetarand":true, "abexprnd":true, "acauchy":true, "active":true,
    "adsr":true, "adsyn":true, "adsynt2":true, "adsynt":true, "aexprand":true,
    "aftouch":true, "agauss":true, "agogobel":true, "alinrand":true,
    "alpass":true, "ampmidi":true, "apcauchy":true, "apoisson":true,
    "apow":true, "areson":true, "aresonk":true, "atone":true, "atonek":true,
    "atonex":true, "atrirand":true, "ATSadd":true, "ATSaddnz":true,
    "ATSbufread":true, "ATScross":true, "ATSinfo":true, "ATSinterpread":true,
    "ATSpartialtap":true, "ATSread":true, "ATSreadnz":true, "ATSsinnoi":true,
    "aunirand":true, "aweibull":true, "babo":true, "balance":true,
    "bamboo":true, "barmodel":true, "bbcutm":true, "bbcuts":true,
    "betarand":true, "bexprnd":true, "bformdec":true, "bformenc":true,
    "biquad":true, "biquada":true, "binit":true, "bqrez":true, "butbp":true,
    "butbr":true, "buthp":true, "butlp":true, "butterbp":true,
    "butterbr":true, "butterhp":true, "butterlp":true, "button":true,
    "buzz":true, "cabasa":true, "cauchy":true, "chanctrl":true,
    "changed":true, "chani":true, "chano":true, "chebyshevpoly":true,
    "checkbox":true, "chn_S":true, "chn_a":true, "chn_k":true,
    "chnclear":true, "chnexport":true, "chnget":true, "chnmix":true,
    "chnparams":true, "chnrecv":true, "chnsend":true, "chnset":true,
    "clear":true, "clfilt":true, "clip":true, "clock":true, "clockoff":true,
    "clockon":true, "comb":true, "compress":true, "control":true,
    "convle":true, "convolve":true, "cps2pch":true, "cpsmidi":true,
    "cpsmidib":true, "cpstmid":true, "cpstun":true, "cpstuni":true,
    "cpsxpch":true, "cross2":true, "crossfm":true, "crossfmi":true,
    "crunch":true, "ctrl14":true, "ctrl21":true, "ctrl7":true,
    "cuserrnd":true, "dam":true, "date":true, "dates":true, "dcblock":true,
    "dconv":true, "delay":true, "delay1":true, "delayk":true, "delayr":true,
    "delayw":true, "deltap":true, "deltap3":true, "deltapi":true,
    "deltapn":true, "deltapx":true, "deltapxw":true, "denorm":true,
    "diff":true, "diskgrain":true, "diskin":true, "diskin2":true,
    "dispfft":true, "display":true, "distort":true, "distort1":true,
    "divz":true, "downsamp":true, "dripwater":true, "dumpk":true,
    "dumpk2":true, "dumpk3":true, "dumpk4":true, "duserrnd":true,
    "envlpx":true, "envlpxr":true, "eqfil":true, "event":true, "event_i":true,
    "expcurve":true, "expon":true, "exprand":true, "expseg":true,
    "expsega":true, "expsegr":true, "ficlose":true, "filelen":true,
    "filenchnls":true, "filepeak":true, "filesr":true, "filter2":true,
    "fin":true, "fini":true, "fink":true, "fiopen":true, "flanger":true,
    "flashtxt":true, "FLbox":true, "FLbutBank":true, "FLbutton":true,
    "FLcloseButton":true, "FLcolor":true, "FLcolor2":true, "FLcount":true,
    "FLexecButton":true, "FLgetsnap":true, "FLgroup":true, "FLgroup_end":true,
    "FLgroupEnd":true, "FLhide":true, "FLhvsBox":true,
    "FLhvsBoxSetValue":true, "FLjoy":true, "FLkeyb":true, "FLkeyIn":true,
    "FLknob":true, "FLlabel":true, "FLloadsnap":true, "FLmouse":true,
    "FLpack":true, "FLpack_end":true, "FLpackEnd":true, "FLpanel":true,
    "FLpanel_end":true, "FLpanelEnd":true, "FLprintk":true, "FLprintk2":true,
    "FLroller":true, "FLrun":true, "FLsavesnap":true, "FLscroll":true,
    "FLscroll_end":true, "FLscrollEnd":true, "FLsetAlign":true,
    "FLsetBox":true, "FLsetColor":true, "FLsetColor2":true, "FLsetFont":true,
    "FLsetPosition":true, "FLsetSize":true, "FLsetsnap":true,
    "FLsetSnapGroup":true, "FLsetText":true, "FLsetTextColor":true,
    "FLsetTextSize":true, "FLsetTextType":true, "FLsetVal_i":true,
    "FLsetVali":true, "FLsetVal":true, "FLshow":true, "FLslidBnk":true,
    "FLslidBnk2":true, "FLslidBnk2Set":true, "FLslidBnk2Setk":true,
    "FLslidBnkGetHandle":true, "FLslidBnkSet":true, "FLslidBnkSetk":true,
    "FLslider":true, "FLtabs":true, "FLtabs_end":true, "FLtabsEnd":true,
    "FLtext":true, "FLupdate":true, "FLvalue":true, "FLvkeybd":true,
    "FLvslidBnk":true, "FLvslidBnk2":true, "FLxyin":true, "flooper":true,
    "flooper2":true, "flooper3":true, "fluidAllOut":true, "fluidCCi":true,
    "fluidCCk":true, "fluidControl":true, "fluidEngine":true,
    "fluidLoad":true, "fluidNote":true, "fluidOut":true,
    "fluidProgramSelect":true, "fmb3":true, "fmbell":true, "fmmetal":true,
    "fmpercfl":true, "fmrhode":true, "fmvoice":true, "fmwurlie":true,
    "fof":true, "fof2":true, "fofilter":true, "fog":true, "fold":true,
    "follow":true, "follow2":true, "foscil":true, "foscili":true, "fout":true,
    "fouti":true, "foutir":true, "foutk":true, "fprintks":true,
    "fprints":true, "freeverb":true, "ftconv":true, "ftfree":true,
    "ftgentmp":true, "ftload":true, "ftloadk":true, "ftmorf":true,
    "ftsave":true, "ftsavek":true, "gain":true, "gainslider":true,
    "gauss":true, "gbuzz":true, "getrow":true, "gogobel":true, "grain":true,
    "grain2":true, "grain3":true, "granule":true, "guiro":true, "harmon":true,
    "harmon2":true, "harmon3":true, "harmon4":true, "hilbert":true,
    "hrtfer":true, "hrtfmove":true, "hrtfmove2":true, "hrtfstat":true,
    "hsboscil":true, "hvs1":true, "hvs2":true, "hvs3":true, "ibetarand":true,
    "ibexprnd":true, "icauchy":true, "ictrl14":true, "ictrl21":true,
    "ictrl7":true, "iexprand":true, "igauss":true, "ilinrand":true,
    "imagecreate":true, "imagefree":true, "imagegetpixel":true,
    "imageload":true, "imagesave":true, "imagesetpixel":true,
    "imagesize":true, "imidic14":true, "imidic21":true, "imidic7":true,
    "in":true, "in32":true, "inch":true, "inh":true, "initc14":true,
    "initc21":true, "initc7":true, "ink":true, "ino":true, "inq":true,
    "inrg":true, "ins":true, "instimek":true, "instimes":true, "integ":true,
    "interp":true, "invalue":true, "inx":true, "inz":true, "ioff":true,
    "ion":true, "iondur":true, "iondur2":true, "ioutat":true, "ioutc":true,
    "ioutc14":true, "ioutpat":true, "ioutpb":true, "ioutpc":true,
    "ipcauchy":true, "ipoisson":true, "ipow":true, "is16b14":true,
    "is32b14":true, "islider16":true, "islider32":true, "islider64":true,
    "islider8":true, "itablecopy":true, "itablegpw":true, "itablemix":true,
    "itablew":true, "itrirand":true, "iunirand":true, "iweibull":true,
    "jitter":true, "jitter2":true, "jspline":true, "kbetarand":true,
    "kbexprnd":true, "kcauchy":true, "kdump":true, "kdump2":true,
    "kdump3":true, "kdump4":true, "kexprand":true, "kfilter2":true,
    "kgauss":true, "klinrand":true, "kon":true, "koutat":true, "koutc":true,
    "koutc14":true, "koutpat":true, "koutpb":true, "koutpc":true,
    "kpcauchy":true, "kpoisson":true, "kpow":true, "kread":true,
    "kread2":true, "kread3":true, "kread4":true, "ktableseg":true,
    "ktrirand":true, "kunirand":true, "kweibull":true, "lfo":true,
    "limit":true, "line":true, "linen":true, "linenr":true, "lineto":true,
    "linrand":true, "linseg":true, "linsegr":true, "locsend":true,
    "locsig":true, "logcurve":true, "loopseg":true, "loopsegp":true,
    "lorenz":true, "loscil":true, "loscil3":true, "loscilx":true,
    "lowpass2":true, "lowres":true, "lowresx":true, "lpf18":true,
    "lpfreson":true, "lphasor":true, "lpinterp":true, "lposcil":true,
    "lposcil3":true, "lposcila":true, "lposcilsa":true, "lposcilsa2":true,
    "lpread":true, "lpreson":true, "lpshold":true, "lpsholdp":true,
    "lpslot":true, "mac":true, "maca":true, "madsr":true, "mandel":true,
    "mandol":true, "marimba":true, "max":true, "max_k":true, "maxabs":true,
    "maxabsaccum":true, "maxaccum":true, "maxk":true, "mclock":true,
    "mdelay":true, "metro":true, "midic14":true, "midic21":true,
    "midic7":true, "midichannelaftertouch":true, "midichn":true,
    "midicontrolchange":true, "midictrl":true, "mididefault":true,
    "midiin":true, "midinoteoff":true, "midinoteoncps":true,
    "midinoteonkey":true, "midinoteonoct":true, "midinoteonpch":true,
    "midion":true, "midion2":true, "midiout":true, "midipitchbend":true,
    "midipolyaftertouch":true, "midiprogramchange":true, "miditempo":true,
    "min":true, "minabs":true, "minabsaccum":true, "minaccum":true,
    "mirror":true, "MixerClear":true, "MixerGetLevel":true,
    "MixerReceive":true, "MixerSend":true, "MixerSetLevel":true,
    "mode":true, "monitor":true, "moog":true, "moogladder":true,
    "moogvcf":true, "moogvcf2":true, "moscil":true, "mpulse":true,
    "mrtmsg":true, "multitap":true, "mxadsr":true, "nestedap":true,
    "nlfilt":true, "noise":true, "noteoff":true, "noteon":true,
    "noteondur":true, "noteondur2":true, "notnum":true, "nreverb":true,
    "nrpn":true, "nstrnum":true, "ntrpol":true, "octmidi":true,
    "octmidib":true, "oscbnk":true, "oscil":true, "oscil1":true,
    "oscil1i":true, "oscil3":true, "oscili":true, "oscilikt":true,
    "osciliktp":true, "oscilikts":true, "osciln":true, "oscils":true,
    "oscilv":true, "oscilx":true, "OSCinit":true, "OSClisten":true,
    "OSCrecv":true, "OSCsend":true, "out":true, "out32":true, "outc":true,
    "outch":true, "outh":true, "outiat":true, "outic":true, "outic14":true,
    "outipat":true, "outipb":true, "outipc":true, "outk":true, "outkat":true,
    "outkc":true, "outkc14":true, "outkpat":true, "outkpb":true,
    "outkpc":true, "outo":true, "outq":true, "outq1":true, "outq2":true,
    "outq3":true, "outq4":true, "outrg":true, "outs":true, "outs1":true,
    "outs2":true, "outvalue":true, "outx":true, "outz":true, "p":true,
    "pan":true, "pan2":true, "pareq":true, "partials":true, "partikkel":true,
    "partikkelsync":true, "pcauchy":true, "pchbend":true, "pchmidi":true,
    "pchmidib":true, "pconvolve":true, "pcount":true, "pdclip":true,
    "pdhalf":true, "pdhalfy":true, "peak":true, "peakk":true, "pgmchn":true,
    "phaser1":true, "phaser2":true, "phasor":true, "phasorbnk":true,
    "pindex":true, "pinkish":true, "pitch":true, "pitchamdf":true,
    "planet":true, "pluck":true, "poisson":true, "polyaft":true,
    "polynomial":true, "pop":true, "pop_f":true, "port":true, "portk":true,
    "poscil":true, "poscil3":true, "pow":true, "powershape":true,
    "prepiano":true, "print":true, "printf":true, "printf_i":true,
    "printk":true, "printk2":true, "printks":true, "prints":true,
    "product":true, "ptrack":true, "push":true, "push_f":true, "puts":true,
    "pvadd":true, "pvbufread":true, "pvcross":true, "pvinterp":true,
    "pvoc":true, "pvread":true, "pvsadsyn":true, "pvsanal":true,
    "pvsarp":true, "pvsbandp":true, "pvsbandr":true, "pvsbin":true,
    "pvsblur":true, "pvsbuffer":true, "pvsbufread":true, "pvscale":true,
    "pvscent":true, "pvscross":true, "pvsdemix":true, "pvsdiskin":true,
    "pvsdisp":true, "pvsfilter":true, "pvsfread":true, "pvsfreeze":true,
    "pvsftr":true, "pvsftw":true, "pvsfwrite":true, "pvshift":true,
    "pvsifd":true, "pvsin":true, "pvsinfo":true, "pvsinit":true,
    "pvsmaska":true, "pvsmix":true, "pvsmooth":true, "pvsmorph":true,
    "pvsosc":true, "pvsout":true, "pvspitch":true, "pvstencil":true,
    "pvsvoc":true, "pvsynth":true, "pyassign":true, "pyassigni":true,
    "pylassign":true, "pylassigni":true, "pyassignt":true, "pylassignt":true,
    "pycall":true, "pycall1":true, "pycall2":true, "pycall3":true,
    "pycall4":true, "pycall5":true, "pycall6":true, "pycall7":true,
    "pycall8":true, "pycalli":true, "pycall1i":true, "pycall2i":true,
    "pycall3i":true, "pycall4i":true, "pycall5i":true, "pycall6i":true,
    "pycall7i":true, "pycall8i":true, "pycallt":true, "pycall1t":true,
    "pycall2t":true, "pycall3t":true, "pycall4t":true, "pycall5t":true,
    "pycall6t":true, "pycall7t":true, "pycall8t":true, "pylcall":true,
    "pylcall1":true, "pylcall2":true, "pylcall3":true, "pylcall4":true,
    "pylcall5":true, "pylcall6":true, "pylcall7":true, "pylcall8":true,
    "pylcalli":true, "pylcall1i":true, "pylcall2i":true, "pylcall3i":true,
    "pylcall4i":true, "pylcall5i":true, "pylcall6i":true, "pylcall7i":true,
    "pylcall8i":true, "pylcallt":true, "pylcall1t":true, "pylcall2t":true,
    "pylcall3t":true, "pylcall4t":true, "pylcall5t":true, "pylcall6t":true,
    "pylcall7t":true, "pylcall8t":true, "pycalln":true, "pycallni":true,
    "pylcalln":true, "pylcallni":true, "pyeval":true, "pyevali":true,
    "pyleval":true, "pylevali":true, "pyevalt":true, "pylevalt":true,
    "pyexec":true, "pyexeci":true, "pylexec":true, "pylexeci":true,
    "pyexect":true, "pylexect":true, "pyinit":true, "pyrun":true,
    "pyruni":true, "pylrun":true, "pylruni":true, "pyrunt":true,
    "pylrunt":true, "rand":true, "randh":true, "randi":true, "random":true,
    "randomh":true, "randomi":true, "rbjeq":true, "readclock":true,
    "readk":true, "readk2":true, "readk3":true, "readk4":true, "release":true,
    "repluck":true, "reson":true, "resonk":true, "resonr":true, "resonx":true,
    "resonxk":true, "resony":true, "resonz":true, "resyn":true, "reverb":true,
    "reverb2":true, "reverbsc":true, "rezzy":true, "rfft":true, "rifft":true,
    "rms":true, "rnd31":true, "rspline":true, "rtclock":true, "s16b14":true,
    "s32b14":true, "samphold":true, "sandpaper":true, "scale":true,
    "scanhammer":true, "scans":true, "scantable":true, "scanu":true,
    "schedkwhen":true, "schedkwhennamed":true, "schedule":true,
    "schedwhen":true, "scoreline":true, "scoreline_i":true, "sekere":true,
    "sense":true, "sensekey":true, "seqtime":true, "seqtime2":true,
    "setctrl":true, "setrow":true, "sfilist":true, "sfinstr":true,
    "sfinstr3":true, "sfinstr3m":true, "sfinstrm":true, "sfload":true,
    "sfpassign":true, "sfplay":true, "sfplay3":true, "sfplay3m":true,
    "sfplaym":true, "sfplist":true, "sfpreset":true, "shaker":true,
    "shiftin":true, "shiftout":true, "sinsyn":true, "sleighbells":true,
    "slider16":true, "slider16f":true, "slider16table":true,
    "slider16tablef":true, "slider32":true, "slider32f":true,
    "slider32table":true, "slider32tablef":true, "slider64":true,
    "slider64f":true, "slider64table":true, "slider64tablef":true,
    "slider8":true, "slider8f":true, "slider8table":true,
    "slider8tablef":true, "sliderKawai":true, "sndload":true, "sndloop":true,
    "sndwarp":true, "sndwarpst":true, "sockrecv":true, "sockrecvs":true,
    "socksend":true, "socksends":true, "soundin":true, "soundout":true,
    "soundouts":true, "space":true, "spat3d":true, "spat3di":true,
    "spat3dt":true, "spdist":true, "specaddm":true, "specdiff":true,
    "specdisp":true, "specfilt":true, "spechist":true, "specptrk":true,
    "specscal":true, "specsum":true, "spectrum":true, "splitrig":true,
    "sprintf":true, "sprintfk":true, "spsend":true, "stack":true,
    "statevar":true, "stix":true, "strcat":true, "strcatk":true,
    "strchar":true, "strchark":true, "strcmp":true, "strcmpk":true,
    "strcpy":true, "strcpyk":true, "strecv":true, "streson":true,
    "strget":true, "strindex":true, "strindexk":true, "strlen":true,
    "strlenk":true, "strlower":true, "strlowerk":true, "strrindex":true,
    "strrindexk":true, "strsub":true, "strsubk":true, "strtod":true,
    "strtodk":true, "strtol":true, "strtolk":true, "strupper":true,
    "strupperk":true, "stsend":true, "subinstr":true, "subinstrinit":true,
    "sum":true, "svfilter":true, "syncgrain":true, "syncloop":true,
    "syncphasor":true, "system":true, "system_i":true, "tab":true,
    "tab_i":true, "table":true, "table3":true, "tablecopy":true,
    "tablegpw":true, "tablei":true, "tableicopy":true, "tableigpw":true,
    "tableikt":true, "tableimix":true, "tableiw":true, "tablekt":true,
    "tablemix":true, "tableng":true, "tablera":true, "tableseg":true,
    "tablew":true, "tablewa":true, "tablewkt":true, "tablexkt":true,
    "tablexseg":true, "tabmorph":true, "tabmorpha":true, "tabmorphak":true,
    "tabmorphi":true, "tabplay":true, "tabrec":true, "tabw":true,
    "tabw_i":true, "tambourine":true, "taninv2":true, "tbvcf":true,
    "tb0":true, "tb0_init":true, "tb1":true, "tb1_init":true, "tb2":true,
    "tb2_init":true, "tb3":true, "tb3_init":true, "tb4":true, "tb4_init":true,
    "tb5":true, "tb5_init":true, "tb6":true, "tb6_init":true, "tb7":true,
    "tb7_init":true, "tb8":true, "tb8_init":true, "tb9":true, "tb9_init":true,
    "tb10":true, "tb10_init":true, "tb11":true, "tb11_init":true, "tb12":true,
    "tb12_init":true, "tb13":true, "tb13_init":true, "tb14":true,
    "tb14_init":true, "tb15":true, "tb15_init":true, "tempest":true,
    "tempo":true, "tempoval":true, "timedseq":true, "timeinstk":true,
    "timeinsts":true, "timek":true, "times":true, "tlineto":true, "tone":true,
    "tonek":true, "tonex":true, "tradsyn":true, "transeg":true,
    "trandom":true, "trcross":true, "trfilter":true, "trhighest":true,
    "trigger":true, "trigseq":true, "trirand":true, "trlowest":true,
    "trmix":true, "trscale":true, "trshift":true, "trsplit":true,
    "unirand":true, "upsamp":true, "urd":true, "vadd":true, "vadd_i":true,
    "vaddv":true, "vaddv_i":true, "vaget":true, "valpass":true, "vaset":true,
    "vbap16":true, "vbap16move":true, "vbap4":true, "vbap4move":true,
    "vbap8":true, "vbap8move":true, "vbaplsinit":true, "vbapz":true,
    "vbapzmove":true, "vcella":true, "vco":true, "vco2":true, "vco2ft":true,
    "vco2ift":true, "vco2init":true, "vcomb":true, "vcopy":true,
    "vcopy_i":true, "vdel_k":true, "vdelay":true, "vdelay3":true,
    "vdelayk":true, "vdelayx":true, "vdelayxq":true, "vdelayxs":true,
    "vdelayxw":true, "vdelayxwq":true, "vdelayxws":true, "vdivv":true,
    "vdivv_i":true, "vecdelay":true, "veloc":true, "vexp":true, "vexp_i":true,
    "vexpseg":true, "vexpv":true, "vexpv_i":true, "vibes":true, "vibr":true,
    "vibrato":true, "vincr":true, "vlimit":true, "vlinseg":true,
    "vlowres":true, "vmap":true, "vmirror":true, "vmult":true,
    "vmult_i":true, "vmultv":true, "vmultv_i":true, "voice":true,
    "vphaseseg":true, "vport":true, "vpow":true, "vpow_i":true,
    "vpowv":true, "vpowv_i":true, "vpvoc":true, "vrandh":true,
    "vrandi":true, "vstaudio":true, "vstaudiog":true, "vstbankload":true,
    "vstbanksave":true, "vstedit":true, "vstinfo":true, "vstinit":true,
    "vstmidiout":true, "vstnote":true, "vstnoteondur":true,
    "vstparamget":true, "vstparamset":true, "vstprogset":true,
    "vsttempo":true, "vsubv":true, "vsubv_i":true, "vtaba":true, "vtabi":true,
    "vtabk":true, "vtable1k":true, "vtablea":true, "vtablei":true,
    "vtablek":true, "vtablewa":true, "vtablewi":true, "vtablewk":true,
    "vtabwa":true, "vtabwi":true, "vtabwk":true, "vwrap":true, "waveset":true,
    "weibull":true, "wgbow":true, "wgbowedbar":true, "wgbrass":true,
    "wgclar":true, "wgflute":true, "wgpluck":true, "wgpluck2":true,
    "wguide1":true, "wguide2":true, "window":true, "wrap":true,
    "wterrain":true, "xadsr":true, "xin":true, "xout":true, "xscanmap":true,
    "xscansmap":true, "xscans":true, "xscanu":true, "xtratim":true,
    "xyin":true, "zacl":true, "zakinit":true, "zamod":true, "zar":true,
    "zarg":true, "zaw":true, "zawm":true, "zfilter2":true, "zir":true,
    "ziw":true, "ziwm":true, "zkcl":true, "zkmod":true, "zkr":true,
    "zkw":true, "zkwm":true
  };

  var functions = {
    "a":true, "abs":true, "ampdb":true, "ampdbfs":true,
    "birnd":true, "ceil":true, "cent":true, "cos":true, "cosh":true,
    "cosinv":true, "cpsmidinn":true, "cpsoct":true, "cpspch":true, "db":true,
    "dbamp":true, "dbfsamp":true, "exp":true, "floor":true, "frac":true,
    "ftchnls":true, "ftlen":true, "ftlptim":true, "ftsr":true, "i":true,
    "int":true, "k":true, "log":true, "log10":true, "logbtwo":true,
    "nsamp":true, "octave":true, "octcps":true, "octmidinn":true,
    "octpch":true, "p":true, "pchmidinn":true, "pchoct":true, "powoftwo":true,
    "rnd":true, "round":true, "semitone":true, "sin":true, "sinh":true,
    "sininv":true, "sqrt":true, "tan":true, "tanh":true, "taninv":true
  };

  function tokenBase(stream, state) {
    var ch = stream.next();
    
    if (ch == '"') {
      state.tokenize = tokenString(ch);
      return state.tokenize(stream, state);
    }
    
    if (/#/.test(ch)) {
      stream.match(/[a-z]+/);
      var s = stream.current();
      if (atoms[s]) {
        return "atom";
      }
      return null;
    }
    
    if (/[a-zA-Z]/.test(ch)) {
      stream.match(/[\w\d]*/);
      var s = stream.current();
      if (keywords[s] || functions[s]) {
        return "keyword";
      }
      if (headers[s]) {
        return "header";
      }
      if (blockStatements[s]) {
        return "header";
      }
      if (atoms[s]) {
        return "atom";
      }
      switch (s[0]) {
      case 'i':
      case 'p':
        return "variable";
      case 'k':
        return "variable-2";
      case 'a':
        return "variable-3";
      }
      return "null";
    }
    
    if (/[\d\.]/.test(ch)) {
      if (ch == ".") {
        stream.match(/[0-9]+/);
      }
      else if (ch == '0' && stream.match("dbfs")) {
        return "header";
      }
      else {
        stream.match(/[0-9]*\.?[0-9]*/);
      }
      return "number";
    }
    
    if (ch == ";") {
      stream.skipToEnd();
      return "comment";
    }
    
    if (isOperatorChar.test(ch)) {
      if (ch == "<") {
        if (stream.match(/(Cs|\/Cs)\w+>/)) {
          return "tag";
        }
      }
      stream.eatWhile(isOperatorChar);
      return "operator";
    }
    
    return null;
  }
  
  function tokenString(quote) {
    return function(stream, state) {
      var escaped = false, next, end = false;
      while ((next = stream.next()) != null) {
        if (next == quote && !escaped) {
          end = true;
          break;
        }
        escaped = (!escaped && next == "\\");
      }
      if (end || !escaped) {
        state.tokenize = tokenBase;
      }
      return "string";
    };
  }

  return {
    startState: function(basecolumn) {
      return {
        tokenize: null,
        startOfLine: true
      };
    },
    
    token: function(stream, state) {
      if (stream.eatSpace()) {
        return null;
      }
      var style = tokenBase(stream, state);
      return style;
    },
    
    lineComment: ";"
  };
});

CodeMirror.defineMIME("text/x-csound", {name: "csound", mime: "text/x-csound", mode: "csound", ext: ["csd", "orc", "sco"]});

});
