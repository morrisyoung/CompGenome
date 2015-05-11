import matplotlib.pyplot as plt
n = 200
n_last = 150


if __name__ == '__main__':


	plt.figure()

	for N in range(1000, 11000, 1000):

		filename = "./data/statistic_N" + str(N) + ".ibd"
		file = open(filename, "r")

		statistic = {}

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
			statistic[i] = fraction

		i = 5
		x = []
		y = []
		while i < n_last:
			x.append(i)
			y.append(statistic[i])
			i += 5

		if N == 1000:
			plt.plot(x, y, "o-",label="$N=1000$", color="red")
		if N == 2000:
			plt.plot(x, y, "o-",label="$N=2000$", color="yellow")
		if N == 3000:
			plt.plot(x, y, "o-",label="$N=3000$", color="green")
		if N == 4000:
			plt.plot(x, y, "o-",label="$N=4000$", color="cyan")
		if N == 5000:
			plt.plot(x, y, "o-",label="$N=5000$", color="blue")

		if N == 6000:
			plt.plot(x, y, "*-",label="$N=6000$", color="red")
		if N == 7000:
			plt.plot(x, y, "*-",label="$N=7000$", color="yellow")
		if N == 8000:
			plt.plot(x, y, "*-",label="$N=8000$", color="green")
		if N == 9000:
			plt.plot(x, y, "*-",label="$N=9000$", color="cyan")
		if N == 10000:
			plt.plot(x, y, "*-",label="$N=10000$", color="blue")


			




	plt.xlabel("number of sequenced individuals")
	plt.ylabel("average cohort-sharing fraction")
	plt.title("Cohort-sharing statistic (constant population size)\ntotal number of randomizations: 1000")
	plt.ylim(0, 1)
	plt.xlim(0, 200)
	plt.legend(loc=4)
	plt.grid('on')
	plt.show()
