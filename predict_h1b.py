import numpy as np
from sklearn.externals import joblib

state_name = np.load('state_name.npy')
soc_name = np.load('soc_name.npy')

#'full time','soc_id','state_id','wage'
#X = np.array([sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])
soc_use = int(np.where(soc_name == 'CHIEF EXECUTIVES')[0])
state_use = int(np.where(state_name == 'NEWHAMPSHIRE')[0])
X = np.array([0, soc_use,  state_use, 242674]).reshape((1, 4))

#logistic Regression
lr = joblib.load("lr.pkl")
preds_lr = lr.predict_proba(X)

#NN
nnc = joblib.load("nn.pkl")
preds_nnc = nnc.predict_proba(X)

#print(statistics.mode([preds_lr, preds_rfc, preds_nnc, preds_gbc]))
print((preds_lr + preds_nnc)/2)

