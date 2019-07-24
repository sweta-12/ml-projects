import pandas as pd
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
import pickle
import os

def pre_proc(df):
    def get_title(name):
        if '.' in name:
            return name.split(',')[1].split('.')[0].strip()
        else:
            return 'Unknown'
    def title_map(title):
        if title in ['Mr']:
            return 1
        elif title in ['Master']:
            return 3
        elif title in ['Ms','Mlle','Miss']:
            return 4
        elif title in ['Mme','Mrs']:
            return 5
        else:
            return 2

    df['title'] = df['Name'].apply(get_title).apply(title_map)   
    df = df.drop(["PassengerId", "Name", "Ticket"], axis="columns")
    df["Sex"] = df["Sex"].replace(["male", "female"], [0, 1])
    df["Cabin"] = df["Cabin"].isna()
    df = pd.get_dummies(df)
    df["Age"][df["Age"].isna()] = df["Age"].mean()
    mf = df['Fare'].mean()
    df['Fare'] = df['Fare']>mf
    df['Fare'] = df['Fare'].astype(int)
    return df    


def training(df):
    df = pre_proc(df)
    y = df["Survived"]
    df.drop("Survived", axis="columns", inplace=True)
    X = df
    
    dummyRow = pd.DataFrame(np.zeros(len(X.columns)).reshape(1, len(X.columns)), columns=X.columns)    
    dummyRow.to_csv("dummyRow.csv", index=False)
    
    model = XGBClassifier(max_depth=2, min_child_weight= 3, gamma=0, 
                     subsample=0.86, reg_alpha=0, n_estimators=125)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=11)
#     model.fit(X_train, y_train)
    model.fit(X, y)
    
    pkl_filename = "pickle_model.pkl"
    with open(pkl_filename, 'wb') as file:
        pickle.dump(model, file)

    print(model.score(X,y))
    yp = model.predict(X_test)
    print("Sur", sum(yp!=0))
    print("Not Sur", sum(yp==0))
    cm = confusion_matrix(y_test, yp)
    print(cm)    

def pred(ob):
    d1 = ob.to_dict()
    df = pd.DataFrame(d1, index=[0])
    df.drop("Survived", axis="columns", inplace=True)    
    df = pre_proc(df)    
    dummyrow_filename = "dummyRow.csv"
    dummyrow_filename = os.path.dirname(__file__) + "/" + dummyrow_filename    
    df2 = pd.read_csv(dummyrow_filename)    
    for c1 in df.columns:
        df2[c1] = df[c1]
    pkl_filename = "pickle_model.pkl"
    pkl_filename = os.path.dirname(__file__) + "/" + pkl_filename
    with open(pkl_filename, 'rb') as file:
        model = pickle.load(file)
    pred = model.predict(df2)
    return pred
                


if __name__ == "__main__":
    df = pd.read_csv("titanic.csv")     
    training(df)