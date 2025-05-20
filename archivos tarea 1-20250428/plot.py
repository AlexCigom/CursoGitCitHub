import matplotlib as mpl
mpl.use('Agg')
import iris
import iris.quickplot as qplt
import sys
import matplotlib.pyplot as plt
from   io                import StringIO
import numpy as np

s =  StringIO(u"$Id: dummy 01 ")
svn = np.genfromtxt(s, dtype=None, usecols=(1,2), names = ['filename','rev'], delimiter=" ", encoding='ascii')

file = sys.argv[1]

precip=iris.load_cube(file+".hrsum_nc","Precipitation")
print (precip)

data_svn        = StringIO(str(precip.attributes['raw_to_nc']))
data_svn_parsed = np.genfromtxt (data_svn, delimiter=' ', usecols=(1,2), dtype=None, names = ['filename','rev'], encoding='ascii')

qplt.plot(precip,'o')
plt.title(precip.name()+"\n"+str(data_svn_parsed["filename"])+\
                     " Rev:"+str(data_svn_parsed["rev"])+\
                     " "+str(svn["filename"])+" Rev:"+str(svn["rev"]))
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig(file+'.pdf')
