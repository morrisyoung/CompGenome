from mpl_toolkits.mplot3d.axes3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from matplotlib import cm
import numpy as np
from mpl_toolkits.mplot3d.axes3d import get_test_data

n = 200
n_last = 150

#---- get the raw data from data file
stats = {}
TB_list = [25, 27, 28, 29, 30, 31, 32, 33, 35]
T_list = [5, 7, 8, 9, 10, 11, 12, 13, 15]

for T in T_list:

	stats[T] = {}

	for TB in TB_list:

		stats[T][TB] = {}

		filename = "./data_TBT/statistic_TB" + str(TB) + "T" + str(T) + ".ibd"
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
			stats[T][TB][i] = fraction


## get the distance matrix, for T = 10, and TB = 30
data = {}
for T in T_list:

	data[T] = {}

	for TB in TB_list:

		distance = 0
		i = 5
		while i < n_last:
			distance += (stats[10][30][i] - stats[T][TB][i]) * (stats[10][30][i] - stats[T][TB][i])
			i += 5
		data[T][TB] = distance





##=================== fig1 =======================
# Twice as wide as it is tall.
fig = plt.figure(figsize=plt.figaspect(0.5))

#---- First subplot (the colored likelihood surface)
ax = fig.add_subplot(1, 2, 1, projection='3d')

x = np.array(T_list)
#y = np.array([1, 3, 5, 7, 8, 9, 10, 11, 12, 13, 15, 17, 19])
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

ax.set_xlabel('T')
ax.set_xlim(0, 20)
ax.set_ylabel('TB')
ax.set_ylim(20, 40)
ax.set_zlabel('distance')
#ax.set_zlim(75500, 77500)
ax.set_title('$T_{real}$ = 10, $TB_{real}$ = 30')

fig.colorbar(surf, shrink=0.5, aspect=10)


#---- Second subplot
ax = fig.add_subplot(1, 2, 2, projection='3d')
#X, Y, Z = axes3d.get_test_data(0.05)
# we can succeed from the above X, Y and Z
ax.plot_surface(X, Y, Z, rstride=4, cstride=8, alpha=0.25)
cset = ax.contour(X, Y, Z, zdir='z', offset=0, cmap=cm.coolwarm)
cset = ax.contour(X, Y, Z, zdir='x', offset=0, cmap=cm.coolwarm)
cset = ax.contour(X, Y, Z, zdir='y', offset=40, cmap=cm.coolwarm)
ax.set_xlabel('T')
ax.set_xlim(0, 20)
ax.set_ylabel('TB')
ax.set_ylim(20, 40)
ax.set_zlabel('distance')
#ax.set_zlim(75500, 77500)
ax.set_title('$T_{real}$ = 10, $TB_{real}$ = 30')

plt.show()
