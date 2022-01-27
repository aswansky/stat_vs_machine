# -*- coding: utf-8 -*-
"""
Created on Sat Jan 22 02:46:07 2022

@author: abdal
"""
#reqiued lib
import numpy as np
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import CategoricalNB
from sklearn.tree import DecisionTreeClassifier
data=pd.read_csv(r'D:\Documents\python\advanced data analysis using python\prob\covid.csv')
#convert date variables to dates format
data.entry_date=pd.to_datetime(data.entry_date)
data.date_symptoms=pd.to_datetime(data.date_symptoms, format='%d-%m-%Y')
data=data.replace({99:np.nan})
data=data.replace({98:np.nan})
data=data.dropna(axis=0)
#create the second target variable number of daysbefore death
data['date_symptoms'].replace({'-':'/'})
data['date_died1']=data.date_died[data.date_died !='9999-99-99'] # creat new variable excluding alive that take code 99
data['date_died1']=pd.to_datetime(data.date_died1,format='%d-%m-%Y')# convert the new variable to date
data['days_alive']=data['date_died1']-data['date_symptoms']# calc number of days alive for deads only
data['days_alive1']=data['days_alive']/ np.timedelta64(1, 'D')# converting number of days alive to numbers
data[data['days_alive1']<0]['days_alive1']#check if there are negative values in number of days alive
data.loc[data['days_alive1']<0,'days_alive1'] = 0
data[data['days_alive1']<0]
data.replace({2:0},inplace=True)
data.info()
#create target and related factors
datax=data[['sex','age','patient_type','pneumonia','diabetes','copd','asthma','inmsupr','hypertension','other_disease','cardiovascular','obesity','renal_chronic','tobacco','contact_other_covid']]
data['death']=np.where(np.isnan(data.days_alive1)==True,0,1)
datay=data.death

mod1=CategoricalNB(alpha=.01,fit_prior=False)
mod1.fit(datax,datay).score(datax,datay)
data['predicted1']=mod1.fit(datax,datay).predict(datax)
(data.query("death==1 and predicted1==0").shape[0])/data.shape[0]
data.query("death==0 and predicted1==1").shape[0]
Categorical_accuracy=round(1-(data.query("death==1 and predicted1==0").shape[0])/data.shape[0],2)
Categorical_all_accuracy=round(mod1.fit(datax,datay).score(datax,datay),2)
##CategoricalNB score accuracy 88.9% with 99.7% accuracy for dead category
###logistic
mod2=LogisticRegression(class_weight={0: 1, 1: 9}, max_iter=10000)
mod2.fit(datax,datay).score(datax,datay)
data['predicted2']=mod2.fit(datax,datay).predict(datax)
data.query("death==1 and predicted2==0")
data.query("death==0 and predicted2==1")
logistic_all_accuracy=round(mod2.fit(datax,datay).score(datax,datay),2)
logistic_accuracy=round(1-(data.query("death==1 and predicted2==0").shape[0]/data.shape[0]),2)
###logistic regression score accuracy 92% with 99.4% accuracy for dead category


results={'ordinary logistic':[.92,.82],'discriminat analysis':[.92,.78],'logistic tuned':[logistic_all_accuracy,logistic_accuracy],'Naive Bayes classifier':[Categorical_all_accuracy,Categorical_accuracy]}
df=pd.DataFrame(results)
resultsplot=pd.DataFrame(df.transpose()).plot(kind='bar')
plt.title('accuracy measures for different classification tech ');
plt.legend(['total accuracy','accuracy for dead patients'],bbox_to_anchor=(1.1, 1.05));
plt.ylabel('percent');
plt.xlabel('tech')
resultsplot.set_xticklabels(['ordinary logistic', 'discriminat analysis', 'logistic tuned', 'Naive Bayes classifier'],rotation=15)
for bar in resultsplot.patches:
    value = bar.get_height()
    text = f'{value}'
    text_x = bar.get_x() + bar.get_width() / 2
    text_y = bar.get_y() + value
    resultsplot.text(text_x, text_y, text, ha='center',color='r',size=12)

###decision tree using cart 
mod3 = DecisionTreeClassifier(criterion = "gini", max_leaf_nodes=10).fit(datax,datay)
data['predicted3']=mod3.fit(datax,datay).predict(datax)
data.query("death==1 and predicted3==0")
data.query("death==0 and predicted3==1")
###decision tree using entropy 
mod4 = DecisionTreeClassifier(criterion = "entropy").fit(datax,datay)
data['predicted4']=mod4.fit(datax,datay).predict(datax)
data.query("death==1 and predicted4==0")
data.query("death==0 and predicted4==1")
data.to_csv('file_name.csv')