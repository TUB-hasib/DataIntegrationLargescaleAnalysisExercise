import pandas as pd
from pprint import pprint
from sklearn.metrics import jaccard_score
from nltk.metrics import jaccard_distance



# Data Integration and Machine Learning: A Natural Synergy
# https://dl.acm.org/doi/10.1145/3292500.3332296
# Learning-based Methods with Human-in-the-loop for Entity Resolution
# https://ertutorial-arc.github.io/


# adding record from dataframe to bucketDict based on the key for blocking stage. 
def createBlockingWithYearAndVenue(bucketDict:dict,df:pd.DataFrame)-> dict:
    
    # creating key for dict. here key is made by concating venue and year of publication(ie. VLDB2003, VLDB2002,SIGMOD2004, SIGMOD1999 etc)
    df['key'] = pd.concat([df['publicationVenue'].astype(str), df['yearOfPublication'].astype(str)], axis=1).apply(''.join, axis=1)
    for index, record in df.iterrows():
        if str(record['key']) not in bucketDict:
            bucketDict[record['key']] = []
        bucketDict[record['key']].append(dict(record))
    return bucketDict

# calculting similarity value for matching stage. 
def calculateSimilarity(acmItem:dict, dblpItem:dict, threshold:float)-> float|None:

    set1 = set(str(acmItem['publicationTitle']).lower().split())
    set2 = set(str(dblpItem['publicationTitle']).lower().split())
    # Calculate Jaccard similarity using similaritymeasures
    # jaccard_similarity = similaritymeasures.Jaccard(set1,set2)
    jaccard_similarity = 1.0 - jaccard_distance(set1,set2)

    if(jaccard_similarity >= threshold):
        # print(f'publicationTitle Acm :  {set1}')
        # print(f'publicationTitle Dblp:  {set2}')
        # print(f"Jaccard Similarity: {jaccard_similarity}")
        return jaccard_similarity
    return None

def er():

    # # working with sample data url
    # urlACM = "data/sampleACM.csv"
    # urlDBLP = "data/sampleDBLP.csv"

    # real data url
    urlACM = "data/ACM_1995_2004.csv"
    urlDBLP = "data/DBLP_1995_2004.csv"

    # read data
    dfACM = pd.read_csv(urlACM)
    dfDBLP = pd.read_csv(urlDBLP)

    #********************************* BLOCKING STAGE  *********************************
    # creating bucket for blocking stage
    # bucketDict:dict ={}
    # bucketDict = createBlockingWithYearAndVenue(bucketDict,dfACM)
    # bucketDict = createBlockingWithYearAndVenue(bucketDict, dfDBLP)

    # creating separate bucket/dict as this way we are not checking value from the same website with its own value
    bucketDictAcm:dict ={}
    bucketDictDblp:dict ={}
    bucketDictAcm = createBlockingWithYearAndVenue(bucketDictAcm,dfACM)
    bucketDictDblp = createBlockingWithYearAndVenue(bucketDictDblp, dfDBLP)

    # pprint(bucketDictAcm) 
    print("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFfffffffffffffffffffffffffffffFF")
    # pprint(bucketDictDblp)


    #********************************* MATCHING STAGE  *********************************

    acmKeys = list(bucketDictAcm.keys())
    dblpKeys = list(bucketDictDblp.keys())
    threshold = .80

    for key in acmKeys:
        if key in dblpKeys:  # if the key of acm also exist in dbpl(ie in the same bucket)
            # print(key)
            # print(bucketDictAcm[key])
            for acmItem in bucketDictAcm[key]:
                for dblpItem in bucketDictDblp[key]: 
                    similarityValue = calculateSimilarity(acmItem, dblpItem, threshold)
                    if similarityValue:
                        print(acmItem)
                        print(dblpItem)
                        print(f"Jaccard Similarity: {similarityValue}")







if __name__ == "__main__":
    er()
    