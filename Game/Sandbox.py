import math
import pandas as pd

if __name__ == '__main__':
    polar_df = pd.read_csv("polar_data_ext.csv")
    cl = polar_df.columns
    print(cl)
    myDict = {}
    i = 0
    for c in cl:
        myDict[c] = i
        i += 1
    print(myDict)
    print(myDict["Wind8"])

