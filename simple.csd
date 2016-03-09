<CsoundSynthesizer>

<CsOptions>
  -d -o dac -m0
</CsOptions>

<CsInstruments>
sr     = 48000
ksmps  = 100
nchnls = 2
0dbfs  = 1

          instr 1
idur      =         p3
iamp      =         p4
icps      =         cpsoct(p5)
ifn       =         p6
irise     =         p7
idec      =         p8
ipan      =         p9
kenv      linen     iamp, irise, idur, idec
asig      oscili    kenv, icps, ifn
a1, a2    pan2      asig, ipan
          outs      a1, a2
          endin
</CsInstruments>

<CsScore>
f 0 14400
</CsScore>
</CsoundSynthesizer>

