# Code was written by Argyris Politis for comparison of low resolution protein complexes
# It is based on the ultrafast algorithm developed by Ballester et al
# Please cite the following papers if use this code: Hall, et al.,Structure,2012 and Politis et al., JMB, 2013 

#  ultrafast code to compare molecular shapes
#import wx
import commands
import re
#import os, numarray
import operator
from operator import itemgetter
from numpy  import *
#from Numeric import *
from math import *
#from Numeric import * # imports numerical python
#from scipy import *
import csv
from scipy.stats import skew, kurtosis

#listmasses=list([11087,11087,11087,11695,11695,11695,60304,60304,60304,43000,43000,43000,29839,29839,29839,25221,25221,25221,21944,21944,21944])
files=commands.getoutput("ls *.mfj")
files=files.split()
#Nstructures=raw_input("enter the number of structures (mfj): ")
#Nstr=int(Nstructures)

Nspheres=raw_input("enter the number of spheres: ")
Nsph=int(Nspheres)

NaverageD=raw_input("enter the average diameter of spheres in the structure: ")
avD=float(NaverageD)

#MassA = raw_input("enter the mass in Da of first type of protein (A): ")
#MA=int(MassA)

#MassB = raw_input("enter the mass in Da of first type of protein (B): ")
#MB=int(MassB)
listnames2=[]
listNames=[]
list10=[]
# This is the native structure that you compare against
for item in files:
	item2=str(item)
        num=(item2.strip("configuration.pymlustermfj"))
        print "num=", num
	listmasses=list([11087,11087,11087,11695,11695,11695,60304,60304,60304,43000,43000,43000,29839,29839,29839,25221,25221,25221,21944,21944,21944])
	InFileName="configuration."+str(num)+".mfj"
	def getRefStruct(InFile):
	       InFile = open(InFileName,'r') # Open file to read
	       InFileLines = InFile.read().splitlines() # string of lines from pdb file
	       InFile.close()
	       print 'file1', InFileName
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
	       for i in range(0, Nsph):
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
	print ctd
	#print ctd[0], ctd[1], ctd[2]

	# getting the first distribution of distances, from centroid to each bead in the strubcture, and store it in a list
	list0 = []
	def getFirstDistribution(lines):
	       for i in range(9,Nsph):
	              D1 = sqrt(pow(ctd[0]-z1[0][i], 2) + pow(ctd[1]-z1[1][i], 2) + pow(ctd[2]-z1[2][i], 2))
	              list0.append(D1)
	       return list0

	fD = getFirstDistribution(getRefStruct(InFileName))


	#$$$ getting the  closest Bead to the centroid

	lo = min(fD)

	idxS1=fD.index(lo)
	#print idxS1

	#% get second Distribution
	list1 = []
	def getSecondDistribution(lines):
	       for i in range(9,Nsph):
	              D2 = sqrt(pow(z1[0][idxS1]-z1[0][i], 2) + pow(z1[1][idxS1]-z1[1][i], 2) + pow(z1[2][idxS1]-z1[2][i], 2))
	              list1.append(D2)
	       return list1


	fD2 = getSecondDistribution(getRefStruct(InFileName))

	#$$$ get farthest Bead to the centroid

	hi = max(fD)
	#print hi

	idxS2=fD.index(hi)

	#% get third Distribution
	list2 = []
	def getThirdDistribution(lines):
	       for i in range(9,Nsph):
	              D3 = sqrt(pow(z1[0][idxS2]-z1[0][i], 2) + pow(z1[1][idxS2]-z1[1][i], 2) + pow(z1[2][idxS2]-z1[2][i], 2))
	              list2.append(D3)
	       return list2


	fD3 = getThirdDistribution(getRefStruct(InFileName))

	hi3 = max(fD3)

	idxS3=fD3.index(hi3)
	#$$$ get farthest Bead from the farthest bead from the centroid


	#% get fourth Distribution
	list3 = []
	def getFourthDistribution(lines):
	       for i in range(9,Nsph):
	              D4 = sqrt(pow(z1[0][idxS3]-z1[0][i], 2) + pow(z1[1][idxS3]-z1[1][i], 2) + pow(z1[2][idxS3]-z1[2][i], 2))
	              list3.append(D4)
	       return list3


	fD4 = getFourthDistribution(getRefStruct(InFileName))
	#print fD4

	# get Mean
	mean1 = mean(fD)
	mean2 = mean(fD2)
	mean3 = mean(fD3)
	mean4 = mean(fD4)
	#print mean1, mean2, mean3, mean4

	# get variance
	var1 = var(fD)
	var2 = var(fD2)
	var3 = var(fD3)
	var4 = var(fD4)
	#print var1, var2, var3, var4

	# get skewness

	sk1 = skew(fD)
	sk2 = skew(fD2)
	sk3 = skew(fD3)
	sk4 = skew(fD4)

	#print sk1, sk2, sk3, sk4
	# get kurtosis
	kur1 = kurtosis(fD)
	kur2 = kurtosis(fD2)
	kur3 = kurtosis(fD3)
	kur4 = kurtosis(fD4)
	#print kur1, kur2, kur3, kur4


	#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


	list0 = []
	list1 = []
	list2 = []
	list3 = []
	list4 = []
	list5 = []
	list6 = []
	#MA = 50000
	#MB = 23000
	#avD = 53.2
	#listNames=[]
	##Read input MFJ files - These are your models that you want to screen against the native structure
	for item in files:
	       item4=str(item)
       	       num=(item4.strip("configuration.pymlustermfj"))
	       InputFileName="configuration."+str(num)+".mfj"
	       #InputFileName="rpn3_cgall.mfj"
	       def ReadFile(InputFile):
	              InputFile = open(InputFileName,'r') # Open file to read
	              InputFileLines = InputFile.read().splitlines() # string of lines from pdb file
	              InputFile.close()
		      print 'file2', InputFileName
	              return InputFileLines

	       def coordinates(lines):
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
	       b= coordinates(ReadFile(InputFileName))



	       def getCent2(lines):
	              outMX2=[]
	              outMY2=[]
	              outMZ2=[]
	              outTotalM2=[]
	              for i in range(0, Nsph):
	                     MX2 = listmasses[i]*b[0][i]
	                     #print MX
	                     MY2 = listmasses[i]*b[1][i]
	                     MZ2 = listmasses[i]*b[2][i]
	                     TotalM2 = listmasses[i]
	                     outMX2.append(MX2)
	                     outMY2.append(MY2)
	                     outMZ2.append(MZ2)
	                     outTotalM2.append(TotalM2)
	                     #print 'totalM=', TotalM2
	              return outMX2, outMY2, outMZ2, outTotalM2       
	       
	       comc2 = getCent2(ReadFile(InputFileName))
	       #print comc[0]

	       def getCentroid2(lines):
	              MX0 = sum(comc2[0])
	              MY0 = sum(comc2[1])
	              MZ0 = sum(comc2[2])
	              TotalM0  =sum(comc2[3])
	              CdX0 = MX0/TotalM0
	              CdY0 = MY0/TotalM0
	              CdZ0 = MZ0/TotalM0
	              print "totalM0=", str(TotalM0)
	              return CdX0, CdY0, CdZ0
	       
	      
	       ctd0 = getCentroid2(ReadFile(InputFileName))
	       #print ctd0[0], ctd0[1], ctd0[2]
	       
	       #linesM0 = getRefStruct(InFileName) 
	       #print linesM0


	       listb0 = []
	       def getFirstDistribution2(lines):
	              for i in range(9,Nsph):
	                     Db1 = sqrt(pow(ctd0[0]-b[0][i], 2) + pow(ctd0[1]-b[1][i], 2) + pow(ctd0[2]-b[2][i], 2))
	                     listb0.append(Db1)
	              return listb0

	       fbD = getFirstDistribution2(ReadFile(InputFileName))
	      # print fbD
	       #$$$ get closest Bead to the centroid

	       #list0.append(fD)
	       #print list0
	       blo = min(fbD)
	       #print blo
	       
	       idxbS1=fbD.index(blo)
	      # print idxbS1

	       #% get second Distribution
	       listb1 = []
	       def getSecondDistribution2(lines):
	              for i in range(9,Nsph):
	                     Db2 = sqrt(pow(b[0][idxbS1]-b[0][i], 2) + pow(b[1][idxbS1]-b[1][i], 2) + pow(b[2][idxbS1]-b[2][i], 2))
	                     listb1.append(Db2)
	              return listb1


	       fbD2 = getSecondDistribution2(ReadFile(InputFileName))
	     #  print fbD2
	       
	       #$$$ get farthest Bead to the centroid
	       #list0.append(fD)
	       #print list0
	       bhi = max(fbD)
	     #  print bhi


	       idxbS2=fbD.index(bhi)
	     #  print idxbS2


	       #% get third Distribution
	       listb2 = []
	       def getThirdDistribution2(lines):
	              for i in range(9,Nsph):
	                     Db3 = sqrt(pow(b[0][idxbS2]-b[0][i], 2) + pow(b[1][idxbS2]-b[1][i], 2) + pow(b[2][idxbS2]-b[2][i], 2))
	                     listb2.append(Db3)
	              return listb2


	       fbD3 = getThirdDistribution2(ReadFile(InputFileName))
	      # print fbD3

	       bhi3 = max(fbD3)
	     #  print bhi3


	       idxbS3=fbD3.index(bhi3)
	      # print idxbS3
	       #$$$ get farthest Bead from the farthest bead from the centroid


	       #% get fourth Distribution
	       listb3 = []
	       def getFourthDistribution2(lines):
	              for i in range(9,Nsph):
	                     Db4 = sqrt(pow(b[0][idxbS3]-b[0][i], 2) + pow(b[1][idxbS3]-b[1][i], 2) + pow(b[2][idxbS3]-b[2][i], 2))
	                     listb3.append(Db4)
	              return listb3


	       fbD4 = getFourthDistribution2(ReadFile(InputFileName))
	     #  print fbD4

	       # get Mean
	       mean10 = mean(fbD)
	       mean20 = mean(fbD2)
	       mean30 = mean(fbD3)
	       mean40 = mean(fbD4)
	      # print mean10, mean20, mean30, mean40

	       # get variance
	       var10 = var(fbD)
	       print "var10=", var10
	       var20 = var(fbD2)
	       var30 = var(fbD3)
	       var40 = var(fbD4)
	     #  print var10, var20, var30, var40

	       # get skewness

	       sk10 = skew(fbD)
	       sk20 = skew(fbD2)
	       sk30 = skew(fbD3)
	       sk40 = skew(fbD4)

	     #  print sk10, sk20, sk30, sk40
	       # get kurtosis
	       kur10 = kurtosis(fbD)
	       kur20 = kurtosis(fbD2)
	       kur30 = kurtosis(fbD3)
	       kur40 = kurtosis(fbD4)
	     #  print kur10, kur20, kur30, kur40
	       
	       m11 = abs(mean10-mean1)/(avD)
	       m12 = abs(mean20-mean2)/(avD)
	       m13 = abs(mean30-mean3)/(avD)
	       m14 = abs(mean40-mean4)/(avD)
	       
	       m21 = abs(var10-var1)/(avD)
	       m22 = abs(var20-var2)/(avD)
	       m23 = abs(var30-var3)/(avD)
	       m24 = abs(var40-var4)/(avD)
	       
	       m31 = abs(sk10-sk1)/(avD)
	       m32 = abs(sk20-sk2)/(avD)
	       m33 = abs(sk30-sk3)/(avD)
	       m34 = abs(sk40-sk4)/(avD)
	       
	       m41 = abs(kur10-kur1)/(avD)
	       m42 = abs(kur20-kur2)/(avD)
	       m43 = abs(kur30-kur3)/(avD)
	       m44 = abs(kur40-kur4)/(avD)
	       
	       #% Calcualte sum of moments
	       #print 'm11=', m11, m12, m13, m14
	       #print 'm21=', m21, m22, m23, m24
	       #print 'm31=', m31, m32, m33, m34
	       #print 'm41=', m41, m42, m43, m44  
	       SM0 = m11+m12+m13+m14+m21+m22+m23+m24+m31+m32+m33+m34+m41+m42+m43+m44
	       SM = float(SM0)
	       print "SM=",SM
	       
	       # Calculates score
	       def getScore(lines, SM):
	       #com1 = 0.2 # expressed 1/Nsph 
	              Ns = float(12)
	              com1 = float(1/Ns)
	              #com1 = pow(float(Nsph), -1)
	              
	              com2 = 0.0625 # is 1/16 where is the 4 momemnts times the 4 distributions
	              scoreN0 = 1+(com1*com2*SM)
	              #scoreN0 = 1*SM
	              score = float(1/scoreN0)
	              return score
	       
	       
	       #scoreN0 = 1+(1/Nsph)*(1/16)*SM
	       #score = 1/scoreN0

	       S= getScore(ReadFile(InputFileName), SM)
	       SF=S
	          
	       
	              
	       listNames.append(InputFileName)
	       listnames2.append(InFileName)
	                                                                    
	       eSM = str(SM)
	       #eSA = str(SA)
	       #eSB = str(SB)
	       eScore=str(SF)
	       list0.append(eSM)
	       list3.append(eScore)
	list10.append(list3)
	      # print list0
	print "Score=", list3

	# This is ths output file - you can rename if you want
	SummaryFileName = 'testingUSR_A.csv'
	SummaryFile = open(SummaryFileName, 'w')
	       #SummaryFile.writerow(["Structre1","Structure2","Score"])
	SummaryFile.write(str(listnames2) +'\n')
	SummaryFile.write(str(listNames) +'\n')
	       #SummaryFile.write(str(list1) +'\n')
	       #SummaryFile.write(str(list2) +'\n')	
        SummaryFile.write(str(list10) +'\n')
	       #SummaryFile.write(str(listOv4) +'\n')
	       #SummaryFile.write(str(listOv5) +'\n')
	       #SummaryFile.write(str(listOv6) +'\n')
	       

SummaryFile.flush()
SummaryFile.close()



        
        
        
