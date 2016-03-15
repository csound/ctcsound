sr     = 48000
ksmps  = 100
nchnls = 2
0dbfs  = 1

          instr 1
idur      =         p3
iamp      =         p4
icps      =         cpspch(p5)
irise     =         p6
idec      =         p7
ipan      =         p8

kenv      linen     iamp, irise, idur, idec
kenv      =         kenv*kenv
asig      poscil    kenv, icps
a1, a2    pan2      asig, ipan
          outs      a1, a2
          endin

