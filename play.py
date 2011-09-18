import string
import serial
import time
from numpy import *

# Play with VNA
# based on ideas gleaned from user manual at
# http://www.w4rt.com/Misc/miniVNA.htm
# See also
# http://wiki.oz9aec.net/index.php/MiniVNA_ICD


# freqs are in MHz

khz2dds = 10737.4182
dev = '/dev/ttyUSB0'

def pause():
    time.sleep(0.1)

# Following returns 4 bytes for every nstep
# The minivna_bas.htm file from the analyzer_iw3hev yahoo group
# (Software/Atmega8 firmware) says it's adcphase and adcmagnitude
# Observation: phase lies between 0 and 1023!
# Q: are these signed or unsigned ints?

def sweep(f1,f2,nstep):
    df = (f2-f1)*1.0/nstep
    s = serial.Serial(dev,115200,timeout=1)
    s.write("0\r");
    pause()
    s.write("%d\r"%(f1*1e3*khz2dds))
    pause()
    s.write("%d\r"%nstep)
    pause()
    s.write("%d\r"%(df*1e3*khz2dds))
    pause()
    ans = string.join(s.readlines(),'')
    s.close()
    a=fromstring(ans,dtype=uint16)
    phase, mag = a[::2]*pi/1024, a[1::2]
    return f1 + df*arange(0,nstep), mag, phase

# For more, see http://www.rigexpert.com/index?s=articles&f=aas
# According to this, the 'magnitude' is the ratio U(refl)/U(in) 
# and the phase is  |phi(refl)-phi(in)|

