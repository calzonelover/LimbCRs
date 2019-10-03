import pyIrfLoader
from math import *
from array import *
import numpy as np
import pyfits

pyIrfLoader.Loader_go()
myFactory = pyIrfLoader.IrfsFactory_instance()
irfs_f = myFactory.create("P8R2_SOURCE_V6::FRONT")
irfs_b = myFactory.create("P8R2_SOURCE_V6::BACK")
aeff_f = irfs_f.aeff()
aeff_b = irfs_b.aeff()

