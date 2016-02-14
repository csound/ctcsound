<CsoundSynthesizer>

<CsOptions>
  -d -o dac -m0
</CsOptions>

<CsInstruments>
sr     = 48000
ksmps  = 2000
nchnls = 2
0dbfs  = 1

ifn       vco2init  31

          instr 1
idur      =         p3
iamp      =         p4
icps      =         p5
imode     =         p6
ipw       =         p7
iatt      =         p8
idec      =         p9
islev     =         p10
irel      =         p11
idel      =         p12
ifco      =         p13
ires      =         p14

kenv      adsr      iatt, idec, islev, irel, idel
a1        vco2      iamp, icps, imode, ipw
a2        rezzy     a1, ifco, ires
          outs      a2*kenv, a2*kenv
          endin
</CsInstruments>

<CsScore>
i 1 0 1 0.7 220 10 0 0.1 0.2 0.75 0.3 0 2000 10
e
</CsScore>
</CsoundSynthesizer>
