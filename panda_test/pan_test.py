import pandas as pd
import numpy as np
# Creating a Series with mixed data types
data_ls=[10,20,'champ',15.05,'red']
ndata=np.array(data_ls)
ps=pd.Series(ndata)
# Displaying the Series
print("Series with mixed data types:")
print(ps)
# Displaying the data type of the Series
print("\nData type of the Series:")
print(ps.dtype) 
