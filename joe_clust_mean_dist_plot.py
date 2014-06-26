import numpy as np
import scipy.spatial.distance as dist
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
import scipy.cluster.hierarchy as clust


pdf = PdfPages("joe_plots.pdf")

# Read the pairwise distance matrix (discard row and column labels).
fname = "restructured.csv"
distmat = np.loadtxt(fname, delimiter=",", skiprows=1)
distmat = distmat[:,1:]

# Calculate the mean of the pairwise similarities.
ii = np.tril_indices(distmat.shape[0], -1)
pwise = distmat[ii]
mdist = np.mean(pwise)
print mdist

# Generate a historgram of the pairwise similarities.
plt.clf()
plt.hist(pwise, 20, color='lightblue')
plt.xlabel("Similarity", size=17)
plt.ylabel("Frequency", size=17)
pdf.savefig()


# Do the clustering
h = clust.average(distmat)
print h
print len(h)

# Plot the dendrogram
plt.figure(figsize=(16,10))
#plt.figure(linewidth=100)
plt.clf()
ax = plt.axes()
for pos in 'right','bottom','top':
    ax.spines[pos].set_color('none')
ax.xaxis.set_ticks_position('none')
ax.yaxis.set_ticks_position('none')
#ax.spines['left'].set_position(('outward', 10))
clust.dendrogram(h, get_leaves="true", count_sort="true",show_leaf_counts="false", color_threshold=1.5)
#no_labels="true")
l=clust.leaves_list(h)
print l
print len(l)
pdf.savefig()

pdf.close()
