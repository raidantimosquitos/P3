import matplotlib.pyplot as plt
import numpy as np
import wave
import sys

spf = wave.open("test_pitch.wav", "r")
fig, axs = plt.subplots(2)
fig.suptitle("Trama sonora y su autocorrelación")

signal = spf.readframes(-1)
signal = np.fromstring(signal, "Int16")
signal = signal[26200:26680]

if spf.getnchannels() == 2:
    print("The files are stereo, try with mono files")
    sys.exit(0)

axs[0].plot(signal, 'tab:red')

r = []

for k in range(0, len(signal)):
    r.append(0)
    for i in range(0, len(signal)-k-1):
        r[k] = r[k] + np.float(signal[i])*np.float(signal[i+k])
    r[k] = r[k]/len(signal)

axs[1].plot(r, 'tab:blue')

plt.show()