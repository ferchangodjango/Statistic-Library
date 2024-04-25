import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from Graphs import Box_Plot

class CleaningData():
    @classmethod
    def clean(self,DATA):
        #Return a data without nan values, duplicate values and irrelevant columns
        
        #Drop null values
        DATA.dropna(inplace=True)

        #Irrelevants columns
        columns_uniques=list(DATA.columns)
        tupla_values_in_columns=[(len(DATA[columns_uniques[i]].unique()),columns_uniques[i]) for i in range(len(columns_uniques)) if len(DATA[columns_uniques[i]].unique())==1]
        try:
            for i in range(len(tupla_values_in_columns)):
                DATA.drop(tupla_values_in_columns[i][1],axis=1,inplace=True)

        except:
            DATA=DATA
        
        #Drop duplicate values
        DATA.drop_duplicates(inplace=True)

        #show outliers
        answer={
            "DATA":DATA
        }
        
        return answer
