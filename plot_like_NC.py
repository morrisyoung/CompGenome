import matplotlib.pyplot as plt
n = 200
n_last = 150


if __name__ == '__main__':



	stats = {}
	NC_list = [5000, 6000, 7000, 7500, 8000, 8500, 9000, 9300, 9500, 9600, 9700, 9800, 9900, 9950, 10000, 10050, 10100, 10200, 10300, 10500, 10800, 11000, 11500, 12000, 13000, 14000, 16000, 18000, 20000]


	for NC in NC_list:


		stats[NC] = {}


		filename = "./data_NC/statistic_NC" + str(NC) + ".ibd"
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
			stats[NC][i] = fraction




	##==== prepare to draw the likelihood curve, for NC = 10000 ====
	x = []
	y = []
	for NC in NC_list:
		x.append(NC)

		distance = 0
		i = 5
		while i < n_last:
			distance += (stats[10000][i] - stats[NC][i]) * (stats[10000][i] - stats[NC][i])
			i += 5
		y.append(distance)


	##==== actually draw the figure ====
	plt.figure()
	#plt.plot(x, y, "*-",label="$N=10000$", color="blue")
	plt.plot(x, y, "*-", color="blue")
	plt.plot([10000], [0], "o", color="red", label="true NC")


	plt.xlabel("NC")
	plt.ylabel("Squared Distance Summation")
	plt.title("Distance Curve for $NC_{real}$ = 10000")
	#plt.ylim(0, 1)
	#plt.xlim(0, 200)
	plt.legend(loc=1)
	plt.grid('on')
	plt.show()
