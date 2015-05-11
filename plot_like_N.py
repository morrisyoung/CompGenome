import matplotlib.pyplot as plt
n = 200
n_last = 150


if __name__ == '__main__':



	stats = {}


	for N in range(1000, 11000, 1000):


		stats[N] = {}


		filename = "./data/statistic_N" + str(N) + ".ibd"
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
			stats[N][i] = fraction






	## draw the likelihood curve, for N = 5000
	x = []
	y = []
	for N in range(1000, 11000, 1000):
		x.append(N)

		distance = 0
		i = 5
		while i < n_last:
			distance += (stats[5000][i] - stats[N][i]) * (stats[5000][i] - stats[N][i])
			i += 5
		y.append(distance)




	## actually draw the figure
	plt.figure()
	#plt.plot(x, y, "*-",label="$N=10000$", color="blue")
	plt.plot(x, y, "*-", color="blue")
	plt.plot([5000], [0], "o-", color="red", label="true N")





	plt.xlabel("N")
	plt.ylabel("Squared Distance Summation")
	plt.title("Distance Curve for $N_{real}$ = 5000")
	#plt.ylim(0, 1)
	#plt.xlim(0, 200)
	plt.legend(loc=1)
	plt.grid('on')
	plt.show()

