import matplotlib.pyplot as plt
import numpy as np

fig, axs = plt.subplots(2)
fig.suptitle("Pitch calculado y pitch de wavesurfer")

frames, frames_ws = np.loadtxt('pitch_nuestro.txt'), np.loadtxt('pitch_wavesurfer.txt')

axs[0].set_title('Pitch calculado')
axs[0].set_ylim(0,500)
axs[1].set_title('Pitch calculado por wavesurfer')
axs[1].set_ylim(0,500)
axs[0].plot(frames, 'o', color = 'red', markersize = 1)
axs[1].plot(frames_ws, 'o', color = 'blue', markersize = 1)

plt.show()