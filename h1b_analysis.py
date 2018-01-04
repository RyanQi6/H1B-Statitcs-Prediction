import csv
import numpy as np
import pandas as pd
import time
import random
from sklearn import preprocessing
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn import neighbors as nb
from sklearn import neural_network as nn
from sklearn.ensemble import GradientBoostingClassifier
#import pickle
from sklearn.externals import joblib
import re

#data processing
print('data processing')
t1 = time.time()
df = pd.read_csv('h1b_kaggle.csv')
## simply remove rows with NAs
df = df.dropna()
pending = np.where(df['CASE_STATUS'] =='PENDING QUALITY AND COMPLIANCE REVIEW - UNASSIGNED')
df = df.drop(df.index[pending])
invalidated = np.where(df['CASE_STATUS'] == 'INVALIDATED')
df = df.drop(df.index[invalidated])
#soc_all = list(np.unique(list(df['SOC_NAME'])))[0:11]
#for name in soc_all:
#    soc_pos = np.where(df['SOC_NAME'] == name)
#    df = df.drop(df.index[soc_pos])

status = list(df['CASE_STATUS'])
employer = list(df['EMPLOYER_NAME'])
soc = list(df['SOC_NAME'])
soc = np.asarray([soc[i].upper() for i in range(len(soc))])

for name in np.unique(soc)[0:11]:
    soc[np.where(soc == name)] = 'OTHER'

name, counts = np.unique(soc,return_counts=True)
name_xiaoyu_500 = name[np.where(counts < 500)]
for name in name_xiaoyu_500:
    soc[np.where(soc == name)] = 'OTHER'

# temp = soc
# for l in range(len(temp)):
#     temp[l] = re.sub(",|;|:|&|AND", " ",temp[l])
#     temp[l] = re.sub(' +',' ', temp[l])
#     if temp[l][-1].upper() == 'S':
#         temp[l] = temp[l][0:(len(temp[l])-1)]


soc_name, soc_id = np.unique(soc, return_inverse=True)
job = list(df['JOB_TITLE'])
full_time = list(df['FULL_TIME_POSITION'])
wage = list(df['PREVAILING_WAGE'])
year = list(df['YEAR']); year = [int(i) for i in year]
state = [x.split(',')[1].replace(" ","") for x in list(df['WORKSITE'])]
state_name, state_id = np.unique(state, return_inverse=True)
longitude = list(df['lon'])
latitude = list(df['lat'])

# company = list(df['EMPLOYER_NAME'])
# company = np.asarray([company[i].upper() for i in range(len(company))])
# for name in np.unique(company):
#     if len(name.split()) >= 5:
#         company[np.where(company == name)] = ' '.join(name.split()[0:5])


np.save('state_name.npy', state_name)
np.save('soc_name.npy', soc_name)


result = []
full = []
for i in range(df.shape[0]):
    if status[i] == 'REJECTED':
        result.append(0)
    elif status[i] == 'DENIED':
        result.append(1)
    elif status[i] == 'WITHDRAWN':
        result.append(2)
    elif status[i] == 'CERTIFIED-WITHDRAWN':
        result.append(3)
    elif status[i] == 'CERTIFIED':
        result.append(4)
    if full_time == 'Y':
        full.append(1)
    else:
        full.append(0)

#The final data in use:
#X = pd.DataFrame({'wage': wage, 'lon': longitude, 'lat': latitude, 'full_time': full, 'soc_name': soc_name, 'state':state})
X = pd.DataFrame({'wage': wage, 'full_time': full, 'soc_id': soc_id, 'state_id': state_id})
#X = pd.DataFrame({'wage': wage})
X['soc_id'] = X['soc_id'].astype('category')
X['state_id'] = X['state_id'].astype('category')
X['full_time'] = X['full_time'].astype('category')
y = pd.DataFrame()
y['STATUS'] = result

#separate the data into training and testing
train_ratio = 0.8; random.seed(123)
n, p = df.shape #28777491
train_size = int(n*train_ratio)
test_size = n-train_size
index = random.sample(range(2877749), 2877749)
train_index = index[0:train_size]
test_index = index[train_size:len(index)+1]
X_train = X.loc[train_index]
X_test = X.loc[test_index]
Y_train = y.loc[train_index]
Y_test = y.loc[test_index]

t2 = time.time()
print('data processing take time: ', t2-t1, 's')

#train data and test result


t3 = time.time()
#logistic regression
print('train and test: logistic regression')
lr = LogisticRegression()
lr.fit(X_train, np.ravel(Y_train))
preds_lr = lr.predict(X_train)
train_y_array = np.array(Y_train)
pred_train = float(sum(np.equal(train_y_array[:, 0], preds_lr)))/float(len(train_index))
print('training error of logistic regression: ', pred_train) #0.873503550301
preds_lr_test = lr.predict(X_test)
test_y_array = np.array(Y_test)
pred_test = float(sum(np.equal(test_y_array[:, 0], preds_lr_test)))/float(len(test_index))
print('testing error of logistic regression: ', pred_test) #0.873046651029
t4 = time.time()
print('logistic regression use time: ', t4-t3, 's')
#filename = 'rfc.sav'
#pickle.dump(rfc, open(filename, 'wb'))
lr = LogisticRegression()
lr.fit(X, np.ravel(y))
joblib_file = "lr.pkl"
joblib.dump(lr, joblib_file)

# load the model from disk
# loaded_model = pickle.load(open(filename, 'rb'))
# result = loaded_model.score(X_test, Y_test)
# print(result)


#NN
nnc = nn.MLPClassifier(activation='tanh',hidden_layer_sizes=(150,))
nnc.fit(X_train, np.ravel(Y_train))
preds_nnc = nnc.predict(X_train)
train_y_array = np.array(Y_train)
pred_train = float(sum(np.equal(train_y_array[:,0], preds_nnc)))/float(len(train_index))
print('training error of NN: ', pred_train) #0.873160834489
preds_nnc = nnc.predict(X_test)
train_y_array = np.array(Y_test)
pred_test = float(sum(np.equal(train_y_array[:,0], preds_nnc)))/float(len(test_index))
print('test error of NN: ', pred_test) #0.872129267657
t7 = time.time()
print('neural network use time: ', t7-t6, 's')
#filename = 'NN.sav'
#pickle.dump(nnc, open(filename, 'wb'))
nnc = nn.MLPClassifier(activation='tanh',hidden_layer_sizes=(150,))
nnc.fit(X, np.ravel(y))
joblib_file = "nn.pkl"
joblib.dump(nnc, joblib_file)






















#XGB
gbc = GradientBoostingClassifier(n_estimators=50, max_depth=4, learning_rate=0.05)
gbc.fit(X_train, np.ravel(Y_train))
preds_gbc = gbc.predict(X_train)
train_y_array = np.array(Y_train)
pred_train = float(sum(np.equal(train_y_array[:,0], preds_gbc)))/float(len(train_index))
print('training error of boosting tree: ', pred_train)
preds_gbc = gbc.predict(X_test)
train_y_array = np.array(Y_test)
pred_test = float(sum(np.equal(train_y_array[:,0], preds_gbc)))/float(len(test_index))
print('training error of boosting tree: ', pred_test)
t8 = time.time()
print('XG boosting tree use time: ', t8-t7, 's')
#filename = 'gbc.sav'
#pickle.dump(gbc, open(filename, 'wb'))
joblib_file = "gbc.pkl"
joblib.dump(gbc, joblib_file)

#random forest
rfc = RandomForestClassifier(n_estimators=100, max_depth=5)
rfc.fit(X_train, np.ravel(Y_train))
preds_rfc = lr.predict(X_train)
train_y_array = np.array(Y_train)
pred_train = sum(np.equal(train_y_array[:,0], preds_rfc))/len(train_index)
print('training error of random forest: ', pred_train) #0.87361214213
preds_rfc = rfc.predict(X_test)
train_y_array = np.array(Y_test)
pred_test = sum(np.equal(train_y_array[:,0], preds_rfc))/len(test_index)
print('training error of random forest: ', pred_test) #0.872838154808
t5 = time.time()
print('random forest use time: ', t5-t4, 's')
#filename = 'rfc.sav'
#pickle.dump(rfc, open(filename, 'wb'))
joblib_file = "rfc.pkl"
joblib.dump(rfc, joblib_file)

#KNN
knc = nb.KNeighborsClassifier(n_neighbors=100)
knc.fit(X_train, np.ravel(Y_train))
preds_knc = knc.predict(X_train)
train_y_array = np.array(Y_train)
pred_train = sum(np.equal(train_y_array[:,0], preds_knc))/len(train_index)
print('training error of KNN: ', pred_train) #0.876431620377
preds_knc = knc.predict(X_test)
train_y_array = np.array(Y_test)
pred_test = sum(np.equal(train_y_array[:,0], preds_knc))/len(test_index)
print('training error of KNN: ', pred_test) # 0.875400920858
t6 = time.time()
print('KNN use time: ', t6-t5, 's')
#filename = 'knc.sav'
#pickle.dump(knc, open(filename, 'wb'))
joblib_file = "knc.pkl"
joblib.dump(knc, joblib_file)