<CsoundSynthesizer>

<CsOptions>
  -d -o dac -i adc -m0
</CsOptions>

<CsInstruments>
sr     = 1024
ksmps  = 128
nchnls = 1
0dbfs  = 1

          instr 10
idur      =         p3

a1        in
          out       a1/3.0
          endin
</CsInstruments>

<CsScore>
i 10 0 1
e
</CsScore>
</CsoundSynthesizer>
