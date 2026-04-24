import pandas as pd
# Creating a Series from a dictionary
data_dict = {'red': 'แดง', 'blue': 'น้ำเงิน', 'green': 'เขียว', 'yellow': 'เหลือง'}
ps = pd.Series(data_dict)
# Displaying the Series
print("Series created from dictionary:")
print(ps)
