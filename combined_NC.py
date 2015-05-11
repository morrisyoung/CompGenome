## this is used to test the combined distance curve, for IBD number distribution and cohort-sharing statistics


### one section:
## this script is used to calculate the cohort-sharing statistic of IBD, for one specific population parameter
## input: simulated IBD segments
## process: ITERATION times SIMULATION runs for this parameter value (e.g. N = 5000)
## output: i = [5, 10, 15, 20, 25, 30, ..., 95] with their cohort-sharing fraction statistic


### another section:
## this is for the IBD number distribution


import numpy as np  ##TODO PLEASE use the random in numpy, other than the seperate random package
#import matplotlib.pyplot as plt
import sys
import time
import os


##===== mainly for cohort-sharing =====
n = 200 ## sample size; always 100 in this testing
n_last = 150
L = 100000000
ITERATION = 50
SIMULATION = 20
segment_sharing = []

##===== mainly for IBD number =====
seg_min = 250000 # this is the base of increase for the model1
m = 1000000
SIMULATION2 = 1000




def para_generator(filename, N):
        #### all the parameters accepted here are float; we should re-form them as needed ####
        global n

        NC = N  ## or NA
        NA = 10000
	NB = 200
	TB = 30
	T = 10

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




###=========================== cohort-sharing statistics =============================
def sort_merge_intervals_fraction():
	global n
	global n_last
	global L
	global ITERATION
	global segment_sharing
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
###===================================================================================




###================================= IBD number ======================================
def seg_process(seg):
	##return the index that this segment belongs to
	global m
	global seg_min
	global L

	coor_present = m
	index = 1
	coor_next = coor_present + seg_min*index
	while(coor_next <= L):
		if seg >= coor_present and seg < coor_next:
			return index
		else:
			index = index*2
			coor_present = coor_next
			coor_next = coor_next + seg_min*index
	return index


#def stat(filename, hashtable1, hashtable2):
def statistic_from_single_simu_IBDNumber(filename):
	global n

	filehandle = open(filename, 'r')
	hashtable1 = {}
	hashtable2 = {}

	h = {}
	for i in range(1, n + 1):
		for j in range(i + 1, n + 1):
			key = str(i) + '-' + str(j)
			h[key] = []

	while 1:
		line = filehandle.readline()
		if not line:
			break
		line = line.strip()
		line = line.split(" ")
		line[1] = line[1][1:-1].split(",")
		line[1] = int(line[1][1]) - int(line[1][0])
		#print line[0]
		#print line[1]
		key = line[0] #the key, or pair name
		value = line[1] #the interval
		h[key].append(value)

	##h: {'1-2':[234,153,...], ...}
	for key in h:
		# for model2: IBD frequency spectrum
		num = len(h[key])
		if num in hashtable2:
			hashtable2[num]+=1
		else:
			hashtable2[num]=1

		# for model1:  IBD count distribution
		for seg in h[key]: # seg is a int number
			index = seg_process(seg)
			if index in hashtable1:
				hashtable1[index]+=1
			else:
				hashtable1[index]=1

	filehandle.close()
	return hashtable1
##====================================================================================






if __name__ == '__main__':


	NC_list = [5000, 6000, 7000, 7500, 8000, 8500, 9000, 9300, 9500, 9600, 9700, 9800, 9900, 9950, 10000, 10050, 10100, 10200, 10300, 10500, 10800, 11000, 11500, 12000, 13000, 14000, 16000, 18000, 20000]

	for NC in NC_list:

		## generate the parameter file
		para_generator("simu.par", NC)


		###============================== cohort-sharing =============================
		###===== timing =====
		time_start = time.time()

		statistic_ave = {}

		for i in range(SIMULATION):
			print "cohort-sharing:",
			print "NC is",
			print NC,
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
		file = open("CohortSharing_NC" + str(NC) + ".ibd", "w")
		file.write("ITERATION " + str(ITERATION) + " SIMULATION " + str(SIMULATION) + "\n")
		for key in statistic_ave:
			file.write(str(key) + " " + str(statistic_ave[key]) + "\n")
		file.close()

		###===== timing =====
		time_end = time.time()
		print "total time used for cohort-sharing is",
		print time_end - time_start,
		print "seconds"



		###============================== IBD number =============================
		###===== timing =====
		time_start = time.time()

		statistic_ave = {}
		
		for i in range(SIMULATION2):  ## for a more assured distance curve, we use this for averaging
			print "IBD number:",
			print "NC is",
			print NC,
			print "working on simulation #",
			print i + 1,
			print "total number:",
			print SIMULATION2

			## generate the tree file (in "./simu/")
			os.system('./fastsimcoal21 -i simu.par -n 1 -T >/dev/null 2>&1')

			## generate the IBD segment
			os.system('./IBDdetection_naive -f ./simu/simu_1_true_trees.trees -F 0 -t 0 -m 1000000 -e 0.01 -d 10000 -l 100000000 -T 1 -o result.ibd  >/dev/null 2>&1')

			filename = "result.ibd"
			statistic = statistic_from_single_simu_IBDNumber(filename)

			for key in statistic:
				if key not in statistic_ave:
					statistic_ave[key] = statistic[key]
				else:
					statistic_ave[key] += statistic[key]

		## average results from all simulations
		for key in statistic_ave:
			statistic_ave[key] = statistic_ave[key] / (SIMULATION2 * 1.0)

		##============== save the statistic for this parameter =================
		file = open("IBDNumber_NC" + str(NC) + ".ibd", "w")
		file.write("SIMULATION " + str(SIMULATION2) + "\n")
		for key in statistic_ave:
			file.write(str(key) + " " + str(statistic_ave[key]) + "\n")
		file.close()

		###===== timing =====
		time_end = time.time()
		print "total time used for IBD number is",
		print time_end - time_start,
		print "seconds"
