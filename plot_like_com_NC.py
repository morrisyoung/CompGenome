import matplotlib.pyplot as plt
n = 200
n_last = 150



def MaxElement(L):
	max_value = L[0]

	for element in L:
		if element > max_value:
			max_value = element

	return max_value


def MeanValue(L):
	mean = 0

	for element in L:
		mean += element

	mean = mean * 1.0 / len(L)

	return mean




if __name__ == '__main__':

	NC_list = [5000, 6000, 7000, 7500, 8000, 8500, 9000, 9300, 9500, 9600, 9700, 9800, 9900, 9950, 10000, 10050, 10100, 10200, 10300, 10500, 10800, 11000, 11500, 12000, 13000, 14000, 16000, 18000, 20000]

	### get two distance curve, and store in x1/y1 and x2/y2
	##================ get cohort-sharing distance curve =================
	stats = {}
	for NC in NC_list:
		stats[NC] = {}

		filename = "./data_com_NC/CohortSharing_NC" + str(NC) + ".ibd"
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
	x1 = []
	y1 = []
	for NC in NC_list:
		x1.append(NC)

		distance = 0
		i = 5
		while i < n_last:
			distance += (stats[10000][i] - stats[NC][i]) * (stats[10000][i] - stats[NC][i])
			i += 5
		y1.append(distance)




	##================ get cohort-sharing distance curve =================
	stats = {}
	for NC in NC_list:
		stats[NC] = {}

		filename = "./data_com_NC/IBDNumber_NC" + str(NC) + ".ibd"
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
			index = int(line[0])
			number = float(line[1])
			stats[NC][index] = number
	x2 = []
	y2 = []
	for NC in NC_list:
		x2.append(NC)

		distance = 0
		for index in stats[NC]:
			distance += (stats[10000][index] - stats[NC][index]) * (stats[10000][index] - stats[NC][index])
		y2.append(distance)





	plt.figure()


	#####################################################################
	plt.subplot(2, 2, 1)
	plt.plot(x1, y1, "*-", color="blue")
	plt.plot([10000], [0], "o", color="red", label="true NC")
	plt.xlabel("NC")
	plt.ylabel("Sum of Squared Distance Between Estimated and Real NC")
	plt.title("Cohort-sharing Distance Curve for $NC_{real}$ = 10000")
	plt.legend()
	plt.grid('on')



	#####################################################################
	plt.subplot(2, 2, 2)
	plt.plot(x2, y2, "*-", color="blue")
	plt.plot([10000], [0], "o", color="red", label="true NC")
	plt.xlabel("NC")
	plt.ylabel("Sum of Squared Distance Between Estimated and Real NC")
	plt.title("IBD Number Distance Curve for $NC_{real}$ = 10000")
	plt.legend()
	plt.grid('on')



	#####################################################################
	plt.subplot(2, 2, 3)
	## get the five scaling coefficients first

	mean1 = MeanValue(y1)
	mean2 = MeanValue(y2)

	ratio = mean1 * 1.0 / mean2
	beta = [0.4, 0.7, 1.0, 1.3, 1.6]
	alpha = [0.4, 0.7, 1.0, 1.3, 1.6]
	for i in range(len(alpha)):
		beta[i] = beta[i] * ratio

	color = ["blue", "green", "cyan", "magenta", "yellow"]

	## plot the five curves
	for i in range(len(beta)):

		x_temp = NC_list
		y_temp = []
		for j in range(len(x_temp)):
			y_temp.append(y1[j] + beta[i] * y2[j])
		plt.plot(x_temp, y_temp, "*--", color=color[i], label="Mean(IBDNumber) = " + str(alpha[i]) + " * Mean(CohortSharing)")

	plt.plot([10000], [0], "o", color="red", label="true NC")
	plt.xlabel("NC")
	plt.ylabel("Combined Distance Between Estimated and Real NC")
	plt.title("Combined Distance Curve (scaled according to mean value of each distance curve)")
	plt.legend()
	plt.grid('on')



	#####################################################################
	plt.subplot(2, 2, 4)
	## get the five scaling coefficients first

	max1 = MaxElement(y1)
	max2 = MaxElement(y2)

	ratio = max1 * 1.0 / max2
	beta = [0.4, 0.7, 1.0, 1.3, 1.6]
	alpha = [0.4, 0.7, 1.0, 1.3, 1.6]
	for i in range(len(alpha)):
		beta[i] = beta[i] * ratio

	color = ["blue", "green", "cyan", "magenta", "yellow"]

	## plot the five curves
	for i in range(len(beta)):
		
		x_temp = NC_list
		y_temp = []
		for j in range(len(x_temp)):
			y_temp.append(y1[j] + beta[i] * y2[j])
		plt.plot(x_temp, y_temp, "*--", color=color[i], label="Max(IBDNumber) = " + str(alpha[i]) + " * Max(CohortSharing)")

	plt.plot([10000], [0], "o", color="red", label="true NC")
	plt.xlabel("NC")
	plt.ylabel("Combined Distance Between Estimated and Real NC")
	plt.title("Combined Distance Curve (scaled according to maximum value of each distance curve)")
	plt.legend()
	plt.grid('on')




	#####################################################################
	plt.show()
