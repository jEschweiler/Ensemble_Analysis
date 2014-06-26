import commands
import operator 
from operator import itemgetter
import re
import numpy as np
import sys

files=commands.getoutput("ls *.mfj")
files=files.split()
#print "files", type(files), files
Nspheres=raw_input("enter the number of spheres: ")
Nsph=int(Nspheres)
nc=[]

for item in files[:39]:
	item2=str(item)
        num=(item2.strip("configuration.pymlustermfj"))
        #print "num=", num
	listmasses=list([11087,11087,11087,11695,11695,11695,60304,60304,60304,43000,43000,43000,29839,29839,29839,25221,25221,25221,21944,21944,21944])
	InFileName="configuration."+str(num)+".mfj"
	def getRefStruct(InFile):
	       InFile = open(InFileName,'r') # Open file to read
	       InFileLines = InFile.read().splitlines() # string of lines from pdb file
	       InFile.close()
	       return InFileLines

	def getCoords(lines):
	              outX=[]
	              outY=[]
	              outZ=[]
	              outR=[]
	              for i in lines[6:]:
	                     l = re.findall ("(\S+)", i)
	                     X0 = float(l[0])
	                     Y0 = float(l[1])
	                     Z0 = float(l[2])
	                     R0 = float(l[3])
	                     outX.append(X0)
	                     outY.append(Y0)
	                     outZ.append(Z0)
	                     outR.append(R0)
	                     #print Scr2
	              return outX, outY, outZ, outR

	z1 = getCoords(getRefStruct(InFileName))
	#print z1[0]

	#%%%% get the centroid of the reference structure as given by "Model_0_test.txt" file 

	def getCent(lines):
	       outMX=[]
	       outMY=[]
	       outMZ=[]
	       outTotalM=[]
	       for i in range(0, 3) + range(6,9):
	              MX = listmasses[i]*z1[0][i]
	              #print MX
	              MY = listmasses[i]*z1[1][i]
	              MZ = listmasses[i]*z1[2][i]
	              TotalM = listmasses[i]
	              outMX.append(MX)
	              outMY.append(MY)
	              outMZ.append(MZ)
	              outTotalM.append(TotalM)
	              #print TotalM
	       return outMX, outMY, outMZ, outTotalM       

	comc = getCent(getRefStruct(InFileName))
		#print comc[0]

	def getCentroid(lines):
	       MX1=sum(comc[0])
	       MY1 = sum(comc[1])
	       MZ1 = sum(comc[2])
	       TotalM1 = sum(comc[3])
	       CdX = MX1/TotalM1
	       CdY = MY1/TotalM1
	       CdZ = MZ1/TotalM1
	       return CdX, CdY, CdZ

	ctd = getCentroid(getRefStruct(InFileName))
	#print ctd
	
	def translate(lines):
		newcoords=[]
		for i in range(0,Nsph):		
			newx=z1[0][i] - ctd[0]
			newy=z1[1][i] - ctd[1]
			newz=z1[2][i] - ctd[2]
			coords=newx, newy, newz
			coords=list(coords)
			newcoords.append(coords)

		return newcoords
		
	transxyz=translate(getRefStruct(InFileName))
	nc.append(transxyz)
	#print transxyz
Q=nc[1][0],nc[1][1],nc[1][2],nc[1][6],nc[1][7],nc[1][8]
master_coords=[]
for i in range(0, len(nc)):
	P=nc[0+i][0],nc[0+i][1],nc[0+i][2],nc[0+i][6],nc[0+i][7],nc[0+i][8]
	#Q=nc[1][0],nc[1][1],nc[1][2],nc[1][6],nc[1][7],nc[1][8]
	F=nc[0+i]
	def kabsch(P, Q):
		C = np.dot(np.transpose(P), Q)
		V, S, W = np.linalg.svd(C)
		d = (np.linalg.det(V) * np.linalg.det(W)) < 0.0

		if d:
			S[-1] = -S[-1]
			V[:,-1] = -V[:,-1]

	# Create Rotation matrix U
		U = np.dot(V, W)

	# Rotate P
		PK = np.dot(F, U)
		
		
		return PK

	#print U
	#print 'KP', P



	k=kabsch(P,Q)
	#Q=np.mean(P, Q)
	k=np.array(k)
	master_coords.append(k)


#print len(master_coords)
master_coords=np.array(master_coords)
print np.shape(master_coords)

mean=np.mean(master_coords, axis=0)
mean1=mean[0],mean[1],mean[2],mean[6],mean[7],mean[8]
master_coords2=[]
for i in range(0, len(master_coords)):
	X=master_coords[0+i][0],master_coords[0+i][1],master_coords[0+i][2],master_coords[0+i][6],master_coords[0+i][7],master_coords[0+i][8]
	X=np.array(X)
	print X
	#Q=nc[1][0],nc[1][1],nc[1][2],nc[1][6],nc[1][7],nc[1][8]
	F=master_coords[0+i]
	def kabsch2(X, mean1):
		C = np.dot(np.transpose(X), mean1)
		V, S, W = np.linalg.svd(C)
		d = (np.linalg.det(V) * np.linalg.det(W)) < 0.0

		if d:
			S[-1] = -S[-1]
			V[:,-1] = -V[:,-1]

	# Create Rotation matrix U
		U = np.dot(V, W)

	# Rotate P
		PK1 = np.dot(F, U)
		#return X
		#return mean1
		#return U
		return PK1

	#print U
	#print 'KP', P



	k2=kabsch2(X,mean1)
	#Q=np.mean(P, Q)
	#k2=np.array(k)
	#print "X", k2[0]
	#print "mean1", k2[1]
	#print "U", k2[2]
	print "PK1", k2
	master_coords2.append(k2)
#print "MASTER", master_coords
pymfilem="mean.pym"
pymfilem=open(pymfilem, "w")
pymfilem.write('from pymol.cgo import *'+ '\n')
pymfilem.write('from pymol import cmd'+ '\n')
pymfilem.write('from pymol.vfont import plain' + '\n' + 'data={}' + '\n' + "curdata=[]" + '\n')

for item2 in mean[0:3]:
		item21=str(item2[0])
		item22=str(item2[1])
		item23=str(item2[2])
		pymfilem.write("k='ProteinA geometry'" +'\n' + "if not k in data.keys():" +'\n'+"   data[k]=[]"+'\n'+'curdata=['+'\n'+'COLOR,  0,.6, .6,' + '\n' + 'SPHERE,'+ item21+ ','+ item22+',' + item23+','+ "20.3245," +'\n')
		pymfilem.write("]"+"\n"+"k='ProteinA geometry'" + '\n' + "if k in data.keys():" + "\n" + "   data[k]= data[k]+curdata"+'\n'+"else:" +'\n' +"   data[k]= curdata"+"\n")
		
for item2 in mean[3:6]:
		item21=str(item2[0])
		item22=str(item2[1])
		item23=str(item2[2])
		pymfilem.write("k='ProteinB geometry'" +'\n' + "if not k in data.keys():" +'\n'+"   data[k]=[]"+'\n'+'curdata=['+'\n'+'COLOR,  1,0,.5,' + '\n' + 'SPHERE,'+ item21+ ','+ item22+',' + item23+','+ "18.4662," +'\n')
		pymfilem.write("]"+"\n"+"k='ProteinB geometry'" + '\n' + "if k in data.keys():" + "\n" + "   data[k]= data[k]+curdata"+'\n'+"else:" +'\n' +"   data[k]= curdata"+"\n")

for item2 in mean[6:9]:
		item21=str(item2[0])
		item22=str(item2[1])
		item23=str(item2[2])
		pymfilem.write("k='ProteinC geometry'" +'\n' + "if not k in data.keys():" +'\n'+"   data[k]=[]"+'\n'+'curdata=['+'\n'+'COLOR,  1, 1, .2,' + '\n' + 'SPHERE,'+ item21+ ','+ item22+',' + item23+','+ "34.7381," +'\n')
		pymfilem.write("]"+"\n"+"k='ProteinC geometry'" + '\n' + "if k in data.keys():" + "\n" + "   data[k]= data[k]+curdata"+'\n'+"else:" +'\n' +"   data[k]= curdata"+"\n")



for item2 in mean[9:12]:
		item21=str(item2[0])
		item22=str(item2[1])
		item23=str(item2[2])
		pymfilem.write("k='ProteinM geometry'" +'\n' + "if not k in data.keys():" +'\n'+"   data[k]=[]"+'\n'+'curdata=['+'\n'+'COLOR,  0.8, .4, 0,' + '\n' + 'SPHERE,'+ item21+ ','+ item22+',' + item23+','+ "30.5044," +'\n')
		pymfilem.write("]"+"\n"+"k='ProteinM geometry'" + '\n' + "if k in data.keys():" + "\n" + "   data[k]= data[k]+curdata"+'\n'+"else:" +'\n' +"   data[k]= curdata"+"\n")
		
for item2 in mean[12:15]:
		item21=str(item2[0])
		item22=str(item2[1])
		item23=str(item2[2])
		pymfilem.write("k='ProteinD geometry'" +'\n' + "if not k in data.keys():" +'\n'+"   data[k]=[]"+'\n'+'curdata=['+'\n'+'COLOR,  .6, 1, 1,' + '\n' + 'SPHERE,'+ item21+ ','+ item22+',' + item23+','+ "26.8763," +'\n')
		pymfilem.write("]"+"\n"+"k='ProteinD geometry'" + '\n' + "if k in data.keys():" + "\n" + "   data[k]= data[k]+curdata"+'\n'+"else:" +'\n' +"   data[k]= curdata"+"\n")

for item2 in mean[15:18]:
		item21=str(item2[0])
		item22=str(item2[1])
		item23=str(item2[2])
		pymfilem.write("k='ProteinF geometry'" +'\n' + "if not k in data.keys():" +'\n'+"   data[k]=[]"+'\n'+'curdata=['+'\n'+'COLOR,  0.8, 0, 0.8,' + '\n' + 'SPHERE,'+ item21+ ','+ item22+',' + item23+','+ "24.4043," +'\n')
		pymfilem.write("]"+"\n"+"k='ProteinF geometry'" + '\n' + "if k in data.keys():" + "\n" + "   data[k]= data[k]+curdata"+'\n'+"else:" +'\n' +"   data[k]= curdata"+"\n")

for item2 in mean[18:21]:
		item21=str(item2[0])
		item22=str(item2[1])
		item23=str(item2[2])
		pymfilem.write("k='ProteinG geometry'" +'\n' + "if not k in data.keys():" +'\n'+"   data[k]=[]"+'\n'+'curdata=['+'\n'+'COLOR,  0, 1, 0,' + '\n' + 'SPHERE,'+ item21+ ','+ item22+',' + item23+','+ "24.4629," +'\n')
		pymfilem.write("]"+"\n"+"k='ProteinG geometry'" + '\n' + "if k in data.keys():" + "\n" + "   data[k]= data[k]+curdata"+'\n'+"else:" +'\n' +"   data[k]= curdata"+"\n")

pymfilem.write("for k in data.keys():" + "\n" + "   cmd.load_cgo(data[k], k, 1)" +"\n"+ "data= {}")


#suma1x=sum(master_coords[0][0][0])
a1=[]
a2=[]
a3=[]
b1=[]
b2=[]
b3=[]
c1=[]
c2=[]
c3=[]
m1=[]
m2=[]
m3=[]
d1=[]
d2=[]
d3=[]
f1=[]
f2=[]
f3=[]
g1=[]
g2=[]
g3=[]
#print "master_coords", master_coords2
for i in range(0,39):
	a=master_coords2[i][0]
	a1.append(a)
	a=master_coords2[i][1]
	a2.append(a)
	a=master_coords2[i][2]
	a3.append(a)
	a=master_coords2[i][3]
	b1.append(a)
	a=master_coords2[i][4]
	b2.append(a)
	a=master_coords2[i][5]
	b3.append(a)
	a=master_coords2[i][6]
	c1.append(a)
	a=master_coords2[i][7]
	c2.append(a)
	a=master_coords2[i][8]
	c3.append(a)
	a=master_coords2[i][9]
	m1.append(a)
	a=master_coords2[i][10]
	m2.append(a)
	a=master_coords2[i][11]
	m3.append(a)
	a=master_coords2[i][12]
	d1.append(a)
	a=master_coords2[i][13]
	d2.append(a)
	a=master_coords2[i][14]
	d3.append(a)
	a=master_coords2[i][15]
	f1.append(a)
	a=master_coords2[i][16]
	f2.append(a)
	a=master_coords2[i][17]
	f3.append(a)
	a=master_coords2[i][18]
	g1.append(a)
	a=master_coords2[i][19]
	g2.append(a)
	a=master_coords2[i][20]
	g3.append(a)


a1=np.array(a1)
allcoords= a1, a2, a3, b1, b2, b3, c1, c2, c3, m1, m2, m3, d1, d2, d3, f1, f2, f3, g1, g2, g3
allcoords=np.array(allcoords)
allcoords=np.swapaxes(allcoords, 0, 1)
#print allcoords
#print np.shape(allcoords)

#print a1
#print np.shape(a1)
#print np.sum(a1, axis=0)
	
pymfilename="pym.pym"
pymfile=open(pymfilename, "w")
pymfile.write('from pymol.cgo import *'+ '\n')
pymfile.write('from pymol import cmd'+ '\n')
pymfile.write('from pymol.vfont import plain' + '\n' + 'data={}' + '\n' + "curdata=[]" + '\n')

for item in allcoords:
	for item2 in item[0:3]:
		item21=str(item2[0])
		item22=str(item2[1])
		item23=str(item2[2])
		pymfile.write("k='ProteinA geometry'" +'\n' + "if not k in data.keys():" +'\n'+"   data[k]=[]"+'\n'+'curdata=['+'\n'+'COLOR,  0,.6, .6,' + '\n' + 'SPHERE,'+ item21+ ','+ item22+',' + item23+','+ "20.3245," +'\n')
		pymfile.write("]"+"\n"+"k='ProteinA geometry'" + '\n' + "if k in data.keys():" + "\n" + "   data[k]= data[k]+curdata"+'\n'+"else:" +'\n' +"   data[k]= curdata"+"\n")
		
	for item2 in item[3:6]:
		item21=str(item2[0])
		item22=str(item2[1])
		item23=str(item2[2])
		pymfile.write("k='ProteinB geometry'" +'\n' + "if not k in data.keys():" +'\n'+"   data[k]=[]"+'\n'+'curdata=['+'\n'+'COLOR,  1,0,.5,' + '\n' + 'SPHERE,'+ item21+ ','+ item22+',' + item23+','+ "18.4662," +'\n')
		pymfile.write("]"+"\n"+"k='ProteinB geometry'" + '\n' + "if k in data.keys():" + "\n" + "   data[k]= data[k]+curdata"+'\n'+"else:" +'\n' +"   data[k]= curdata"+"\n")

	for item2 in item[6:9]:
		item21=str(item2[0])
		item22=str(item2[1])
		item23=str(item2[2])
		pymfile.write("k='ProteinC geometry'" +'\n' + "if not k in data.keys():" +'\n'+"   data[k]=[]"+'\n'+'curdata=['+'\n'+'COLOR,  1, 1, .2,' + '\n' + 'SPHERE,'+ item21+ ','+ item22+',' + item23+','+ "34.7381," +'\n')
		pymfile.write("]"+"\n"+"k='ProteinC geometry'" + '\n' + "if k in data.keys():" + "\n" + "   data[k]= data[k]+curdata"+'\n'+"else:" +'\n' +"   data[k]= curdata"+"\n")



	for item2 in item[9:12]:
		item21=str(item2[0])
		item22=str(item2[1])
		item23=str(item2[2])
		pymfile.write("k='ProteinM geometry'" +'\n' + "if not k in data.keys():" +'\n'+"   data[k]=[]"+'\n'+'curdata=['+'\n'+'COLOR,  0.8, .4, 0,' + '\n' + 'SPHERE,'+ item21+ ','+ item22+',' + item23+','+ "30.5044," +'\n')
		pymfile.write("]"+"\n"+"k='ProteinM geometry'" + '\n' + "if k in data.keys():" + "\n" + "   data[k]= data[k]+curdata"+'\n'+"else:" +'\n' +"   data[k]= curdata"+"\n")
		
	for item2 in item[12:15]:
		item21=str(item2[0])
		item22=str(item2[1])
		item23=str(item2[2])
		pymfile.write("k='ProteinD geometry'" +'\n' + "if not k in data.keys():" +'\n'+"   data[k]=[]"+'\n'+'curdata=['+'\n'+'COLOR,  .6, 1, 1,' + '\n' + 'SPHERE,'+ item21+ ','+ item22+',' + item23+','+ "26.8763," +'\n')
		pymfile.write("]"+"\n"+"k='ProteinD geometry'" + '\n' + "if k in data.keys():" + "\n" + "   data[k]= data[k]+curdata"+'\n'+"else:" +'\n' +"   data[k]= curdata"+"\n")

	for item2 in item[15:18]:
		item21=str(item2[0])
		item22=str(item2[1])
		item23=str(item2[2])
		pymfile.write("k='ProteinF geometry'" +'\n' + "if not k in data.keys():" +'\n'+"   data[k]=[]"+'\n'+'curdata=['+'\n'+'COLOR,  0.8, 0, 0.8,' + '\n' + 'SPHERE,'+ item21+ ','+ item22+',' + item23+','+ "24.4043," +'\n')
		pymfile.write("]"+"\n"+"k='ProteinF geometry'" + '\n' + "if k in data.keys():" + "\n" + "   data[k]= data[k]+curdata"+'\n'+"else:" +'\n' +"   data[k]= curdata"+"\n")

	for item2 in item[18:21]:
		item21=str(item2[0])
		item22=str(item2[1])
		item23=str(item2[2])
		pymfile.write("k='ProteinG geometry'" +'\n' + "if not k in data.keys():" +'\n'+"   data[k]=[]"+'\n'+'curdata=['+'\n'+'COLOR,  0, 1, 0,' + '\n' + 'SPHERE,'+ item21+ ','+ item22+',' + item23+','+ "24.4629," +'\n')
		pymfile.write("]"+"\n"+"k='ProteinG geometry'" + '\n' + "if k in data.keys():" + "\n" + "   data[k]= data[k]+curdata"+'\n'+"else:" +'\n' +"   data[k]= curdata"+"\n")

pymfile.write("for k in data.keys():" + "\n" + "   cmd.load_cgo(data[k], k, 1)" +"\n"+ "data= {}")
