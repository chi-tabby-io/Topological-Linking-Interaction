import matplotlib.pyplot as plt
import numpy as np
from numpy.linalg import norm


N = 500
rand_dir_2d = np.zeros(2,)
dirs = np.zeros((N, 2))
for i in np.arange(N):
	phi = np.random.uniform(0, 2*np.pi)
	rand_dir_2d[0] = np.cos(phi)
	rand_dir_2d[1] = np.sin(phi)
	dirs[i] = rand_dir_2d

plt.plot(dirs[:,0], dirs[:,1], 'bo')
plt.show()


