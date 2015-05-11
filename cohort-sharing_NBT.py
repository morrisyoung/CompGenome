## this script is used to calculate the cohort-sharing statistic of IBD, for one specific population parameter
## input: simulated IBD segments
## process: ITERATION times SIMULATION runs for this parameter value (e.g. N = 5000)
## output: i = [5, 10, 15, 20, 25, 30, ..., 95] with their cohort-sharing fraction statistic

import numpy as np  ##TODO PLEASE use the random in numpy, other than the seperate random package
#import matplotlib.pyplot as plt
import sys
import time
import os


n = 200 ## sample size; always 100 in this testing
n_last = 150
L = 100000000
ITERATION = 50
SIMULATION = 20
segment_sharing = []



def para_generator(filename, NB, T):
        #### all the parameters accepted here are float; we should re-form them as needed ####
        global n

        NC = 10000
        NA = 10000
	#NB = NB
	TB = 30
	#T = 10

	filehandle = open(filename, 'w')
        filehandle.write('//Number of population samples (demes)\n1\n')
        filehandle.write('//Population effective sizes (number of genes)\n')
        filehandle.write(str(int(NC))+'\n')
        filehandle.write('//Sample sizes\n')
        filehandle.write(str(n)+'\n')
        filehandle.write('//Growth rates        : negative growth implies population expansion\n0\n')
        filehandle.write('//Number of migration matrices : 0 implies no migration between demes\n0\n')

        ## historical events:
        ##====================
        filehandle.write('//historical event: time, source, sink, migrants, new size, new growth rate, migr. matrix\n2  historical event\n')
        filehandle.write(str(int(TB)))
        filehandle.write(' 0 0 0 ')
        filehandle.write(str(NB*1.0/NC))
        filehandle.write(' 0 0\n')
        TBEND = TB + T
        filehandle.write(str(int(TBEND)))
        filehandle.write(' 0 0 0 ')
        filehandle.write(str(NA*1.0/NB))
        filehandle.write(' 0 0\n')
        ##====================

        filehandle.write('//Number of independent loci [chromosome]\n1 0\n')
        filehandle.write('//Per chromosome: Number of linkage blocks\n1\n')
        filehandle.write('//per Block: data type, num loci, rec. rate and mut rate + optional parameters\nDNA 100000000 0.00000001 0.00000002 0.33\n')
        filehandle.write('\n')
        filehandle.close()

	return



def sort_merge_intervals_fraction():
	global n
	global n_last
	global L
	global ITERATION
	global segment_sharing
	global N
	## input: list of intervals: [ (start, end), (start, end), ... ]
	## output: the fraction number: (total length of all merged intervals)/(length of the chromosome)
	## the following is the detailed algorithm:
	#1. Sort the intervals based on increasing order of starting time.
	#2. Push the first interval on to a stack.
	#3. For each interval do the following
	#	a. If the current interval does not overlap with the stack top, push it.
	#	b. If the current interval overlaps with stack top and ending time of current interval is more than that of stack top, update stack top with the ending time of current interval.
	#4. At the end stack contains the merged intervals.

	segment_sharing.sort(key = lambda tup: tup[0])
	stack = []

	while len(segment_sharing) != 0:
		interval = segment_sharing[0]
		del segment_sharing[0]

		if len(stack) == 0:
			stack.append(interval)
			continue

		## compare interval with the head of stack
		if interval[0] <= stack[-1][1]:
			if interval[1] > stack[-1][1]: ## extend to the end of this interval
				stack[-1] = (stack[-1][0], interval[1])
			else: ## simply drop this interval
				continue
		else:
			stack.append(interval)

	fraction = 0
	for interval in stack:
		fraction += interval[1] - interval[0]

	fraction = fraction * 1.0 / ( L * 1.0 )

	return fraction



def statistic_from_single_simu(filename):
	global n
	global n_last
	global L
	global ITERATION
	global segment_sharing
	global N

	file = open(filename, "r")

	repository = {} ## { 2:{ 3:[xxx-xxx, xxx-xxx],  5:[xxx-xxx, xxx-xxx, xxx-xxx],  ... },  5:{},  ...          }
	while 1:
		line = file.readline()

		if not line:
			break

		line = (line.strip()).split(" ")
		pair = (line[0]).split("-")
		## all the following are strings
		individual1 = int(pair[0])
		individual2 = int(pair[1])
		segment = line[1][1:-1]

		## inject the rep; individual1 < individual2 always holds
		if individual1 in repository:
			if individual2 in repository[individual1]:
				repository[individual1][individual2].append(segment)
			else:
				repository[individual1][individual2] = [segment]
		else:
			repository[individual1] = {}
			repository[individual1][individual2] = [segment]
	file.close()


	## randomly draw numbers

	statistic = {}
	i = 5
	while i < n_last:

		result = np.array([])

		for k in range(ITERATION):
			## i individuals are sequenced
			ref = np.random.random_integers(1, n)

			## draw i individuals from [1,...,n].remove(ref)
			# the following method is wrong; it does not sample i numbers simutaneously
			#candidates = np.array([ref])
			#while ref in candidates:
			#	candidates = random.random_integers(1, n, i)
			array = np.arange(1, n + 1)
			np.delete(array, ref - 1)
			candidates = (np.random.permutation(array))[0:i]


			# gather all the segments
			del segment_sharing[:]
			for candidate in candidates:
				## accumulate the total fraction
				if candidate < i:
					if candidate not in repository:
						continue
					else:
						if i not in repository[candidate]:
							continue
						else:
							for segment in repository[candidate][i]:
								[start, end] = map(lambda x: int(x), segment.split(","))
								segment_sharing.append((start, end))
				else:
					if i not in repository:
						continue
					else:
						if candidate not in repository[i]:
							continue
						else:
							for segment in repository[i][candidate]:
								[start, end] = map(lambda x: int(x), segment.split(","))
								segment_sharing.append((start, end))

			fraction = sort_merge_intervals_fraction()
			result = np.append(result, fraction)

		## get the average of the "iteration" fractions
		average = np.average(result)
		statistic[i] = average

		## refresh the counter
		i += 5

	return statistic



if __name__ == '__main__':


	#NB_list = [130, 150, 165, 180, 190, 195, 200, 205, 210, 220, 235, 250, 280]
	NB_list = [130, 150, 165, 180, 190, 195]
	T_list = [1, 3, 5, 7, 8, 9, 10, 11, 12, 13, 15, 17, 19]


	for NB in NB_list:
		for T in T_list:


			## generate the parameter file
			para_generator("simu.par", NB, T)



			###===== timing =====
			time_start = time.time()



			statistic_ave = {}

			for i in range(SIMULATION):
				print "NB and T are",
				print NB,
				print T,
				print "working on simulation #",
				print i + 1,
				print "total number:",
				print SIMULATION

				## generate the tree file (in "./simu/")
				os.system('./fastsimcoal21 -i simu.par -n 1 -T >/dev/null 2>&1')

				## generate the IBD segment
				os.system('./IBDdetection_naive -f ./simu/simu_1_true_trees.trees -F 0 -t 0 -m 1000000 -e 0.01 -d 10000 -l 100000000 -T 1 -o result.ibd  >/dev/null 2>&1')

				filename = "result.ibd"
				statistic = statistic_from_single_simu(filename)
				for key in statistic:
					if key not in statistic_ave:
						statistic_ave[key] = statistic[key]
					else:
						statistic_ave[key] += statistic[key]

			## average results from all simulations
			for key in statistic_ave:
				statistic_ave[key] = statistic_ave[key] / (SIMULATION * 1.0)



			##============== save the statistic for this parameter =================
			file = open("statistic_NB" + str(NB) + "T" + str(T) + ".ibd", "w")
			file.write("ITERATION " + str(ITERATION) + " SIMULATION " + str(SIMULATION) + "\n")
			for key in statistic_ave:
				file.write(str(key) + " " + str(statistic_ave[key]) + "\n")
			file.close()



			###===== timing =====
			time_end = time.time()
			print "total time used is",
			print time_end - time_start,
			print "seconds"
