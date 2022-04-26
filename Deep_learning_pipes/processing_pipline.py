import pandas as pd
from os import walk


f = []

for (dirpath, dirnames, filenames) in walk("./datasets"):
    f.extend(filenames)
    break

for filename in f:
    csvToDataset = "./datasets/" + filename
    print(csvToDataset)
    df = pd.read_csv(csvToDataset)
    df.drop(df.columns.difference(['date', ' pm10']), 1, inplace=True)
    indexNamespm10 = df[df[' pm10'] == ' '].index
    df.drop(indexNamespm10, inplace=True)
    df[' pm10'] = df[' pm10'].astype('int')
    newCsvName = './processed_datasets/' + filename
    df.to_csv(newCsvName, index=False)

