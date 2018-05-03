import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import kde
%matplotlib inline

dat = pd.read_csv('match_less_90.csv', encoding =  "ISO-8859-1",sep=';')

matched = dat[dat.Match == True]

values = np.vstack([matched.distance, matched.name_distance])
k = kde.gaussian_kde(values)
nbins = 20
xi, yi = np.mgrid[matched.distance.min():matched.distance.max():nbins*1j, matched.name_distance.min():matched.name_distance.max():nbins*1j]
zi = k(np.vstack([xi.flatten(), yi.flatten()]))
plt.pcolormesh(xi, yi, zi.reshape(xi.shape), shading='gouraud', cmap = 'YlOrBr') ;


plt.hist2d(matched.distance, matched.name_distance) ;
