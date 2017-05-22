import time
import pandas as pd
import ipyparallel
import subprocess


data1 = pd.read_csv('renaloc_data.csv')
data2 = pd.read_csv('bureau_data.csv')


start_cluster_command = 'ipcluster start -n 4'
subprocess.Popen(start_cluster_command)

## Create Cluster to run on multiple nodes

print('Starting Cluster')
for i in range(0,100):
    while True:
        try:
            clients = ipyparallel.Client()
            dview = clients[:]
        except:
            time.sleep(5)
            continue
        break

out = data1.groupby(['commune_ID' , 'localite_ID']).apply(findMatches , data2)

out.to_csv('renaloc_bureau_full.csv')
