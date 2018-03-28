
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 03 02:32:10 2017

@author: Vinayak
"""
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.ensemble import RandomForestRegressor,RandomForestClassifier
from sklearn.metrics import mean_squared_error,r2_score,explained_variance_score
from sklearn.metrics import accuracy_score,roc_auc_score,roc_curve,auc,confusion_matrix
from sklearn.cross_validation import train_test_split

""" Ranfom Forest """
X= pd.read_csv('E:/UMN Things/Minne MUDAC/Real Data/Transformed Data/v2/MUDAC_Xtrain.csv',header = None)
del X[67]
y= pd.read_csv('E:/UMN Things/Minne MUDAC/Real Data/Transformed Data/v2/MUDAC_ytrain.csv',header = None)
#y_class = y[0].apply(lambda x: 1 if x>1980.290 else 0)
#x_test = pd.read_csv('E:/UMN Things/Minne MUDAC/Real Data/Transformed Data/MUDAC_Xtest.csv',header = None)


x_train,x_test,y_train,y_test = train_test_split(X,y,test_size = 0.2, random_state = 20)#,stratify = y_class)


rf_model = RandomForestRegressor(n_estimators = 500, min_samples_split = 4, min_samples_leaf = 1, max_features = 'auto',random_state = 20,oob_score=True)
#rf_model = RandomForestClassifier(n_estimators = 500, min_samples_split = 2, min_samples_leaf = 1, max_features = 'auto',random_state = 20)
rf_model.fit(x_train,y_train)

print rf_model.feature_importances_

""" Prediction """
y_pred_train = rf_model.predict(x_train)

y_pred_test = rf_model.predict(x_test)



"""Training Accuracy """
print mean_squared_error(y_train,y_pred_train)
print r2_score(y_train,y_pred_train)
print explained_variance_score(y_train,y_pred_train)

#print accuracy_score(y_train,y_pred_train)
#print roc_auc_score(y_train,y_pred_train)

"""Testing Accuracy """
print mean_squared_error(y_test,y_pred_test)
print r2_score(y_test,y_pred_test)
print explained_variance_score(y_test,y_pred_test)

#print accuracy_score(y_test,y_pred_test)
#print roc_auc_score(y_test,y_pred_test)
y_new = y_test[y_test[0]<1.5e6]
y_pred_new = y_pred_test[y_pred_test<1.0e5]
plt.scatter(y_new,y_pred_new)
del y_new,y_pred_new
