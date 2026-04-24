import pandas as pd
data1 = ['red', 'blue', 'green', 'yellow']
data2 = [11, 22, 33, 44]
pd.Series(data1, index=data2)  # This will create a Series with custom indices
# Displaying the Series with custom indices
print("\nSeries with custom indices:")
print(pd.Series(data1, index=data2))


