# import modules
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# read the dataset
df = pd.read_csv('D:/jupyter/TrainTestDataSet.csv')

# get the locations
x = df.iloc[:, :-1]
y = df.iloc[:, -1]

# split the dataset
x_train, x_test, y_train, y_test = train_test_split(
	x, y, test_size=0.30, random_state=0)

#feature Scaling  
from sklearn.preprocessing import StandardScaler    
st_x= StandardScaler()    
x_train= st_x.fit_transform(x_train)    
x_test= st_x.transform(x_test) 

#Fitting Decision Tree classifier to the training set  
from sklearn.ensemble import RandomForestClassifier  
classifier= RandomForestClassifier(n_estimators= 100, criterion="entropy")  
classifier.fit(x_train, y_train)  

#Predicting the test set result  
y_pred= classifier.predict(x_test) 
print(y_pred)
labels=['Cluster 0','Cluster 1', 'Cluster 2']
#Creating the Confusion matrix  
from sklearn.metrics import confusion_matrix  
cm= confusion_matrix(y_test, y_pred)  
print(cm)

#accuracy Score
acc=accuracy_score(y_test,y_pred)
print(acc)


df2= pd.read_csv('D:/jupyter/clusterData.csv')
ipdata=df2.iloc[:, :-1]
cluslabel=df2.iloc[:,-1]

print(cluslabel)

from sklearn.metrics import silhouette_score

# Assuming you have already computed the cluster labels and assigned them to the 'cluster_labels' variable
silhouette_avg = silhouette_score(ipdata, cluslabel)
print("The average silhouette score is :", silhouette_avg)


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler


X = StandardScaler().fit_transform(ipdata)

# Perform DBSCAN clustering
db = DBSCAN(eps=0.5, min_samples=5)
db.fit(X)

# Visualize the results
labels = db.labels_
print(labels)
unique_labels = set(labels)
colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))

for k, col in zip(unique_labels, colors):
    if k == -1:
        col = 'k'

    class_member_mask = (labels == k)

    xy = X[class_member_mask]
    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col,
             markeredgecolor='k', markersize=6)

plt.title('DBSCAN Clustering')
plt.xlabel('X')
plt.ylabel('Y')
plt.show()

silhouette_avg = silhouette_score(X, labels)
print("The average silhouette db score is :", silhouette_avg)