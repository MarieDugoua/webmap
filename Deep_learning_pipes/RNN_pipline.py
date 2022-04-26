import math
from this import d
import json
import csv
from os import walk

import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from dateutil import rrule
from datetime import datetime, timedelta


def split_dataset(filename):
    df = pd.read_csv(filename)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values(by="date")
    train_set, test_set = np.split(df, [int(.90 * len(df))])
    return train_set, test_set

def RNN_pipline(filenameTrain, filenameTest):
    sc = MinMaxScaler()
    df_Train = pd.read_csv(filenameTrain)
    training_set = df_Train[[' pm10']].values
    training_set_scaled = sc.fit_transform(training_set)
    X_train = []
    y_train = []
    for i in range(365, len(df_Train.index)):
        X_train.append(training_set_scaled[(i-365):i, 0])
        y_train.append(training_set_scaled[i, 0])
    X_train = np.array(X_train)
    y_train = np.array(y_train)
    X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
    regressor = Sequential()

    # Première couche LSTM
    regressor.add(LSTM(units=50,
                       return_sequences=True,
                       input_shape=(X_train.shape[1], 1)))
    regressor.add(Dropout(0.2))  

    # Seconde couche LSTM
    regressor.add(LSTM(units=50, return_sequences=True))
    regressor.add(Dropout(0.2))

    # Troisième couche LSTM
    regressor.add(LSTM(units=50, return_sequences=True))
    regressor.add(Dropout(0.2))

    # Dernière couche LSTM
    regressor.add(LSTM(units=50))
    regressor.add(Dropout(0.2))

    # Couche de sortie
    regressor.add(Dense(units=1))

    # Compilation
    regressor.compile(optimizer="adam", loss="mean_squared_error")

    # Entrainement
    regressor.fit(X_train, y_train, epochs=150, batch_size=32)

    # Evaluation
    df_Test = pd.read_csv(filenameTest)
    true_test_values_set = df_Test[[' pm10']].values
    df_total = pd.concat((df_Train[' pm10'], df_Test[' pm10']), axis=0)
    inputs = df_total[len(df_total) - len(df_Test) - 365:].values
    inputs = inputs.reshape(-1, 1)
    inputs = sc.transform(inputs)

    X_test = []
    for i in range(365, len(inputs)):
        X_test.append(inputs[(i - 365):i, 0])
    X_test = np.array(X_test)
    X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

    predictied_pm = regressor.predict(X_test)
    predictied_pm = sc.inverse_transform(predictied_pm)
    return predictied_pm, true_test_values_set

def visualize(true_test_values_set, prediction, filename):
    # visualisation resultas
    plotPath = './finalPredictedDatasets/plots/' + filename.replace(".csv", ".png")
    city = filename.split('.')[0]
    plt.plot(true_test_values_set, color='red', label='valeurs réelles')
    plt.plot(prediction, color='green', label='valeurs prédites')
    plt.title(f"prédiction de la qualité de l'air à {city}")
    plt.xlabel("jour")
    plt.ylabel("pm10")
    plt.legend()
    plt.savefig(plotPath, bbox_inches='tight')
    plt.clf()

def eval(true_test_values_set, prediction, filename):
    # eval avec RMSE
    rmse = math.sqrt(mean_squared_error(true_test_values_set, prediction))
    dictEval = {'nom' : filename, "scoreRMSE" : rmse}
    field_names = ['nom', 'scoreRMSE']
    with open('./finalPredictedDatasets/evals/allEvals.csv', 'a') as f:
        dictwriter_object = csv.DictWriter(f, fieldnames=field_names)
        dictwriter_object.writerow(dictEval)
        f.close()

def fromPredictDatesDict (filenameTest, prediction):
    df_Test = pd.read_csv(filenameTest)
    firstDayPredicted = df_Test["date"][0]
    firstDayPredicted = datetime.strptime(firstDayPredicted, '%Y-%m-%d')
    lastDayPredicted = df_Test["date"].iloc[-1]
    lastDayPredicted = datetime.strptime(lastDayPredicted, '%Y-%m-%d')

    ListDate = []
    for date in rrule.rrule(rrule.DAILY, dtstart=firstDayPredicted, until=lastDayPredicted):
        ListDate.append(date)
    i = 0
    dict = {}
    for predict in prediction:
         dict[ListDate[i].strftime('%Y-%m-%d')] = predict
         i += 1
    
    return dict
    
def concatDict(trainFile, predDict):
    df_Temp = pd.read_csv(trainFile)
    trainDict = {}
    for i in range(df_Temp.shape[0]):
        trainDict[df_Temp["date"][i]] = int(df_Temp[" pm10"][i])
    
    trainDict.update(predDict)
    return trainDict

def makeCitysDict(metadatasFile):
    df_Temp = pd.read_csv(metadatasFile)
    coordDict = {}
    for i in df_Temp.index:
        coordDict[df_Temp['city'][i]] = [df_Temp['lat'][i].replace('[','').replace(' ',''), df_Temp['long'][i].replace(']','').replace(' ','')]
    return coordDict

def FinalJsonConstr(metadatasdict, datasDict, filename):
    LastDict = {'nom' : filename, 'coords' : metadatasdict[filename], 'datas' : datasDict}

    return LastDict

def prepareDatas(filename, TempCsvTrain, TempCsvTest):
    tempprediction = pd.read_csv(f'./temp_datasets/Predict/{filename}')
    tempprediction['0'] = tempprediction['0'].astype(int)
    prediction = tempprediction['0'].tolist()
    datas = concatDict(TempCsvTrain, fromPredictDatesDict(TempCsvTest, prediction))
    return datas

def produceDatas(filename):
    train_set, test_set = split_dataset(f'./processed_datasets/{filename}')
    TempCsvTrain = './temp_datasets/Train/' + filename
    TempCsvTest = './temp_datasets/Test/' + filename
    train_set.to_csv(TempCsvTrain, index=False)
    test_set.to_csv(TempCsvTest, index=False)
    prediction, true_test_values_set = RNN_pipline(TempCsvTrain, TempCsvTest)
    TempCsvPred = './temp_datasets/Predict/' + filename
    df_pred = pd.DataFrame(prediction)
    df_pred.to_csv(TempCsvPred, index=False)
    datas = prepareDatas(filename, TempCsvTrain, TempCsvTest)
    eval(true_test_values_set, prediction, filename)
    visualize(true_test_values_set, prediction, filename)
    return datas

cityDict = makeCitysDict('./metadataset_coord.csv') 

# datas = produceDatas('chambery_le haut.csv')

# finalDict = FinalJsonConstr(cityDict, datas, 'chambery_le haut.csv')


# with open('./finalPredictedDatasets/data_test.json', 'w') as fp:
#      json.dump(finalDict, fp, default=str, indent=4)

listFiles = []

for (dirpath, dirnames, filenames) in walk("./processed_datasets"):
    listFiles.extend(filenames)
    break

for filename in listFiles:
    print(f'Current file : {filename}')
    datas = produceDatas(filename)
    finalDict = FinalJsonConstr(cityDict, datas, filename)
    jsonFilename = filename.replace(".csv", ".json")
    with open(f'./finalPredictedDatasets/{jsonFilename}', 'w') as fp:
        json.dump(finalDict, fp, default=str, indent=4)