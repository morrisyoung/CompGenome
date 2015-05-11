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

	## T = 20, ratio = 0.05, so NB_{real} = 400
	NB_list = [100, 150, 200, 240, 270, 300, 325, 345, 360, 370, 375, 380, 385, 390, 395, 398, 400, 402, 404, 406, 408, 410, 415, 420, 430, 440, 450, 465, 480, 500, 525, 550, 575, 600]
	TB_list = [20, 23, 25, 27, 28, 29, 30, 31, 32, 33, 35, 37, 40]


	for NB in NB_list:

		stats[NB] = {}

		for TB in TB_list:

			stats[NB][TB] = {}

			filename = "./data_NBTBT20_2/statistic_NB" + str(NB) + "TB" + str(TB) + ".ibd"
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
				stats[NB][TB][i] = fraction


	## get the distance matrix, for NB = 200 and TB = 30 with true T = 10
	## get the reald data first (where NB = 200, TB = 30 and T = 10)
	real_data = {}

	filename = "./data_NBTB/statistic_NB" + str(200) + "TB" + str(30) + ".ibd"
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
		real_data[i] = fraction

	## get the distance statistics
	data = {}
	for NB in NB_list:

		data[NB] = {}

		for TB in TB_list:

			distance = 0
			i = 5
			while i < n_last:
				distance += (real_data[i] - stats[NB][TB][i]) * (real_data[i] - stats[NB][TB][i])
				i += 5
			data[NB][TB] = distance






	##=================== fig1 =======================
	# Twice as wide as it is tall.
	fig = plt.figure(figsize=plt.figaspect(0.5))

	#---- First subplot (the colored likelihood surface)
	ax = fig.add_subplot(1, 2, 1, projection='3d')


	x = np.array(NB_list)
	y = np.array(TB_list)


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
	ax.set_xlim(100, 600)
	ax.set_ylabel('TB')
	ax.set_ylim(20, 40)
	ax.set_zlabel('distance')
	#ax.set_zlim(116500, 119000)  ##TODO set the range according to the actual values
	ax.set_title('$NB_{real}$=200, $TB_{real}$=30, $T_{real}$=10, $T_{biased}$=20, ave=1000')

	fig.colorbar(surf, shrink=0.5, aspect=10)


	#---- Second subplot
	ax = fig.add_subplot(1, 2, 2, projection='3d')
	#X, Y, Z = axes3d.get_test_data(0.05)
	# we can succeed from the above X, Y and Z
	ax.plot_surface(X, Y, Z, rstride=4, cstride=8, alpha=0.25)
	cset = ax.contour(X, Y, Z, zdir='z', offset=0, cmap=cm.coolwarm)
	cset = ax.contour(X, Y, Z, zdir='x', offset=100, cmap=cm.coolwarm)
	cset = ax.contour(X, Y, Z, zdir='y', offset=40, cmap=cm.coolwarm)
	ax.set_xlabel('NB')
	ax.set_xlim(100, 600)
	ax.set_ylabel('TB')
	ax.set_ylim(20, 40)
	ax.set_zlabel('distance')
	#ax.set_zlim(68500, 71300)  ##TODO set the range according to the actual values
	ax.set_title('$NB_{real}$=200, $TB_{real}$=30, $T_{real}$=10, $T_{biased}$=20, ave=1000')

	plt.show()
