import csv
import shutil
Mobcaloutput = '12.out'
eCCS=23417
InputFile = open(Mobcaloutput,'r') # Open file to read
def ReadFile(InputFile):
              InputFileLines = InputFile.read().splitlines() 
              InputFile.close()
              return InputFileLines

m = ReadFile(InputFile)
#print m

ccslist=[]
for item in m:
	if item.startswith(" average PA cross section"): 
		ccslist.append(float(item[28:]))
deltaccsl=[]
percenterrorl=[]
print ccslist
key=open("MFJkey.txt", "r")
keylines=key.read().splitlines()
key.close()
i=0


master_itemlist=[]
for item in ccslist:
	deltaccs=item-eCCS
	percenterror=deltaccs/eCCS*100
	abso=abs(percenterror)
	percenterror='%.2f' % percenterror
	#abso=abs(percenterror)
	itemlist= str(i),str(keylines[i]), str(ccslist[i]), str(deltaccs), str(percenterror), abso
	master_itemlist.append(itemlist)

	i=i+1
top10=298
print master_itemlist
from operator import itemgetter
ms=sorted(master_itemlist, key=itemgetter(5))
with open('ccsscore.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(ms)	 
for n in range(0, 298):
	thefile=ms[n][1]
        shutil.copyfile(thefile, "F/"+ms[n][1])

		

