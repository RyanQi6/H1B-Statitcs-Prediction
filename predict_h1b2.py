import numpy as np

from sklearn.externals import joblib

#'PREVAILING_WAGE','YEAR','full_time','lat','lon'

#X = np.array([sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5]])



def calculation(X):

    #logistic Regression

    lr = joblib.load("/opt/djangoproject/H1B_DB/H1B_DB/lr.pkl")

    preds_lr = lr.predict_proba(X)



    #random forest

    rfc = joblib.load("/opt/djangoproject/H1B_DB/H1B_DB/rfc.pkl")

    preds_rfc = rfc.predict_proba(X)



    #NN

    nnc = joblib.load("/opt/djangoproject/H1B_DB/H1B_DB/nn.pkl")

    preds_nnc = nnc.predict_proba(X)



    #XGB

    gbc = joblib.load("/opt/djangoproject/H1B_DB/H1B_DB/gbc.pkl")

    preds_gbc = gbc.predict_proba(X)



    #print(statistics.mode([preds_lr, preds_rfc, preds_nnc, preds_gbc]))

    # print((preds_lr + preds_rfc + preds_nnc + preds_gbc)/4)

    ###Results order: rejected, denied. withdraw, certified-withdraw, certified.

    result=np.zeros(shape=(1,5),dtype=float)

    result=(preds_lr + preds_rfc + preds_nnc + preds_gbc)/4



    output=np.zeros(shape=(1,4),dtype=float)

    for i in range(4):

        output[0][i]=result[0][i+1];

    output[0][0]+=result[0][0];

    return output

def printOutput(input):

    print "Given you have got the lottery, the predicted probablity of application CERTIFIED is: ",input[0][3]

    print "Given you have got the lottery, the predicted probablity of application DENIED is: ",input[0][0]

    print "Given you have got the lottery, the predicted probablity of application WITHDRAW is: ",input[0][1]

    print "Given you have got the lottery, the predicted probablity of application CERTIFIED-WITHDRAW is: ",input[0][2]



