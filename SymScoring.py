#CODE TO CALCULATE SYMMETRY SCORES FOR .MFJ MODELS AND TO MOVE TOP SCORING MODELS TO A NEW FOLDER
#JOSEPH ESCHWEILER, 5/19.2014.

import numpy
import re
#import os, numarray
import operator
from operator import itemgetter
#from numpy  import *
#from Numeric import *
from math import *
#from Numeric import * # imports numerical python
import csv
import commands
import numpy as np
import shutil

##get the files##
files=commands.getoutput("ls *.mfj")
files=files.split()
totalfiles=len(files)
## empty lists to add values to ##

listSym6 = []
listSym7 = []
listSym8 = []

listNames=[]
symlist=[]
##Read input file
for i in files:
       InputFileName=str(i)
       def ReadFile(InputFile):
              InputFile = open(InputFileName,'r') # Open file to read
              InputFileLines = InputFile.read().splitlines() # string of lines from pdb file
              InputFile.close()
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
                     
              return outX, outY, outZ, outR
	    
       b= coordinates(ReadFile(InputFileName))


       XA1=b[0][0]
       XA2=b[0][1]
       XA3=b[0][2]
       XB1=b[0][3]
       XB2=b[0][4]
       XB3=b[0][5]
       XC1=b[0][6]
       XC2=b[0][7]
       XC3=b[0][8]
       XM1=b[0][9]
       XM2=b[0][10]
       XM3=b[0][11]
       XD1=b[0][12]
       XD2=b[0][13]
       XD3=b[0][14]
       XF1=b[0][15]
       XF2=b[0][16]
       XF3=b[0][17]
       XG1=b[0][18]
       XG2=b[0][19]
       XG3=b[0][20]

       YA1=b[1][0]
       YA2=b[1][1]
       YA3=b[1][2]
       YB1=b[1][3]
       YB2=b[1][4]
       YB3=b[1][5]
       YC1=b[1][6]
       YC2=b[1][7]
       YC3=b[1][8]
       YM1=b[1][9]
       YM2=b[1][10]
       YM3=b[1][11]
       YD1=b[1][12]
       YD2=b[1][13]
       YD3=b[1][14]
       YF1=b[1][15]
       YF2=b[1][16]
       YF3=b[1][17]
       YG1=b[1][18]
       YG2=b[1][19]
       YG3=b[1][20]

       ZA1=b[2][0]
       ZA2=b[2][1]
       ZA3=b[2][2]
       ZB1=b[2][3]
       ZB2=b[2][4]
       ZB3=b[2][5]
       ZC1=b[2][6]
       ZC2=b[2][7]
       ZC3=b[2][8]
       ZM1=b[2][9]
       ZM2=b[2][10]
       ZM3=b[2][11]
       ZD1=b[2][12]
       ZD2=b[2][13]
       ZD3=b[2][14]
       ZF1=b[2][15]
       ZF2=b[2][16]
       ZF3=b[2][17]
       ZG1=b[2][18]
       ZG2=b[2][19]
       ZG3=b[2][20]



       def getDistancesAA(lines):
#here the first number is X, Y or Z respectively, the second number is the sphere 1, 2, or 3. 
              DM1M2 = sqrt(pow(XM1-XM2, 2) + pow(YM1-YM2, 2) + pow(ZM1-ZM2, 2))
              DM1M3 = sqrt(pow(XM1-XM3, 2) + pow(YM1-YM3, 2) + pow(ZM1-ZM3, 2))
              DM2M3 = sqrt(pow(XM2-XM3, 2) + pow(YM2-YM3, 2) + pow(ZM2-ZM3, 2))
              
              DD1D2 = sqrt(pow(XD1-XD2, 2) + pow(YD1-YD2, 2) + pow(ZD1-ZD2, 2))
              DD1D3 = sqrt(pow(XD1-XD3, 2) + pow(YD1-YD3, 2) + pow(ZD1-ZD3, 2))
              DD2D3 = sqrt(pow(XD2-XD3, 2) + pow(YD2-YD3, 2) + pow(ZD2-ZD3, 2))
              
              DF1F2 = sqrt(pow(XF1-XF2, 2) + pow(YF1-YF2, 2) + pow(ZF1-ZF2, 2))
              DF1F3 = sqrt(pow(XF1-XF3, 2) + pow(YF1-YF3, 2) + pow(ZF1-ZF3, 2))
              DF2F3 = sqrt(pow(XF2-XF3, 2) + pow(YF2-YF3, 2) + pow(ZF2-ZF3, 2))
              
              DG1G2 = sqrt(pow(XG1-XG2, 2) + pow(YG1-YG2, 2) + pow(ZG1-ZG2, 2))
              DG1G3 = sqrt(pow(XG1-XG3, 2) + pow(YG1-YG3, 2) + pow(ZG1-ZG3, 2))
              DG2G3 = sqrt(pow(XG2-XG3, 2) + pow(YG2-YG3, 2) + pow(ZG2-ZG3, 2))
              

#here we measure distance from the centroid of B. The 3 corresponds to sphere 4 which starts the B's.          
              DM1C0 = sqrt(pow(XM1-((b[0][0]+ b[0][1]+b[0][2])/3), 2) + pow(YM1-((b[1][0]+ b[1][1]+b[1][2])/3), 2) + pow(ZM1-((b[2][0]+ b[2][1]+b[2][2])/3), 2))
              DM2C0 = sqrt(pow(XM2-((b[0][0]+ b[0][1]+b[0][2])/3), 2) + pow(YM2-((b[1][0]+ b[1][1]+b[1][2])/3), 2) + pow(ZM2-((b[2][0]+ b[2][1]+b[2][2])/3), 2))
              DM3C0 = sqrt(pow(XM3-((b[0][0]+ b[0][1]+b[0][2])/3), 2) + pow(YM3-((b[1][0]+ b[1][1]+b[1][2])/3), 2) + pow(ZM3-((b[2][0]+ b[2][1]+b[2][2])/3), 2))

              DD1C0 = sqrt(pow(XD1-((b[0][0]+ b[0][1]+b[0][2])/3), 2) + pow(YD1-((b[1][0]+ b[1][1]+b[1][2])/3), 2) + pow(ZD1-((b[2][0]+ b[2][1]+b[2][2])/3), 2))
              DD2C0 = sqrt(pow(XD2-((b[0][0]+ b[0][1]+b[0][2])/3), 2) + pow(YD2-((b[1][0]+ b[1][1]+b[1][2])/3), 2) + pow(ZD2-((b[2][0]+ b[2][1]+b[2][2])/3), 2))
              DD3C0 = sqrt(pow(XD3-((b[0][0]+ b[0][1]+b[0][2])/3), 2) + pow(YD3-((b[1][0]+ b[1][1]+b[1][2])/3), 2) + pow(ZD3-((b[2][0]+ b[2][1]+b[2][2])/3), 2))

              DF1C0 = sqrt(pow(XF1-((b[0][0]+ b[0][1]+b[0][2])/3), 2) + pow(YF1-((b[1][0]+ b[1][1]+b[1][2])/3), 2) + pow(ZF1-((b[2][0]+ b[2][1]+b[2][2])/3), 2))
              DF2C0 = sqrt(pow(XF2-((b[0][0]+ b[0][1]+b[0][2])/3), 2) + pow(YF2-((b[1][0]+ b[1][1]+b[1][2])/3), 2) + pow(ZF2-((b[2][0]+ b[2][1]+b[2][2])/3), 2))
              DF3C0 = sqrt(pow(XF3-((b[0][0]+ b[0][1]+b[0][2])/3), 2) + pow(YF3-((b[1][0]+ b[1][1]+b[1][2])/3), 2) + pow(ZF3-((b[2][0]+ b[2][1]+b[2][2])/3), 2))

              DG1C0 = sqrt(pow(XG1-((b[0][0]+ b[0][1]+b[0][2])/3), 2) + pow(YG1-((b[1][0]+ b[1][1]+b[1][2])/3), 2) + pow(ZG1-((b[2][0]+ b[2][1]+b[2][2])/3), 2))
              DG2C0 = sqrt(pow(XG2-((b[0][0]+ b[0][1]+b[0][2])/3), 2) + pow(YG2-((b[1][0]+ b[1][1]+b[1][2])/3), 2) + pow(ZG2-((b[2][0]+ b[2][1]+b[2][2])/3), 2))
              DG3C0 = sqrt(pow(XG3-((b[0][0]+ b[0][1]+b[0][2])/3), 2) + pow(YG3-((b[1][0]+ b[1][1]+b[1][2])/3), 2) + pow(ZG3-((b[2][0]+ b[2][1]+b[2][2])/3), 2))
            
              return DM1M2, DM1M3, DM2M3, DM1C0, DM2C0, DM3C0,DD1D2, DD1D3, DD2D3, DD1C0, DD2C0, DD3C0,DF1F2, DF1F3, DF2F3, DF1C0, DF2C0, DF3C0,DG1G2, DG1G3, DG2G3, DG1C0, DG2C0, DG3C0,
              #print DA1A2,DA1A3,DA2A3,DA1B0,DA2B0,DA3B0
	
#now add all the calculated distances to their respective lists##	
       listNames.append(InputFileName)
       c = getDistancesAA(ReadFile(InputFileName))
 
       
       CenterDist_Score = sqrt(pow(c[3]-c[4], 2) + pow(c[4]-c[5], 2)+ pow(c[3]-c[5], 2)) + sqrt(pow(c[10]-c[11], 2) + pow(c[9]-c[10], 2)+ pow(c[9]-c[11], 2)) + sqrt(pow(c[15]-c[16], 2) + pow(c[16]-c[17], 2)+ pow(c[15]-c[17], 2)) + sqrt(pow(c[21]-c[22], 2) + pow(c[21]-c[23], 2)+ pow(c[22]-c[23], 2))

       AlphaDist_Score = sqrt(pow(c[0]-c[1], 2) + pow(c[1]-c[2], 2)+ pow(c[0]-c[2], 2)) + sqrt(pow(c[6]-c[7], 2) + pow(c[7]-c[8], 2)+ pow(c[6]-c[8], 2)) + sqrt(pow(c[12]-c[13], 2) + pow(c[13]-c[14], 2)+ pow(c[12]-c[14], 2)) + sqrt(pow(c[18]-c[19], 2) + pow(c[19]-c[20], 2)+ pow(c[18]-c[20], 2))
       SYMSCORE= CenterDist_Score + AlphaDist_Score

       d6 = str(CenterDist_Score)
       d7 = str(AlphaDist_Score)
       d8 = (SYMSCORE)


       listSym6.append(d6)
       listSym7.append(d7)
       listSym8.append(d8)
       symlist.append([InputFileName, d8])
##write a csv containing all the scores   
       
       #SummaryFileName = 'VolSymscore.csv'
       #SummaryFile = open(SummaryFileName, 'w')
       #SummaryFile.write(str(listNames) +'\n')
       #SummaryFile.write(str(listSym0) +'\n')
       #SummaryFile.write(str(listSym1) +'\n')
       #SummaryFile.write(str(listSym2) +'\n')
       #SummaryFile.write(str(listSym3) +'\n')
       #SummaryFile.write(str(listSym4) +'\n')       
 
       #SummaryFile.write(str(listSym6) +'\n')
       #SummaryFile.write(str(listSym7) +'\n')
       #SummaryFile.write(str(listSym8) +'\n')


## sort the symscores from lowest to highest
array=np.array(listNames)
array1=np.array(listSym8)
array3=np.array([array, array1])
dic={}      
for num in range(0, totalfiles):
	dic[array1[num]]=array[num]

sortedscores=np.sort(array1)
top10=179

sortednames=[]
for item in sortedscores:
	sortednames.append(dic[item])

##take the top 10% of files and put them into a new folder
	
for n in range(0, top10):
	thefile=sortednames[n]
        shutil.copyfile(thefile, "B/"+thefile)

with open("sym.csv", "w") as csvfile:
	writer = csv.writer(csvfile)
	writer.writerows(symlist)

#close the summary file
#SummaryFile.flush()
#SummaryFile.close()



#        with open('ccsscore.csv', 'w') as csvfile:
#    writer = csv.writer(csvfile)
#    writer.writerows(ms)	 

        
        
