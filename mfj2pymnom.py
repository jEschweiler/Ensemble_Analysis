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

for item in files:
	item2=str(item)
        num=(item2.strip("configuration.pymlustermfj"))
	pymfilename="configuration"+num+".pym"
	pymfile=open(pymfilename, "w")
	pymfile.write('from pymol.cgo import *'+ '\n')
	pymfile.write('from pymol import cmd'+ '\n')
	pymfile.write('from pymol.vfont import plain' + '\n' + 'data={}' + '\n' + "curdata=[]" + '\n')

        #print "num=", num
	#listmasses=list([11087,11087,11087,11695,11695,11695,60304,60304,60304,43000,43000,43000,29839,29839,29839,25221,25221,25221,21944,21944,21944])
	InFileName="configuration."+str(num)+".mfj"
	def getRefStruct(InFile):
	       InFile = open(InFileName,'r') # Open file to read
	       lines = InFile.read().splitlines() # string of lines from pdb file
	       InFile.close()
	       return lines
	z1= getRefStruct(item)
	print z1
	def getCoords(lines):
	              outX=[]
	              outY=[]
	              outZ=[]
	              outR=[]
		      print
	              for i in lines[6:9]:
	                     l = re.findall ("(\S+)", i)
			     print "L=", l
	                     X0 = str(l[0])
			     print "X=", X0
	                     Y0 = str(l[1])
	                     Z0 = str(l[2])
	                     R0 = str(l[3])
			     pymfile.write("k='ProteinA geometry'" +'\n' + "if not k in data.keys():" +'\n'+"   data[k]=[]"+'\n'+'curdata=['+'\n'+'COLOR,  0,.6, .6,' + '\n' + 'SPHERE,'+ X0+ ','+ Y0+',' + Z0+','+ "20.3245," +'\n')
		             pymfile.write("]"+"\n"+"k='ProteinA geometry'" + '\n' + "if k in data.keys():" + "\n" + "   data[k]= data[k]+curdata"+'\n'+"else:" +'\n' +"   data[k]= curdata"+"\n")
		      for i in lines[9:12]:
	                     l = re.findall ("(\S+)", i)
	                     X0 = str(l[0])
	                     Y0 = str(l[1])
	                     Z0 = str(l[2])
	                     R0 = str(l[3])
			     pymfile.write("k='ProteinA geometry'" +'\n' + "if not k in data.keys():" +'\n'+"   data[k]=[]"+'\n'+'curdata=['+'\n'+'COLOR,  1,0,.5,' + '\n' + 'SPHERE,'+ X0+ ','+ Y0+',' + Z0+','+ "18.4662," +'\n')
		             pymfile.write("]"+"\n"+"k='ProteinA geometry'" + '\n' + "if k in data.keys():" + "\n" + "   data[k]= data[k]+curdata"+'\n'+"else:" +'\n' +"   data[k]= curdata"+"\n")
	              for i in lines[12:15]:
	                     l = re.findall ("(\S+)", i)
	                     X0 = str(l[0])
	                     Y0 = str(l[1])
	                     Z0 = str(l[2])
	                     R0 = str(l[3])
			     pymfile.write("k='ProteinA geometry'" +'\n' + "if not k in data.keys():" +'\n'+"   data[k]=[]"+'\n'+'curdata=['+'\n'+'COLOR,  1, 1, .2,' + '\n' + 'SPHERE,'+ X0+ ','+ Y0+',' + Z0+','+ "34.7381," +'\n')
		             pymfile.write("]"+"\n"+"k='ProteinA geometry'" + '\n' + "if k in data.keys():" + "\n" + "   data[k]= data[k]+curdata"+'\n'+"else:" +'\n' +"   data[k]= curdata"+"\n")    

#		      for i in lines[15:18]:
#	                     l = re.findall ("(\S+)", i)
#	                     X0 = str(l[0])
#	                     Y0 = str(l[1])
#	                     Z0 = str(l[2])
#	                     R0 = str(l[3])
#			     pymfile.write("k='ProteinA geometry'" +'\n' + "if not k in data.keys():" +'\n'+"   data[k]=[]"+'\n'+'curdata=['+'\n'+'COLOR,  0.8, .4, 0,' + '\n' + 'SPHERE,'+ X0+ ','+ Y0+',' + Z0+','+ "30.5044," +'\n')
#		             pymfile.write("]"+"\n"+"k='ProteinA geometry'" + '\n' + "if k in data.keys():" + "\n" + "   data[k]= data[k]+curdata"+'\n'+"else:" +'\n' +"   data[k]= curdata"+"\n")	
		      for i in lines[18:21]:
	                     l = re.findall ("(\S+)", i)
	                     X0 = str(l[0])
	                     Y0 = str(l[1])
	                     Z0 = str(l[2])
	                     R0 = str(l[3])
			     pymfile.write("k='ProteinA geometry'" +'\n' + "if not k in data.keys():" +'\n'+"   data[k]=[]"+'\n'+'curdata=['+'\n'+'COLOR,  .6, 1, 1,' + '\n' + 'SPHERE,'+ X0+ ','+ Y0+',' + Z0+','+ "26.8763," +'\n')
		             pymfile.write("]"+"\n"+"k='ProteinA geometry'" + '\n' + "if k in data.keys():" + "\n" + "   data[k]= data[k]+curdata"+'\n'+"else:" +'\n' +"   data[k]= curdata"+"\n")

		      for i in lines[21:24]:
	                     l = re.findall ("(\S+)", i)
	                     X0 = str(l[0])
	                     Y0 = str(l[1])
	                     Z0 = str(l[2])
	                     R0 = str(l[3])
			     pymfile.write("k='ProteinA geometry'" +'\n' + "if not k in data.keys():" +'\n'+"   data[k]=[]"+'\n'+'curdata=['+'\n'+'COLOR,  0.8, 0, 0.8,' + '\n' + 'SPHERE,'+ X0+ ','+ Y0+',' + Z0+','+ "24.4043," +'\n')
		             pymfile.write("]"+"\n"+"k='ProteinA geometry'" + '\n' + "if k in data.keys():" + "\n" + "   data[k]= data[k]+curdata"+'\n'+"else:" +'\n' +"   data[k]= curdata"+"\n")

		      for i in lines[24:27]:
	                     l = re.findall ("(\S+)", i)
	                     X0 = str(l[0])
	                     Y0 = str(l[1])
	                     Z0 = str(l[2])
	                     R0 = str(l[3])
			     pymfile.write("k='ProteinA geometry'" +'\n' + "if not k in data.keys():" +'\n'+"   data[k]=[]"+'\n'+'curdata=['+'\n'+'COLOR,  0, 1, 0,' + '\n' + 'SPHERE,'+ X0+ ','+ Y0+',' + Z0+','+ "24.4629," +'\n')
		             pymfile.write("]"+"\n"+"k='ProteinA geometry'" + '\n' + "if k in data.keys():" + "\n" + "   data[k]= data[k]+curdata"+'\n'+"else:" +'\n' +"   data[k]= curdata"+"\n")

		


		      pymfile.write("for k in data.keys():" + "\n" + "   cmd.load_cgo(data[k], k, 1)" +"\n"+ "data= {}")
		      pymfile.close()

	getCoords(z1)
