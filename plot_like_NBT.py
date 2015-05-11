from mpl_toolkits.mplot3d.axes3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from matplotlib import cm
import numpy as np
from mpl_toolkits.mplot3d.axes3d import get_test_data

n = 200
n_last = 150


if __name__ == '__main__':

	#---- get the raw data from data file
	stats = {}

	NB_list = [130, 150, 165, 180, 190, 195, 200, 205, 210, 220, 235, 250, 280]
	T_list = [1, 3, 5, 7, 8, 9, 10, 11, 12, 13, 15, 17, 19]


	for NB in NB_list:

		stats[NB] = {}

		for T in T_list:

			stats[NB][T] = {}

			filename = "./data_NBT/statistic_NB" + str(NB) + "T" + str(T) + ".ibd"
			file = open(filename, "r")

			count = 0
			while 1:
				line = file.readline()
				if not line:
					break

				count += 1
				if count == 1:
					continue

				line = (line.strip()).split(" ")
				i = int(line[0])
				fraction = float(line[1])
				stats[NB][T][i] = fraction


	## get the distance matrix, for NB = 200, and T = 10
	data = {}
	for NB in NB_list:

		data[NB] = {}

		for T in T_list:

			distance = 0
			i = 5
			while i < n_last:
				distance += (stats[200][10][i] - stats[NB][T][i]) * (stats[200][10][i] - stats[NB][T][i])
				i += 5
			data[NB][T] = distance






	##=================== fig1 =======================
	# Twice as wide as it is tall.
	fig = plt.figure(figsize=plt.figaspect(0.5))

	#---- First subplot (the colored likelihood surface)
	ax = fig.add_subplot(1, 2, 1, projection='3d')

	x = np.array(NB_list)
	y = np.array(T_list)

	X, Y = np.meshgrid(x, y)
	z = np.zeros((len(y), len(x)))
	for i in range(len(z)):
		for j in range(len(z[i])):
			z[i][j] = data[x[j]][y[i]]
	Z = np.array(z)
	#print Z

	surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm,
		linewidth=0, antialiased=False)
	#ax.set_zlim3d(-1.01, 1.01)

	#ax.zaxis.set_major_locator(LinearLocator(10))
	#ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

	ax.set_xlabel('NB')
	ax.set_xlim(100, 300)
	ax.set_ylabel('T')
	ax.set_ylim(0, 20)
	ax.set_zlabel('distance')
	#ax.set_zlim(116500, 119000)
	ax.set_title('$NB_{real}$=200, $T_{real}$=10, average: 1000')

	fig.colorbar(surf, shrink=0.5, aspect=10)


	#---- Second subplot
	ax = fig.add_subplot(1, 2, 2, projection='3d')
	#X, Y, Z = axes3d.get_test_data(0.05)
	# we can succeed from the above X, Y and Z
	ax.plot_surface(X, Y, Z, rstride=4, cstride=8, alpha=0.25)
	cset = ax.contour(X, Y, Z, zdir='z', offset=0, cmap=cm.coolwarm)
	cset = ax.contour(X, Y, Z, zdir='x', offset=100, cmap=cm.coolwarm)
	cset = ax.contour(X, Y, Z, zdir='y', offset=20, cmap=cm.coolwarm)
	ax.set_xlabel('NB')
	ax.set_xlim(100, 300)
	ax.set_ylabel('T')
	ax.set_ylim(0, 20)
	ax.set_zlabel('distance')
	#ax.set_zlim(68500, 71300)
	ax.set_title('$NB_{real}$=200, $T_{real}$=10, average: 1000')

	plt.show()
