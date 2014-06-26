import csv
import string
import numpy as np

tr = string.maketrans("", "")

fid = open("testingUSR_A.csv")
rdr = csv.reader(fid)

names1 = rdr.next()
names2 = rdr.next()
sims = rdr.next()
fid.close()


names1 = [string.translate(x, tr, "[]' ") for x in names1]
names2 = [string.translate(x, tr, "[]' ") for x in names2]
sims = [string.translate(x, tr, "[]' ") for x in sims]

names1 = [x.split(".")[1] for x in names1]
names2 = [x.split(".")[1] for x in names2]


names = list(set(names1))
names.sort()

qmap = {}
for n1,n2,v in zip(names1, names2, sims):
    qmap[n1 + ":" + n2] = v


fid = open("restructured.csv", "w")

fid.write("," + ",".join(names) + "\n")
for n1 in names:
    fid.write(n1 + ",")
    line = [qmap[n1 + ":" + n2] for n2 in names]
    fid.write(",".join(line) + "\n")

fid.close()



