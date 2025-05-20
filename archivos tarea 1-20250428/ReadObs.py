import json
import iris
import numpy as np
import datetime
from   matplotlib.dates import strpdate2num,num2epoch
import sys
from   cf_units import Unit


def readSMN(file):
    fn = lambda astr: strpdate2num('%d/%m/%Y %H:%M')(astr.decode())
    SNP = np.genfromtxt (file, delimiter=(16,31,10,10,10,10,10,10),\
                         usecols=(0,1,2,3,4,5,6,7),\
                         skip_header=1, skip_footer=3,\
                         converters={0:fn},\
                         dtype=None)


    num_obs= len(SNP)
    time_data = np.zeros(num_obs-1)
    obs_data  = np.zeros(num_obs-1, np.float32)
    precip_data  = np.zeros(num_obs-1, np.float32)

    for obs in range(0, num_obs-1):
     time_data[obs]   = num2epoch(SNP[obs][0])
     obs_data[obs]    = SNP[obs][3]
     precip_data[obs] = SNP[obs][6]

    time = iris.coords.DimCoord(time_data,\
                         standard_name='time',\
                         units=Unit('seconds since epoch'))

    cubeTemp = iris.cube.Cube(obs_data,\
                dim_coords_and_dims=[(time, 0)])
    cubeTemp.units=Unit('celsius')
    cubeTemp.rename ( 'Temperature')

    cubePrecip = iris.cube.Cube(precip_data,\
                dim_coords_and_dims=[(time, 0)])
    cubePrecip.units=Unit('mm')
    cubePrecip.rename ( 'Precipitation')


    cubeList = iris.cube.CubeList([cubeTemp,cubePrecip])
    return cubeList;

try:
  file = sys.argv[1]
except:
    print ("usage:",sys.argv[0]," filename")
    exit(0)
    
iris.FUTURE.netcdf_no_unlimited=True

try:

    SMN_obs_cube = readSMN(file+".txt")
    attributes=SMN_obs_cube[0].attributes
    attributes['raw_to_nc'] = '$Id: dummy 00 $'
    attributes=SMN_obs_cube[1].attributes
    attributes['raw_to_nc'] = '$Id: dummy 00 $'
    iris.save(SMN_obs_cube, file+'.nc')

except:
    import traceback 
    print ("Error in SMN " + sys.argv[0] + ' ' + file)
    traceback.print_exc()
