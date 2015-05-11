import matplotlib.pyplot as plt
n = 200
n_last = 150


if __name__ == '__main__':



	stats = {}
	TB_list = [20, 23, 25, 27, 28, 29, 30, 31, 32, 33, 35, 37, 40]



	for TB in TB_list:


		stats[TB] = {}


		filename = "./data_TB/statistic_TB" + str(TB) + ".ibd"
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
			stats[TB][i] = fraction






	## draw the likelihood curve, for N = 5000
	x = []
	y = []
	for TB in TB_list:

		x.append(TB)

		distance = 0
		i = 5
		while i < n_last:
			distance += (stats[30][i] - stats[TB][i]) * (stats[30][i] - stats[TB][i])
			i += 5
		y.append(distance)




	## actually draw the figure
	plt.figure()
	#plt.plot(x, y, "*-",label="$N=10000$", color="blue")
	plt.plot(x, y, "*-", color="blue")
	plt.plot([30], [0], "o-", color="red", label="true TB")





	plt.xlabel("TB")
	plt.ylabel("Sum of Squared Distance")
	plt.title("Distance Curve for $TB_{real}$ = 30 (50 * 20 times for averaging)")
	#plt.ylim(0, 1)
	#plt.xlim(0, 200)
	plt.legend(loc=1)
	plt.grid('on')
	plt.show()
