'''
  File name: carv.py
  Author: Hantian Liu
  Date created:
'''

'''
  File clarification:
    Aimed to handle finding seams of minimum energy, and seam removal, the algorithm
    shall tackle resizing images when it may be required to remove more than one seam, 
    sequentially and potentially along different directions.
    
    - INPUT I: n × m × 3 matrix representing the input image.
    - INPUT nr: the numbers of rows to be removed from the image.
    - INPUT nc: the numbers of columns to be removed from the image.
    - OUTPUT Ic: (n − nr) × (m − nc) × 3 matrix representing the carved image.
    - OUTPUT T: (nr + 1) × (nc + 1) matrix representing the transport map.
'''

import numpy as np
from cumMinEngHor import cumMinEngHor
from cumMinEngVer import cumMinEngVer
from rmHorSeam import rmHorSeam
from rmVerSeam import rmVerSeam
from genEngMap import genEngMap
import imageio
import matplotlib.pyplot as plt

'''
def mincost(r, c, I, record):
  if r==0 && c==0:
    return 0
  else:
    emap=genEngMap(I)
    [Mx, Tbx] = cumMinEngVer(emap)
    [My, Tby] = cumMinEngHor(emap)
    [Ix, Ex] = rmVerSeam(I, Mx, Tbx)
    [Iy, Ey] = rmHorSeam(I, My, Tby)
    if (mincost(r-1,c, Ix)+ Ex >= mincost(r,c-1, Iy)+ Ey) :
      record[r-1,c-1]=1
      return mincost(r,c-1, Iy)+ Ey
    else:
      record[r-1,c-1]=0
      return mincost(r-1,c, Ix)+ Ex
'''


def carv(I, nr, nc):
	# record=np.zeros(np.array([nr,nc]))
	# T=mincost(nr, nc, I, record)

	T = np.zeros(np.array([nr + 1, nc + 1]))

	path=T # to find the path for generating the result

	# x_mesh, y_mesh=np.meshgrid(np.arange(nr), np.arange(nc))
	dict = {(0, 0): I}

	for i in range(0, nr + 1):
		print(i)
		for j in range(0, nc + 1):
			print(j)
			if (i == 0 and j == 0):
				T[i, j] = 0
			elif i == 0:
				emap = genEngMap(dict[(i, j - 1)])
				[Mx, Tbx] = cumMinEngVer(emap)
				[Ix, Ex] = rmVerSeam(dict[(i, j - 1)], Mx, Tbx)
				dict[(i, j)] = Ix
				T[i, j] = T[i, j - 1] + Ex
				path[i,j]=-1
			elif j == 0:
				emap = genEngMap(dict[(i - 1, j)])
				[My, Tby] = cumMinEngHor(emap)
				[Iy, Ey] = rmHorSeam(dict[(i - 1, j)], My, Tby)
				dict[(i, j)] = Iy
				T[i, j] = T[i - 1, j] + Ey
				path[i,j]=1
			else:
				emap = genEngMap(dict[(i, j - 1)])
				emap2 = genEngMap(dict[(i - 1, j)])
				[Mx, Tbx] = cumMinEngVer(emap)
				[My, Tby] = cumMinEngHor(emap2)
				[Ix, Ex] = rmVerSeam(dict[(i, j - 1)], Mx, Tbx)
				[Iy, Ey] = rmHorSeam(dict[(i - 1, j)], My, Tby)
				if (T[i - 1, j] + Ey <= T[i, j - 1] + Ex):
					dict[(i, j)] = Iy
					T[i, j] = T[i - 1, j] + Ey
					path[i,j]=1
				else:
					dict[(i, j)] = Ix
					T[i, j] = T[i, j - 1] + Ex
					path[i,j]=-1

	res_list = []
	r=nr
	c=nc
	while path[r,c]!=0:
		if path[r,c]==1:
			res_list.append(dict[(r,c)])
			r=r-1
		elif path[r,c]==-1:
			res_list.append(dict[(r,c)])
			c=c-1
	res_list.append(dict[(0,0)])
	res_list.reverse()

	return dict[(i, j)], T, res_list
