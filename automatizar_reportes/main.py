import os
import pandas as pd

BASE_DIR = os.path.dirname(__file__)

data_file = os.path.join(BASE_DIR , 'supermarket_sales.csv') 
x_column = 'Product line'

df = pd.read_csv(data_file) if data_file.endswith('.csv') else pd.read_excel(data_file)

print(df.columns)