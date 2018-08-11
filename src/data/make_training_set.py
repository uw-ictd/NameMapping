import pandas as pd
import data.metrics as metrics

renaloc = pd.read_csv('../data/raw/renaloc_data.csv', encoding = "ISO-8859-1")
bureau = pd.read_csv('../data/raw/bureau_data.csv', encoding = "ISO-8859-1")

pairs_renaloc_bureau = metrics.make_pairs(renaloc, bureau)
metrics_renaloc_bureau = metrics.make_pairs_distances(pairs_renaloc_bureau)
metrics_renaloc_bureau.to_csv('../data/metrics_renaloc_bureau.csv')

############# Sampling

def sample_training(data, size_chunk):
    n = min(len(data), size_chunk)
    out = data.sample(n, replace =False)
    return out

# Initial drawing
training_set_renaloc_bureau = metrics_renaloc_bureau.groupby(['levenshtein_dist', 'sound']).apply(sample_training,15)


## reading current sample
training_set_renaloc_bureau = pd.read_excel('../data/training_set.xls')

## Updating the metrics
training_set_renaloc_bureau  = metrics_renaloc_bureau.merge(training_set_renaloc_bureau, left_on = ['commune_ID', 'name_1', 'name_2'], right_on = ['commune_ID', 'list_1', 'list_2'] , how='right' , suffixes = ["", "-y"])
training_set_renaloc_bureau = training_set_renaloc_bureau[metrics_renaloc_bureau.columns.tolist() + ['match']]

training_set_renaloc_bureau.to_csv('../data/training_set.csv')
