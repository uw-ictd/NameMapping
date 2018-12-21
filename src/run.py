import pandas as pd
%matplotlib inline
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn import tree, svm
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
import graphviz
import matplotlib.pyplot as plt

training_set_renaloc_bureau = pd.read_csv('../data/training_set.csv')
## Take out only parenthesis
## Take out word inn parenthesis
## Take out roman number
## Remove all
## One is subset of the other


variables = ['jaro_dist_clean', 'levenshtein_dist',  'sound']

## MODEL BUILDING AND SELECTION

X = training_set_renaloc_bureau.drop("match" , axis =1)
y = training_set_renaloc_bureau["match"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4)

X_train_dat, X_test_dat = X_train[variables] , X_test[variables]


treereg = tree.DecisionTreeClassifier(max_depth = 3, criterion = 'gini')
r_tree  = treereg.fit(X_train_dat, y_train)
treereg.score(X_test_dat, y_test)
scores = cross_val_score(treereg, X[variables], y, cv=5, scoring='f1_macro')
print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))

clf = svm.SVC(kernel='linear', C=3, probability = True)
clf_f = clf.fit(X_train_dat, y_train)
scores = cross_val_score(clf, X[variables], y, cv=5, scoring='f1_macro')
print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))

forest = RandomForestClassifier(n_estimators=10)
forest_f = forest.fit(X_train_dat, y_train)
scores = cross_val_score(forest, X[variables], y, cv=5, scoring='f1_macro')
print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))


models=  {'tree':r_tree, 'clf':clf_f, 'forest':forest_f}

def group_predictions(X_test, models, variables):
    for i in models.keys():
        X_test.loc[:,i] = list(pd.DataFrame(models[i].predict_proba(X_test[variables]))[1])
    return X_test

sout = group_predictions(X_test_dat, models, variables)


## PPN / NPV -> Threshold optimization
def predict_threshold(predict_proba, threshold):
    predict = predict_proba > threshold
    return predict

X_train_2, X_test_2, y_train_2, y_test_2 = train_test_split(sout[list(models.keys())], y_test, test_size=0.4, random_state=2)



treereg = tree.DecisionTreeClassifier(max_depth = 3, criterion = 'gini')
r_tree  = treereg.fit(X_train_2, y_train_2)
treereg.score(X_test_2, y_test_2)
scores = cross_val_score(r_tree, sout[list(models.keys())], y_test, cv=5, scoring='f1_macro')
print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))

clf = svm.SVC(kernel='linear', C=3, probability = True)
clf_f = clf.fit(X_train_2, y_train_2)
clf_f.score(X_test_2, y_test_2)
scores = cross_val_score(clf, sout[list(models.keys())], y_test, cv=5, scoring='f1_macro')
print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))

forest = RandomForestClassifier(n_estimators=10)
forest_f = forest.fit(X_train_2, y_train_2)
forest_f.score(X_test_2, y_test_2)
scores = cross_val_score(forest, sout[list(models.keys())], y_test, cv=5, scoring='f1_macro')
print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))

### THRESHOLDING => look at distrib in both positives and negatives false and true


sout = sout.merge(pd.DataFrame(y_test), left_index = True ,right_index = True)



plt.subplot(221)
plt.hist(sout[sout.match == True].tree, histtype = 'step', normed=True);
plt.hist(sout[sout.match == False].tree, histtype = 'step', normed=True);
plt.subplot(222)
plt.hist(sout.clf[sout.match == True], histtype = 'step', normed=True);
plt.hist(sout.clf[sout.match == False], histtype = 'step', normed=True);
plt.subplot(223)
plt.hist(sout.forest[sout.match == True], histtype = 'step', normed=True);
plt.hist(sout.forest[sout.match == False], histtype = 'step', normed=True);

def get_certainty_zone(labelled_metrics, models, alpha):
    model_names = models.keys()
    for m in models:
        p = 1
        while (sum(labelled_metrics.match[labelled_metrics[m] < p] == True) >0) and (p > 0):
            p = p - .05
        print(m + ' : ' + str(p))

get_certainty_zone(sout, models, .02)

sum((sout.tree < .1))

len(sout[(sout.clf < .15) | (sout.tree < .1) | (sout.forest < 0)])


sout_mix = sout[(sout.clf > .15) & (sout.tree > .1) & (sout.forest > 0)]

sum(sout_mix.match)

dat = pd.read_csv('../data/metrics_renaloc_bureau.csv')

dat.dropna(inplace=True)

dat.head()

r_tree.classes_

dat[variables].shape

pre = r_tree.predict(dat[variables])

print(sum(pre))




tree_full = pd.DataFrame(
dat.loc[0:1000, variables]))
tree_full



sout_mix.merge(X[['name_1','name_2']], left_index = True, right_index = True)


## Ranking matches both sides / validate first wave

def rank_matches(model, X_test, variables):
    X_test_dat = X_test[variables]
    predicted = model.predict(X_test_dat)
    X_test['predict'] = predicted
    return X_test


rank_matches(r_tree, X_test,variables)

## PROCEDURAL MATCH
