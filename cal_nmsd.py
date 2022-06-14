from myvasp import vasp_EPI_dp_shell as epi_dp                                                                              from yaya_metal.yaya_re import yaya_io
import numpy as np
import os, re

# extract_number from string
re_digits = re.compile(r'(\d+)')
def extract_number(str):
    pieces = re_digits.split(str)
    return int(pieces[1])

# cfg need to cal
file_set = ['POSCAR/' + f +'/CONTCAR' for f in os.listdir('POSCAR')]
# sort by number
file_set.sort(key = lambda x: extract_number(x))

a=3.81

def pbc_delta(vector1,vector2,cell):
    delta = []
    for i in range(len(cell)):
        d = min(abs(vector1[i]-vector2[i]),abs(vector1[i]-vector2[i]+cell[i]),abs(vector1[i]-vector2[i]-cell[i]))
        delta.append(d)
    return delta

msd_per_cfg = []
for f in file_set:
    atoms = yaya_io.read_vasp(f)
# perfect lattice
# same atoms
    numbers_pre = atoms.numbers.copy()
    atoms.numbers = np.where(numbers_pre == 28, 79, numbers_pre)
    os.chdir('perfect_lattice')
    yaya_io.write_lammps_data(atoms)
    os.system('./run.bash')
    atoms0 = yaya_io.read_lammps_dump('perfect')
    atoms0.numbers = numbers_pre # perfect
    atoms.numbers = numbers_pre  # relaxed(pre)
    os.chdir('../')

    positions0 = atoms0.positions
    positions1 = atoms.positions
    cell = [atoms.cell[0][0],atoms.cell[1][1],atoms.cell[2][2]]

    delta = [pbc_delta(positions0[i],positions1[i],cell) for i in range(len(positions0))]

    square = [i[0]*i[0]+i[1]*i[1]+i[2]*i[2] for i in delta]
    square = np.array(square)
    msd = square.mean()
    msd_per_cfg.append(msd)
nmsd_per_cfg = np.array(msd_per_cfg)/a**2
np.save('nmsd.npy',msd_per_cfg)
np.savetxt('nmsd.txt', msd_per_cfg)
