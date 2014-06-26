import sys
import os
import commands
import shutil
import re

#numbers=open("numberslist.txt", "r")
#list_of_numbers=numbers.str.splitlines()
#list_of_numbers=list(numbers.splitlines())
#list_of_numbers.strip()
#print list_of_numbers
with open("numbers2.txt") as f:
    numbers=f.read().split()
print numbers
print len(numbers)
files=commands.getoutput("ls *.mfj")
files=files.split()
print files

numbers = [ int(x) for x in numbers ]
for item in numbers:
    fil=files[item]
    print fil
    item3=str(fil)
    num=(item3.strip("configuration.pymlustermfj"))
    num=int(num)
    item=str(num)
    #print num
    shutil.copyfile(fil, "mod.large/configuration."+item+".mfj")
