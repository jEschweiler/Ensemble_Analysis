import commands
import operator 
from operator import itemgetter
import re
import numpy as np
import sys

files=commands.getoutput("ls *.mfj")
files=files.split()
num=len(files)
num=str(num)
master_output=open("master_output.mfj", "w")
master_output.write("master_output.mfj" + "\n" + num + "\n" + "21" + "\n" + 'ang' + "\n" + "none" + "\n" + "1.0000" + "\n")
Key=open("MFJkey.txt", "w")

for item in files:
	       InFile = open(item,'r') # Open file to read
	       InFileLines = InFile.read().splitlines() # string of lines from pdb file
	       InFile.close()
	       outX=[]
	       outY=[]
	       outZ=[]
	       outR=[]
	       for i in InFileLines[6:]:
	              l = re.findall ("(\S+)", i)
		      #print l
	              X0 = str(l[0])
	              Y0 = str(l[1])
	              Z0 = str(l[2])
	              R0 = float(l[3])
		      R0 = round(R0, 0)
		      R0 = int(R0)
		      R0 = str(R0)
	              #outX.append(X0)
	              #outY.append(Y0)
	              #outZ.append(Z0)
	              #outR.append(R0)
	              #print Scr2
	              #return outX, outY, outZ, outR
		      master_output.write("      "+ X0 + "       " + Y0 + "       " + Z0 + "   " + R0 + "      " +"0.0000" + "\n")

	       master_output.write("21" + "\n")
	       Key.write(str(item) + '\n')
