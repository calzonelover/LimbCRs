from ROOT import *
from math import *
import pyfits


#fileneme spacecraft
f_sp= ['lat_spacecraft_weekly_w%03d_p202_v001.fits'%(i+10) for i in range(390)]

#file = ['lat_photon_weekly_w0%d_p302_v001.fits'%(i+10) for i in range(90)]
f_photon = ['select_photon_w%d.fits'%(i+10) for i in range(390)]


# Cut ROCKING_ANGLE
for f in f_sp:
	# Look at table
	file_sp = pyfits.open(f)
	file_table = file_sp[1].data
	# Cut zenith
	file_selected = file_table.field('ROCK_ANGLE') > 52.0
	file_cut = file_table[file_selected]
	# HDU write
	hdu = pyfits.BinTableHDU(file_cut)
	hdu.writeto('Cut_ROCKING_ANGLE_52/%s'%f)
	print(f)
'''

# plot distribution
Dist_ROCK = TH1F('ROCK distribution', 'ROCK distribution', 2700, 0., 90.)
#file = 0
for f in f_sp:
	'''
	file +=1
	if file == 3:
		break
	'''
	print(f)
	file_sp = pyfits.open(f)
	event = file_sp[1].data
	for i in range(len(event)):
		Dist_ROCK.Fill(abs(event[i]['ROCK_ANGLE']))

C = TCanvas('C','C',800,600)
Dist_ROCK.Draw()
Dist_ROCK.GetXaxis().SetTitle('#theta_{ROCK}')
Dist_ROCK.GetYaxis().SetTitle('Count')
raw_input()
'''
