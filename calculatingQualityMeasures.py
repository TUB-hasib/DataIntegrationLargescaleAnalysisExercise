import pandas as pd
import ast


def createPublicationId(x):
    # id = ast.literal_eval(x)['publicationID'] 
    print(dict(x))
    return x

def calculate():
    
    # reading data for matched entities
    urlErBase = "data/Matched Entities with Brute Force.csv"
    urlErWithBlocking = "data/Matched Entities.csv"

    print("hello")
    dfBase = pd.read_csv(urlErBase)
    dfWithBlocking= pd.read_csv(urlErWithBlocking)

    print(f"no of entities in base : {dfBase.shape[0]}")
    print(f"no of entities with blocking :{dfWithBlocking.shape[0]}")


    # dfCommonRecords = pd.merge(dfBase, dfWithBlocking, on='recordId', how='inner')
    dfCommonRecords = pd.merge(dfBase, dfWithBlocking, on ='recordId', how='inner')

    print(dfCommonRecords)

    duplicates_dfBase = dfBase[dfBase.duplicated(subset='recordId')]
    duplicates_dfWithBlocking = dfWithBlocking[dfWithBlocking.duplicated(subset='recordId')]

    duplicates_dfCommonRecords = dfCommonRecords[dfCommonRecords.duplicated(subset='recordId')]

    print(duplicates_dfBase)
    print(duplicates_dfWithBlocking)

    print(duplicates_dfCommonRecords)






if __name__ == "__main__":
    calculate()
    