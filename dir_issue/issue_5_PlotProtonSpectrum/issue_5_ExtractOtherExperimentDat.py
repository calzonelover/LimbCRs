from math import *
import numpy as np
import csv
import re # regular expression

#### Plot Setting ###

#### End Plot Setting ###

def getData():
	# AMS-02
	dat_AMS = csv.reader(open('ProtonAMS02.csv', 'r'),delimiter=',')
	# PAMELA
	dat_PAMELA = csv.reader(open('ProtonPAMELA.csv', 'r'),delimiter=',')
	return dat_AMS, dat_PAMELA
## Function for fill edge bin
def fillEdgeBin():
	dat_AMS, dat_PAMELA = getData()
	# energy bin for individual histogram (TH1F)
	binEdgeAMS = []
	binEdgePAMELA = []
	## For AMS
	for i, row in enumerate(dat_AMS):
		# fill edge bin AMS
		if i == 0:
			binEdgeAMS.append(float(row[0]))
		binEdgeAMS.append(float(row[2]))
		# fill edge bin PAMELA
	## For PAMELA
	for i, row in enumerate(dat_PAMELA):
		if i == 0:
			binEdgePAMELA.append(float(re.split(r' - ', row[0])[0]))
		binEdgePAMELA.append(float(re.split(r' - ', row[0])[1]))
	return binEdgeAMS, binEdgePAMELA

### method for get Flux
def getFlux():
	dat_AMS, dat_PAMELA = getData()
	# flux bin
	binFluxAMS = []
	binFluxPAMELA = []
	# AMS
	for i, row in enumerate(dat_AMS):
		flux_i = float(re.split(r'\(', row[3])[1])
		try:
			fluxDeg_i = float(re.split(r'10', row[9])[-1])
		except ValueError:
			fluxDeg_i = -1.0*float(re.split(r'10', row[9])[-1][1:])
		binFluxAMS.append(flux_i*10.0**(fluxDeg_i))
	# PAMELA
	for i, row in enumerate(dat_PAMELA):
		try:
			binFluxPAMELA.append(float(re.split(r'±', row[-1])[0]))
		except ValueError:
			flux_i = float(re.split(r'±', row[-1])[0][1:])
			fluxDeg_i = -1.0*float(re.split(r'±', row[-1])[-1][-1])
			binFluxPAMELA.append(flux_i*10.0**fluxDeg_i)
	return binFluxAMS, binFluxPAMELA

### method for get an error
## Statistics
def getStatError():
	dat_AMS, dat_PAMELA = getData()
	# error bin
	binStatErrorAMS = []
	binStatErrorPAMELA = []
	# AMS
	for i, row in enumerate(dat_AMS):
		try:
			Deg_i = float(re.split(r'10', row[9])[-1])
		except ValueError:
			Deg_i = -1.0*float(re.split(r'10', row[9])[-1][1:])
		binStatErrorAMS.append(float(row[4])*10.0**Deg_i)
	# PAMELA
	for i, row in enumerate(dat_PAMELA):
		error_i = float(re.split(r'±', row[-1])[1])
		if re.split(r'[(]', row[-1])[0] == '':
			Deg_i = -1.0*float(re.split(r'±', row[-1])[-1][-1])
			binStatErrorPAMELA.append(error_i*10.0**Deg_i)
		else:
			binStatErrorPAMELA.append(error_i)
	return binStatErrorAMS, binStatErrorPAMELA
## Systematics
def getSysError():
	dat_AMS, dat_PAMELA = getData()
	# error bin
	binSysErrorAMS = []
	binSysErrorPAMELA = []
	# AMS
	for i, row in enumerate(dat_AMS):
		error_i = float(re.split(r'[)]', row[-1])[0])
		try:
			Deg_i = float(re.split(r'10', row[9])[-1])
		except ValueError:
			Deg_i = -1.0*float(re.split(r'10', row[9])[-1][1:])
		binSysErrorAMS.append(error_i*10.0**Deg_i)
	# PAMELA
	for i, row in enumerate(dat_PAMELA):
		error_i = float(re.split(r'[)]', re.split(r'±', row[-1])[-1])[0])
		if re.split(r'[(]', row[-1])[0] == '':
			Deg_i = -1.0*float(re.split(r'±', row[-1])[-1][-1])
			binSysErrorPAMELA.append(error_i*10.0**Deg_i)
		else:
			binSysErrorPAMELA.append(error_i)
	return binSysErrorAMS, binSysErrorPAMELA


if __name__ == "__main__":
	### get data from CSV file
	### get edge bin of each histogram
	binEdgeAMS, binEdgePAMELA = fillEdgeBin()
	### get flux data
	binFluxAMS, binFluxPAMELA = getFlux()
	### get error bar
	binStatErrorAMS, binStatErrorPAMELA = getStatError()
	binSysErrorAMS, binSysErrorPAMELA = getSysError()
	### write data to txt file
	f_AMS = open('AMS_data.dat','w')
	f_PAMELA = open('PAMELA_data.dat','w')
	# write AMS
	for i in range(len(binEdgeAMS)):
		try:
			f_AMS.write('%f %f %f %f\n'%(binEdgeAMS[i], binFluxAMS[i]\
						 			   , binStatErrorAMS[i], binSysErrorAMS[i]))
		except IndexError:
			f_AMS.write('%f 0 0 0\n'%(binEdgeAMS[i]))
	for i in range(len(binEdgePAMELA)):
		try:
			f_PAMELA.write('%f %f %f %f\n'%(binEdgePAMELA[i], binFluxPAMELA[i]\
										  , binStatErrorPAMELA[i], binSysErrorPAMELA[i]))
		except IndexError:
			f_PAMELA.write('%f 0 0 0\n'%(binEdgePAMELA[i]))
	print("done")
