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
    "else":true, "elseif":true, "endif":true, "goto":true, "if":true, "igoto":true,
    "iholf":true, "kgoto":true, "loop_ge":true, "loop_gt":true, "loop_le":true,
    "loop_lt":true, "reinit":true, "rigoto":true, "rireturn":true, "then":true,
    "tigoto":true, "timout":true, "tival":true, "until":true, "do":true,
    "od":true, "while":true, "#define":true, "#include":true, "#undef":true,
    "#ifdef":true, "#ifndef":true, "#else":true, "#end":true
  };
  
  var keywords = {
    "ATSadd":true, "ATSaddnz":true, "ATSbufread":true, "ATScross":true,
    "ATSinfo":true, "ATSinterpread":true, "ATSpartialtap":true, "ATSread":true,
    "ATSreadnz":true, "ATSsinnoi":true, "FLbox":true, "FLbutBank":true,
    "FLbutton":true, "FLcloseButton":true, "FLcolor":true, "FLcolor2":true,
    "FLcount":true, "FLexecButton":true, "FLgetsnap":true, "FLgroup":true,
    "FLgroupEnd":true, "FLgroup_end":true, "FLhide":true, "FLhvsBox":true,
    "FLhvsBoxSetValue":true, "FLjoy":true, "FLkeyIn":true, "FLknob":true,
    "FLlabel":true, "FLloadsnap":true, "FLmouse":true, "FLpack":true,
    "FLpackEnd":true, "FLpack_end":true, "FLpanel":true, "FLpanelEnd":true,
    "FLpanel_end":true, "FLprintk":true, "FLprintk2":true, "FLroller":true,
    "FLrun":true, "FLsavesnap":true, "FLscroll":true, "FLscrollEnd":true,
    "FLscroll_end":true, "FLsetAlign":true, "FLsetBox":true, "FLsetColor":true,
    "FLsetColor2":true, "FLsetFont":true, "FLsetPosition":true, "FLsetSize":true,
    "FLsetSnapGroup":true, "FLsetText":true, "FLsetTextColor":true, "FLsetTextSize":true,
    "FLsetTextType":true, "FLsetVal":true, "FLsetVal_i":true, "FLsetVali":true,
    "FLsetsnap":true, "FLshow":true, "FLslidBnk":true, "FLslidBnk2":true,
    "FLslidBnk2Set":true, "FLslidBnk2Setk":true, "FLslidBnkGetHandle":true, "FLslidBnkSet":true,
    "FLslidBnkSetk":true, "FLslider":true, "FLtabs":true, "FLtabsEnd":true,
    "FLtabs_end":true, "FLtext":true, "FLupdate":true, "FLvalue":true,
    "FLvkeybd":true, "FLvslidBnk":true, "FLvslidBnk2":true, "FLxyin":true,
    "JackoAudioIn":true, "JackoAudioInConnect":true, "JackoAudioOut":true, "JackoAudioOutConnect":true,
    "JackoFreewheel":true, "JackoInfo":true, "JackoInit":true, "JackoMidiInConnect":true,
    "JackoMidiOut":true, "JackoMidiOutConnect":true, "JackoNoteOut":true, "JackoOn":true,
    "JackoTransport":true, "K35_hpf":true, "K35_lpf":true, "MixerClear":true,
    "MixerGetLevel":true, "MixerReceive":true, "MixerSend":true, "MixerSetLevel":true,
    "MixerSetLevel_i":true, "OSCinit":true, "OSCinitM":true, "OSClisten":true,
    "OSCraw":true, "OSCsend":true, "OSCsendA":true, "OSCsend_lo":true,
    "S":true, "STKBandedWG":true, "STKBeeThree":true, "STKBlowBotl":true,
    "STKBlowHole":true, "STKBowed":true, "STKBrass":true, "STKClarinet":true,
    "STKDrummer":true, "STKFMVoices":true, "STKFlute":true, "STKHevyMetl":true,
    "STKMandolin":true, "STKModalBar":true, "STKMoog":true, "STKPercFlut":true,
    "STKPlucked":true, "STKResonate":true, "STKRhodey":true, "STKSaxofony":true,
    "STKShakers":true, "STKSimple":true, "STKSitar":true, "STKStifKarp":true,
    "STKTubeBell":true, "STKVoicForm":true, "STKWhistle":true, "STKWurley":true,
    "a":true, "abs":true, "active":true, "adsr":true,
    "adsyn":true, "adsynt":true, "adsynt2":true, "aftouch":true,
    "alpass":true, "alwayson":true, "ampdb":true, "ampdbfs":true,
    "ampmidi":true, "ampmidid":true, "areson":true, "aresonk":true,
    "atone":true, "atonek":true, "atonex":true, "babo":true,
    "balance":true, "bamboo":true, "barmodel":true, "bbcutm":true,
    "bbcuts":true, "betarand":true, "bexprnd":true, "bformdec1":true,
    "bformenc1":true, "binit":true, "biquad":true, "biquada":true,
    "birnd":true, "bpf":true, "bqrez":true, "buchla":true,
    "butbp":true, "butbr":true, "buthp":true, "butlp":true,
    "butterbp":true, "butterbr":true, "butterhp":true, "butterlp":true,
    "button":true, "buzz":true, "c2r":true, "cabasa":true,
    "cauchy":true, "cauchyi":true, "cbrt":true, "ceil":true,
    "cell":true, "cent":true, "centroid":true, "ceps":true,
    "cepsinv":true, "cggoto":true, "chanctrl":true, "changed":true,
    "changed2":true, "chani":true, "chano":true, "chebyshevpoly":true,
    "checkbox":true, "chn_S":true, "chn_a":true, "chn_k":true,
    "chnclear":true, "chnexport":true, "chnget":true, "chnmix":true,
    "chnparams":true, "chnset":true, "chuap":true, "cigoto":true,
    "cingoto":true, "ckgoto":true, "clear":true, "clfilt":true,
    "clip":true, "clockoff":true, "clockon":true, "cmp":true,
    "cmplxprod":true, "cngoto":true, "cnkgoto":true, "comb":true,
    "combinv":true, "compilecsd":true, "compileorc":true, "compilestr":true,
    "compress":true, "compress2":true, "connect":true, "control":true,
    "convle":true, "convolve":true, "copya2ftab":true, "copyf2array":true,
    "cos":true, "cosh":true, "cosinv":true, "cosseg":true,
    "cossegb":true, "cossegr":true, "cps2pch":true, "cpsmidi":true,
    "cpsmidib":true, "cpsmidinn":true, "cpsoct":true, "cpspch":true,
    "cpstmid":true, "cpstun":true, "cpstuni":true, "cpsxpch":true,
    "cpumeter":true, "cpuprc":true, "cross2":true, "crossfm":true,
    "crossfmi":true, "crossfmpm":true, "crossfmpmi":true, "crosspm":true,
    "crosspmi":true, "crunch":true, "ctlchn":true, "ctrl14":true,
    "ctrl21":true, "ctrl7":true, "ctrlinit":true, "cuserrnd":true,
    "dam":true, "date":true, "dates":true, "db":true,
    "dbamp":true, "dbfsamp":true, "dcblock":true, "dcblock2":true,
    "dconv":true, "dct":true, "dctinv":true, "delay":true,
    "delay1":true, "delayk":true, "delayr":true, "delayw":true,
    "deltap":true, "deltap3":true, "deltapi":true, "deltapn":true,
    "deltapx":true, "deltapxw":true, "denorm":true, "diff":true,
    "diode_ladder":true, "directory":true, "diskgrain":true, "diskin":true,
    "diskin2":true, "dispfft":true, "display":true, "distort":true,
    "distort1":true, "divz":true, "doppler":true, "dot":true,
    "downsamp":true, "dripwater":true, "dssiactivate":true, "dssiaudio":true,
    "dssictls":true, "dssiinit":true, "dssilist":true, "dumpk":true,
    "dumpk2":true, "dumpk3":true, "dumpk4":true, "duserrnd":true,
    "dust":true, "dust2":true, "endin":true, "endop":true,
    "envlpx":true, "envlpxr":true, "ephasor":true, "eqfil":true,
    "evalstr":true, "event":true, "event_i":true, "exciter":true,
    "exitnow":true, "exp":true, "expcurve":true, "expon":true,
    "exprand":true, "exprandi":true, "expseg":true, "expsega":true,
    "expsegb":true, "expsegba":true, "expsegr":true, "fareylen":true,
    "fareyleni":true, "fft":true, "fftinv":true, "ficlose":true,
    "filebit":true, "filelen":true, "filenchnls":true, "filepeak":true,
    "filescal":true, "filesr":true, "filevalid":true, "fillarray":true,
    "filter2":true, "fin":true, "fini":true, "fink":true,
    "fiopen":true, "flanger":true, "flashtxt":true, "flooper":true,
    "flooper2":true, "floor":true, "fluidAllOut":true, "fluidCCi":true,
    "fluidCCk":true, "fluidControl":true, "fluidEngine":true, "fluidLoad":true,
    "fluidNote":true, "fluidOut":true, "fluidProgramSelect":true, "fluidSetInterpMethod":true,
    "fmanal":true, "fmax":true, "fmb3":true, "fmbell":true,
    "fmin":true, "fmmetal":true, "fmod":true, "fmpercfl":true,
    "fmrhode":true, "fmvoice":true, "fmwurlie":true, "fof":true,
    "fof2":true, "fofilter":true, "fog":true, "fold":true,
    "follow":true, "follow2":true, "foscil":true, "foscili":true,
    "fout":true, "fouti":true, "foutir":true, "foutk":true,
    "fprintks":true, "fprints":true, "frac":true, "fractalnoise":true,
    "framebuffer":true, "freeverb":true, "ftchnls":true, "ftconv":true,
    "ftcps":true, "ftfree":true, "ftgen":true, "ftgenonce":true,
    "ftgentmp":true, "ftlen":true, "ftload":true, "ftloadk":true,
    "ftlptim":true, "ftmorf":true, "ftom":true, "ftresize":true,
    "ftresizei":true, "ftsamplebank":true, "ftsave":true, "ftsavek":true,
    "ftsr":true, "gain":true, "gainslider":true, "gauss":true,
    "gaussi":true, "gausstrig":true, "gbuzz":true, "genarray":true,
    "genarray_i":true, "gendy":true, "gendyc":true, "gendyx":true,
    "getcfg":true, "getcol":true, "getftargs":true, "getrow":true,
    "getseed":true, "gogobel":true, "goto":true, "grain":true,
    "grain2":true, "grain3":true, "granule":true, "guiro":true,
    "harmon":true, "harmon2":true, "harmon3":true, "harmon4":true,
    "hilbert":true, "hilbert2":true, "hrtfearly":true, "hrtfmove":true,
    "hrtfmove2":true, "hrtfreverb":true, "hrtfstat":true, "hsboscil":true,
    "hvs1":true, "hvs2":true, "hvs3":true, "hypot":true,
    "i":true, "igoto":true, "ihold":true, "imagecreate":true,
    "imagefree":true, "imagegetpixel":true, "imageload":true, "imagesave":true,
    "imagesetpixel":true, "imagesize":true, "in":true, "in32":true,
    "inch":true, "inh":true, "init":true, "initc14":true,
    "initc21":true, "initc7":true, "inleta":true, "inletf":true,
    "inletk":true, "inletkid":true, "inletv":true, "ino":true,
    "inq":true, "inrg":true, "ins":true, "insglobal":true,
    "insremot":true, "instr":true, "int":true, "integ":true,
    "interp":true, "invalue":true, "inx":true, "inz":true,
    "jacktransport":true, "jitter":true, "jitter2":true, "joystick":true,
    "jspline":true, "k":true, "kgoto":true, "la_i_add_mc":true,
    "la_i_add_mr":true, "la_i_add_vc":true, "la_i_add_vr":true, "la_i_assign_mc":true,
    "la_i_assign_mr":true, "la_i_assign_t":true, "la_i_assign_vc":true, "la_i_assign_vr":true,
    "la_i_conjugate_mc":true, "la_i_conjugate_mr":true, "la_i_conjugate_vc":true, "la_i_conjugate_vr":true,
    "la_i_distance_vc":true, "la_i_distance_vr":true, "la_i_divide_mc":true, "la_i_divide_mr":true,
    "la_i_divide_vc":true, "la_i_divide_vr":true, "la_i_dot_mc":true, "la_i_dot_mc_vc":true,
    "la_i_dot_mr":true, "la_i_dot_mr_vr":true, "la_i_dot_vc":true, "la_i_dot_vr":true,
    "la_i_get_mc":true, "la_i_get_mr":true, "la_i_get_vc":true, "la_i_get_vr":true,
    "la_i_invert_mc":true, "la_i_invert_mr":true, "la_i_lower_solve_mc":true, "la_i_lower_solve_mr":true,
    "la_i_lu_det_mc":true, "la_i_lu_det_mr":true, "la_i_lu_factor_mc":true, "la_i_lu_factor_mr":true,
    "la_i_lu_solve_mc":true, "la_i_lu_solve_mr":true, "la_i_mc_create":true, "la_i_mc_set":true,
    "la_i_mr_create":true, "la_i_mr_set":true, "la_i_multiply_mc":true, "la_i_multiply_mr":true,
    "la_i_multiply_vc":true, "la_i_multiply_vr":true, "la_i_norm1_mc":true, "la_i_norm1_mr":true,
    "la_i_norm1_vc":true, "la_i_norm1_vr":true, "la_i_norm_euclid_mc":true, "la_i_norm_euclid_mr":true,
    "la_i_norm_euclid_vc":true, "la_i_norm_euclid_vr":true, "la_i_norm_inf_mc":true, "la_i_norm_inf_mr":true,
    "la_i_norm_inf_vc":true, "la_i_norm_inf_vr":true, "la_i_norm_max_mc":true, "la_i_norm_max_mr":true,
    "la_i_print_mc":true, "la_i_print_mr":true, "la_i_print_vc":true, "la_i_print_vr":true,
    "la_i_qr_eigen_mc":true, "la_i_qr_eigen_mr":true, "la_i_qr_factor_mc":true, "la_i_qr_factor_mr":true,
    "la_i_qr_sym_eigen_mc":true, "la_i_qr_sym_eigen_mr":true, "la_i_random_mc":true, "la_i_random_mr":true,
    "la_i_random_vc":true, "la_i_random_vr":true, "la_i_size_mc":true, "la_i_size_mr":true,
    "la_i_size_vc":true, "la_i_size_vr":true, "la_i_subtract_mc":true, "la_i_subtract_mr":true,
    "la_i_subtract_vc":true, "la_i_subtract_vr":true, "la_i_t_assign":true, "la_i_trace_mc":true,
    "la_i_trace_mr":true, "la_i_transpose_mc":true, "la_i_transpose_mr":true, "la_i_upper_solve_mc":true,
    "la_i_upper_solve_mr":true, "la_i_vc_create":true, "la_i_vc_set":true, "la_i_vr_create":true,
    "la_i_vr_set":true, "la_k_a_assign":true, "la_k_add_mc":true, "la_k_add_mr":true,
    "la_k_add_vc":true, "la_k_add_vr":true, "la_k_assign_a":true, "la_k_assign_f":true,
    "la_k_assign_mc":true, "la_k_assign_mr":true, "la_k_assign_t":true, "la_k_assign_vc":true,
    "la_k_assign_vr":true, "la_k_conjugate_mc":true, "la_k_conjugate_mr":true, "la_k_conjugate_vc":true,
    "la_k_conjugate_vr":true, "la_k_current_f":true, "la_k_current_vr":true, "la_k_distance_vc":true,
    "la_k_distance_vr":true, "la_k_divide_mc":true, "la_k_divide_mr":true, "la_k_divide_vc":true,
    "la_k_divide_vr":true, "la_k_dot_mc":true, "la_k_dot_mc_vc":true, "la_k_dot_mr":true,
    "la_k_dot_mr_vr":true, "la_k_dot_vc":true, "la_k_dot_vr":true, "la_k_f_assign":true,
    "la_k_get_mc":true, "la_k_get_mr":true, "la_k_get_vc":true, "la_k_get_vr":true,
    "la_k_invert_mc":true, "la_k_invert_mr":true, "la_k_lower_solve_mc":true, "la_k_lower_solve_mr":true,
    "la_k_lu_det_mc":true, "la_k_lu_det_mr":true, "la_k_lu_factor_mc":true, "la_k_lu_factor_mr":true,
    "la_k_lu_solve_mc":true, "la_k_lu_solve_mr":true, "la_k_mc_set":true, "la_k_mr_set":true,
    "la_k_multiply_mc":true, "la_k_multiply_mr":true, "la_k_multiply_vc":true, "la_k_multiply_vr":true,
    "la_k_norm1_mc":true, "la_k_norm1_mr":true, "la_k_norm1_vc":true, "la_k_norm1_vr":true,
    "la_k_norm_euclid_mc":true, "la_k_norm_euclid_mr":true, "la_k_norm_euclid_vc":true, "la_k_norm_euclid_vr":true,
    "la_k_norm_inf_mc":true, "la_k_norm_inf_mr":true, "la_k_norm_inf_vc":true, "la_k_norm_inf_vr":true,
    "la_k_norm_max_mc":true, "la_k_norm_max_mr":true, "la_k_qr_eigen_mc":true, "la_k_qr_eigen_mr":true,
    "la_k_qr_factor_mc":true, "la_k_qr_factor_mr":true, "la_k_qr_sym_eigen_mc":true, "la_k_qr_sym_eigen_mr":true,
    "la_k_random_mc":true, "la_k_random_mr":true, "la_k_random_vc":true, "la_k_random_vr":true,
    "la_k_subtract_mc":true, "la_k_subtract_mr":true, "la_k_subtract_vc":true, "la_k_subtract_vr":true,
    "la_k_t_assign":true, "la_k_trace_mc":true, "la_k_trace_mr":true, "la_k_upper_solve_mc":true,
    "la_k_upper_solve_mr":true, "la_k_vc_set":true, "la_k_vr_set":true, "lenarray":true,
    "lfo":true, "limit":true, "limit1":true, "line":true,
    "linen":true, "linenr":true, "lineto":true, "linlin":true,
    "linrand":true, "linseg":true, "linsegb":true, "linsegr":true,
    "liveconv":true, "locsend":true, "locsig":true, "log":true,
    "log10":true, "log2":true, "logbtwo":true, "logcurve":true,
    "loop_ge":true, "loop_gt":true, "loop_le":true, "loop_lt":true,
    "loopseg":true, "loopsegp":true, "looptseg":true, "loopxseg":true,
    "lorenz":true, "loscil":true, "loscil3":true, "loscilx":true,
    "lowpass2":true, "lowres":true, "lowresx":true, "lpf18":true,
    "lpform":true, "lpfreson":true, "lphasor":true, "lpinterp":true,
    "lposcil":true, "lposcil3":true, "lposcila":true, "lposcilsa":true,
    "lposcilsa2":true, "lpread":true, "lpreson":true, "lpshold":true,
    "lpsholdp":true, "lpslot":true, "lua_exec":true, "lua_iaopcall":true,
    "lua_iaopcall_off":true, "lua_ikopcall":true, "lua_ikopcall_off":true, "lua_iopcall":true,
    "lua_iopcall_off":true, "lua_opdef":true, "mac":true, "maca":true,
    "madsr":true, "mags":true, "mandel":true, "mandol":true,
    "maparray":true, "maparray_i":true, "marimba":true, "massign":true,
    "max":true, "max_k":true, "maxabs":true, "maxabsaccum":true,
    "maxaccum":true, "maxalloc":true, "maxarray":true, "mclock":true,
    "mdelay":true, "median":true, "mediank":true, "metro":true,
    "mfb":true, "midglobal":true, "midiarp":true, "midic14":true,
    "midic21":true, "midic7":true, "midichannelaftertouch":true, "midichn":true,
    "midicontrolchange":true, "midictrl":true, "mididefault":true, "midifilestatus":true,
    "midiin":true, "midinoteoff":true, "midinoteoncps":true, "midinoteonkey":true,
    "midinoteonoct":true, "midinoteonpch":true, "midion":true, "midion2":true,
    "midiout":true, "midipgm":true, "midipitchbend":true, "midipolyaftertouch":true,
    "midiprogramchange":true, "miditempo":true, "midremot":true, "min":true,
    "minabs":true, "minabsaccum":true, "minaccum":true, "minarray":true,
    "mincer":true, "mirror":true, "mode":true, "modmatrix":true,
    "monitor":true, "moog":true, "moogladder":true, "moogladder2":true,
    "moogvcf":true, "moogvcf2":true, "moscil":true, "mp3bitrate":true,
    "mp3in":true, "mp3len":true, "mp3nchnls":true, "mp3scal":true,
    "mp3sr":true, "mpulse":true, "mrtmsg":true, "mtof":true,
    "mton":true, "multitap":true, "mute":true, "mvchpf":true,
    "mvclpf1":true, "mvclpf2":true, "mvclpf3":true, "mvclpf4":true,
    "mxadsr":true, "nchnls_hw":true, "nestedap":true, "nlalp":true,
    "nlfilt":true, "nlfilt2":true, "noise":true, "noteoff":true,
    "noteon":true, "noteondur":true, "noteondur2":true, "notnum":true,
    "nreverb":true, "nrpn":true, "nsamp":true, "nstance":true,
    "nstrnum":true, "ntom":true, "ntrpol":true, "nxtpow2":true,
    "octave":true, "octcps":true, "octmidi":true, "octmidib":true,
    "octmidinn":true, "octpch":true, "olabuffer":true, "opcode":true,
    "oscbnk":true, "oscil":true, "oscil1":true, "oscil1i":true,
    "oscil3":true, "oscili":true, "oscilikt":true, "osciliktp":true,
    "oscilikts":true, "osciln":true, "oscils":true, "oscilx":true,
    "out":true, "out32":true, "outc":true, "outch":true,
    "outh":true, "outiat":true, "outic":true, "outic14":true,
    "outipat":true, "outipb":true, "outipc":true, "outkat":true,
    "outkc":true, "outkc14":true, "outkpat":true, "outkpb":true,
    "outkpc":true, "outleta":true, "outletf":true, "outletk":true,
    "outletkid":true, "outletv":true, "outo":true, "outq":true,
    "outq1":true, "outq2":true, "outq3":true, "outq4":true,
    "outrg":true, "outs":true, "outs1":true, "outs2":true,
    "outvalue":true, "outx":true, "outz":true, "p":true,
    "pan":true, "pan2":true, "pareq":true, "part2txt":true,
    "partials":true, "partikkel":true, "partikkelget":true, "partikkelset":true,
    "partikkelsync":true, "passign":true, "paulstretch":true, "pcauchy":true,
    "pchbend":true, "pchmidi":true, "pchmidib":true, "pchmidinn":true,
    "pchoct":true, "pchtom":true, "pconvolve":true, "pcount":true,
    "pdclip":true, "pdhalf":true, "pdhalfy":true, "peak":true,
    "pgmassign":true, "pgmchn":true, "phaser1":true, "phaser2":true,
    "phasor":true, "phasorbnk":true, "phs":true, "pindex":true,
    "pinker":true, "pinkish":true, "pitch":true, "pitchac":true,
    "pitchamdf":true, "planet":true, "platerev":true, "plltrack":true,
    "pluck":true, "poisson":true, "pol2rect":true, "polyaft":true,
    "polynomial":true, "port":true, "portk":true, "poscil":true,
    "poscil3":true, "pow":true, "powershape":true, "powoftwo":true,
    "pows":true, "prealloc":true, "prepiano":true, "print":true,
    "print_type":true, "printf":true, "printf_i":true, "printk":true,
    "printk2":true, "printks":true, "printks2":true, "prints":true,
    "product":true, "pset":true, "ptable":true, "ptable3":true,
    "ptablei":true, "ptableiw":true, "ptablew":true, "ptrack":true,
    "puts":true, "pvadd":true, "pvbufread":true, "pvcross":true,
    "pvinterp":true, "pvoc":true, "pvread":true, "pvs2array":true,
    "pvs2tab":true, "pvsadsyn":true, "pvsanal":true, "pvsarp":true,
    "pvsbandp":true, "pvsbandr":true, "pvsbin":true, "pvsblur":true,
    "pvsbuffer":true, "pvsbufread":true, "pvsbufread2":true, "pvscale":true,
    "pvscent":true, "pvsceps":true, "pvscross":true, "pvsdemix":true,
    "pvsdiskin":true, "pvsdisp":true, "pvsenvftw":true, "pvsfilter":true,
    "pvsfread":true, "pvsfreeze":true, "pvsfromarray":true, "pvsftr":true,
    "pvsftw":true, "pvsfwrite":true, "pvsgain":true, "pvsgendy":true,
    "pvshift":true, "pvsifd":true, "pvsin":true, "pvsinfo":true,
    "pvsinit":true, "pvslock":true, "pvsmaska":true, "pvsmix":true,
    "pvsmooth":true, "pvsmorph":true, "pvsosc":true, "pvsout":true,
    "pvspitch":true, "pvstanal":true, "pvstencil":true, "pvstrace":true,
    "pvsvoc":true, "pvswarp":true, "pvsynth":true, "pwd":true,
    "pyassign":true, "pyassigni":true, "pyassignt":true, "pycall":true,
    "pycall1":true, "pycall1i":true, "pycall1t":true, "pycall2":true,
    "pycall2i":true, "pycall2t":true, "pycall3":true, "pycall3i":true,
    "pycall3t":true, "pycall4":true, "pycall4i":true, "pycall4t":true,
    "pycall5":true, "pycall5i":true, "pycall5t":true, "pycall6":true,
    "pycall6i":true, "pycall6t":true, "pycall7":true, "pycall7i":true,
    "pycall7t":true, "pycall8":true, "pycall8i":true, "pycall8t":true,
    "pycalli":true, "pycalln":true, "pycallni":true, "pycallt":true,
    "pyeval":true, "pyevali":true, "pyevalt":true, "pyexec":true,
    "pyexeci":true, "pyexect":true, "pyinit":true, "pylassign":true,
    "pylassigni":true, "pylassignt":true, "pylcall":true, "pylcall1":true,
    "pylcall1i":true, "pylcall1t":true, "pylcall2":true, "pylcall2i":true,
    "pylcall2t":true, "pylcall3":true, "pylcall3i":true, "pylcall3t":true,
    "pylcall4":true, "pylcall4i":true, "pylcall4t":true, "pylcall5":true,
    "pylcall5i":true, "pylcall5t":true, "pylcall6":true, "pylcall6i":true,
    "pylcall6t":true, "pylcall7":true, "pylcall7i":true, "pylcall7t":true,
    "pylcall8":true, "pylcall8i":true, "pylcall8t":true, "pylcalli":true,
    "pylcalln":true, "pylcallni":true, "pylcallt":true, "pyleval":true,
    "pylevali":true, "pylevalt":true, "pylexec":true, "pylexeci":true,
    "pylexect":true, "pylrun":true, "pylruni":true, "pylrunt":true,
    "pyrun":true, "pyruni":true, "pyrunt":true, "qinf":true,
    "qnan":true, "r2c":true, "rand":true, "randh":true,
    "randi":true, "random":true, "randomh":true, "randomi":true,
    "rbjeq":true, "readclock":true, "readf":true, "readfi":true,
    "readk":true, "readk2":true, "readk3":true, "readk4":true,
    "readks":true, "readscore":true, "readscratch":true, "rect2pol":true,
    "reinit":true, "release":true, "remoteport":true, "remove":true,
    "repluck":true, "reson":true, "resonk":true, "resonr":true,
    "resonx":true, "resonxk":true, "resony":true, "resonz":true,
    "resyn":true, "return":true, "reverb":true, "reverb2":true,
    "reverbsc":true, "rewindscore":true, "rezzy":true, "rfft":true,
    "rifft":true, "rigoto":true, "rireturn":true, "rms":true,
    "rnd":true, "rnd31":true, "round":true, "rspline":true,
    "rtclock":true, "s16b14":true, "s32b14":true, "samphold":true,
    "sandpaper":true, "sc_lag":true, "sc_lagud":true, "sc_phasor":true,
    "sc_trig":true, "scale":true, "scalearray":true, "scanhammer":true,
    "scans":true, "scantable":true, "scanu":true, "schedkwhen":true,
    "schedkwhennamed":true, "schedule":true, "schedwhen":true, "scoreline":true,
    "scoreline_i":true, "seed":true, "sekere":true, "select":true,
    "semitone":true, "sense":true, "sensekey":true, "seqtime":true,
    "seqtime2":true, "serialBegin":true, "serialEnd":true, "serialFlush":true,
    "serialPrint":true, "serialRead":true, "serialWrite":true, "serialWrite_i":true,
    "setcol":true, "setctrl":true, "setksmps":true, "setrow":true,
    "setscorepos":true, "sfilist":true, "sfinstr":true, "sfinstr3":true,
    "sfinstr3m":true, "sfinstrm":true, "sfload":true, "sflooper":true,
    "sfpassign":true, "sfplay":true, "sfplay3":true, "sfplay3m":true,
    "sfplaym":true, "sfplist":true, "sfpreset":true, "shaker":true,
    "shiftin":true, "shiftout":true, "signalflowgraph":true, "signum":true,
    "sin":true, "sinh":true, "sininv":true, "sinsyn":true,
    "sleighbells":true, "slicearray":true, "slider16":true, "slider16f":true,
    "slider16table":true, "slider16tablef":true, "slider32":true, "slider32f":true,
    "slider32table":true, "slider32tablef":true, "slider64":true, "slider64f":true,
    "slider64table":true, "slider64tablef":true, "slider8":true, "slider8f":true,
    "slider8table":true, "slider8tablef":true, "sliderKawai":true, "sndloop":true,
    "sndwarp":true, "sndwarpst":true, "sockrecv":true, "sockrecvs":true,
    "socksend":true, "socksends":true, "sorta":true, "sortd":true,
    "soundin":true, "space":true, "spat3d":true, "spat3di":true,
    "spat3dt":true, "spdist":true, "specaddm":true, "specdiff":true,
    "specdisp":true, "specfilt":true, "spechist":true,  "specptrk":true,
    "specscal":true, "specsum":true, "spectrum":true,
    "splitrig":true, "sprintf":true,
    "sprintfk":true, "spsend":true, "sqrt":true, "statevar":true,
    "stix":true, "strcat":true, "strcatk":true, "strchar":true,
    "strchark":true, "strcmp":true, "strcmpk":true, "strcpy":true,
    "strcpyk":true, "strecv":true, "streson":true, "strget":true,
    "strindex":true, "strindexk":true, "strlen":true, "strlenk":true,
    "strlower":true, "strlowerk":true, "strrindex":true, "strrindexk":true,
    "strset":true, "strsub":true, "strsubk":true, "strtod":true,
    "strtodk":true, "strtol":true, "strtolk":true, "strupper":true,
    "strupperk":true, "stsend":true, "subinstr":true, "subinstrinit":true,
    "sum":true, "sumarray":true, "svfilter":true, "syncgrain":true,
    "syncloop":true, "syncphasor":true, "system":true, "system_i":true,
    "systime":true, "tab":true, "tab2pvs":true, "tab_i":true,
    "tabifd":true, "table":true, "table3":true, "table3kt":true,
    "tablecopy":true, "tablefilter":true, "tablefilteri":true, "tablegpw":true,
    "tablei":true, "tableicopy":true, "tableigpw":true, "tableikt":true,
    "tableimix":true, "tableiw":true, "tablekt":true, "tablemix":true,
    "tableng":true, "tablera":true, "tableseg":true, "tableshuffle":true,
    "tableshufflei":true, "tablew":true, "tablewa":true, "tablewkt":true,
    "tablexkt":true, "tablexseg":true, "tabmorph":true, "tabmorpha":true,
    "tabmorphak":true, "tabmorphi":true, "tabplay":true, "tabrec":true,
    "tabsum":true, "tabw":true, "tabw_i":true, "tambourine":true,
    "tan":true, "tanh":true, "taninv":true, "taninv2":true,
    "tb0":true, "tb0_init":true, "tb1":true, "tb10":true,
    "tb10_init":true, "tb11":true, "tb11_init":true, "tb12":true,
    "tb12_init":true, "tb13":true, "tb13_init":true, "tb14":true,
    "tb14_init":true, "tb15":true, "tb15_init":true, "tb1_init":true,
    "tb2":true, "tb2_init":true, "tb3":true, "tb3_init":true,
    "tb4":true, "tb4_init":true, "tb5":true, "tb5_init":true,
    "tb6":true, "tb6_init":true, "tb7":true, "tb7_init":true,
    "tb8":true, "tb8_init":true, "tb9":true, "tb9_init":true,
    "tbvcf":true, "tempest":true, "tempo":true, "temposcal":true,
    "tempoval":true, "tigoto":true, "timedseq":true, "timeinstk":true,
    "timeinsts":true, "timek":true, "times":true, "timout":true,
    "tival":true, "tlineto":true, "tone":true, "tonek":true,
    "tonex":true, "tradsyn":true, "trandom":true, "transeg":true,
    "transegb":true, "transegr":true, "trcross":true, "trfilter":true,
    "trhighest":true, "trigger":true, "trigseq":true, "trirand":true,
    "trlowest":true, "trmix":true, "trscale":true, "trshift":true,
    "trsplit":true, "turnoff":true, "turnoff2":true, "turnon":true,
    "tvconv":true, "unirand":true, "unwrap":true, "upsamp":true,
    "urandom":true, "urd":true, "vactrol":true, "vadd":true,
    "vadd_i":true, "vaddv":true, "vaddv_i":true, "vaget":true,
    "valpass":true, "vaset":true, "vbap":true,
    "vbap16":true, "vbap16move": true, "vbap4":true, "vbap4move":true,
    "vbap8":true, "vbap8move":true, "vbapg":true,
    "vbapgmove":true, "vbaplsinit":true, "vbapmove":true, "vbapz":true,
    "vbapzmove":true, "vcella":true, "vco":true, "vco2":true,
    "vco2ft":true, "vco2ift":true, "vco2init":true, "vcomb":true,
    "vcopy":true, "vcopy_i":true, "vdel_k":true, "vdelay":true,
    "vdelay3":true, "vdelayk":true, "vdelayx":true, "vdelayxq":true,
    "vdelayxs":true, "vdelayxw":true, "vdelayxwq":true, "vdelayxws":true,
    "vdivv":true, "vdivv_i":true, "vecdelay":true, "veloc":true,
    "vexp":true, "vexp_i":true, "vexpseg":true, "vexpv":true,
    "vexpv_i":true, "vibes":true, "vibr":true, "vibrato":true,
    "vincr":true, "vlimit":true, "vlinseg":true, "vlowres":true,
    "vmap":true, "vmirror":true, "vmult":true, "vmult_i":true,
    "vmultv":true, "vmultv_i":true, "voice":true, "vosim":true,
    "vphaseseg":true, "vport":true, "vpow":true, "vpow_i":true,
    "vpowv":true, "vstaudio":true, "vstaudiog":true, "vstbankload":true,
    "vstbanksave":true, "vstedit":true, "vstinfo":true, "vstinit":true,
    "vstmidiout":true, "vstnote":true, "vstnoteondur":true, "vstparamget":true,
    "vstparamset":true, "vstprogset":true, "vsttempo":true,
    "vpowv_i":true, "vpvoc":true, "vrandh":true,
    "vrandi":true, "vstparamget":true,
    "vstprogset":true,
    "vsubv":true, "vsubv_i":true, "vtaba":true,
    "vtabi":true, "vtabk":true, "vtable1k":true, "vtablea":true,
    "vtablei":true, "vtablek":true, "vtablewa":true, "vtablewi":true,
    "vtablewk":true, "vtabwa":true, "vtabwi":true, "vtabwk":true,
    "vwrap":true, "waveset":true, "websocket":true, "weibull":true,
    "wgbow":true, "wgbowedbar":true, "wgbrass":true, "wgclar":true,
    "wgflute":true, "wgpluck":true, "wgpluck2":true, "wguide1":true,
    "wguide2":true, "window":true, "wrap":true, "writescratch":true,
    "wterrain":true, "xadsr":true, "xin":true, "xout":true,
    "xscanmap":true, "xscans":true, "xscansmap":true, "xscanu":true,
    "xtratim":true, "xyin":true, "xyscale":true, "zacl":true, "zakinit":true,
    "zamod":true, "zar":true, "zarg":true, "zaw":true,
    "zawm":true, "zdf_1pole":true, "zdf_1pole_mode":true, "zdf_2pole":true,
    "zdf_2pole_mode":true, "zdf_ladder":true, "zfilter2":true, "zir":true,
    "ziw":true, "ziwm":true, "zkcl":true, "zkmod":true,
    "zkr":true, "zkw":true, "zkwm":true
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
    
    if (ch == "/") {
      if (stream.eat("*")) {
        state.tokenize = tokenComment;
        return tokenComment(stream, state);
      }
      if (stream.eat("/")) {
        stream.skipToEnd();
        return "comment";
      }
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
  
  function tokenComment(stream, state) {
    var maybeEnd = false, ch;
    while (ch = stream.next()) {
      if (ch == "/" && maybeEnd) {
        state.tokenize = tokenBase;
        break;
      }
      maybeEnd = (ch == "*");
    }
    return "comment";
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
        tokenize: tokenBase,
        startOfLine: true,
      };
    },
    
    token: function(stream, state) {
      if (stream.eatSpace()) {
        return null;
      }
      var style = state.tokenize(stream, state);
      return style;
    },
    
    blockCommentStart: "/*",
    blockCommentEnd: "*/",
    lineComment: ";"
  };
});

CodeMirror.defineMIME("text/x-csound", {name: "csound", mime: "text/x-csound", mode: "csound", ext: ["csd", "orc", "sco"]});

});
