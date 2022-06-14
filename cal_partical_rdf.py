from ovito.io import import_file
from ovito.modifiers import CoordinationAnalysisModifier
import numpy as np
import os, re                                                                                                                

# cfg need to cal
file_set = ['POSCAR/' + f +'/CONTCAR' for f in os.listdir('POSCAR')]
# sort by number
file_set.sort()



rdf_list = []
for f in file_set:
#load file
    pipeline = import_file(f)

# Calculate partial RDFs:
    pipeline.modifiers.append(CoordinationAnalysisModifier(cutoff=5.0, number_of_bins=100, partial=True))
    rdf_table = pipeline.compute().tables['coordination-rdf']

# Au-Au Au-Ni Ni-Ni here
    rdf_names = rdf_table.y.component_names
# distance, Au-Au ....
    rdf = rdf_table.xy()
# 3 type
    r = []
    for i in range(3):
        line = rdf[:,i+1]
        r.append(rdf[:,0][np.argwhere(line==max(line))[0][0]])
    rdf_list.append(r)

rdf_list = np.array(rdf_list)

np.savetxt('rdf_list.txt',rdf_list)

rdf_mean = [rdf_list[:,i].mean() for i in range(3)]

np.savetxt('rdf_mean.txt',rdf_mean)
