from math import *
import numpy as np
import matplotlib.pyplot as plt

#### Setting #####

# File IO
f_time = 'issue_3_time.olo'
f_count = 'issue_3_count.olo'

# setting visualize
xLabelName = 'Time_Cut52/Time_Cut42'
yLabelName = 'Count_Cut52_Limb/Count_limb'

#### End Setting ####


#### Define function ####

# read file (Return as a array of each week)
def getFraction():
	# get data
	dat_time = np.genfromtxt(f_time)
	dat_count = np.genfromtxt(f_count)
	try:
		fracC, fracT = np.divide(dat_count[:, 2], dat_count[:, 1])\
					  ,np.divide(dat_time[:, 2], dat_time[:, 1])
	except ZeroDivisionError:
		print('Found zero divider !!')
		exit()
	return fracC, fracT

# plot
def plot(array_x, array_y):
	plt.scatter(array_x, array_y)
	plt.xlabel(xLabelName)
	plt.ylabel(yLabelName)
	plt.show()



########################
#     Main program 
########################

if __name__ == '__main__':
	# get fraction
	fracC, fracT = getFraction()
	# Plot
	plot(fracT, fracC)











