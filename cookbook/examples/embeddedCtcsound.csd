<CsoundSynthesizer>
<CsOptions>
  -odac
</CsOptions>
<CsInstruments>

sr     = 48000
ksmps  = 100
nchnls = 2

pyinit ;Start python interpreter

pyruni {{
import ctcsound
import sys

# Get an opaque pointer to the running Csound instance
# and print Python version number
p = _CSOUND_
print("\\n  --> Python version number: {}\\n".format(sys.version_info[0]))
# Create an object called cs from the ctcsound.Csound class
# using the opaque pointer to the Csound instance
cs = ctcsound.Csound(pointer_=p)
}}

instr 1
  ; Use the cs python object
  pyruni {{
print("\\n  --> Sample Rate: {}, Control Rate: {}\\n".format(cs.sr(), cs.kr()))
  }}
endin

</CsInstruments>
<CsScore>
i1 0 1
</CsScore>
</CsoundSynthesizer> 

