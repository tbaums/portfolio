from database import CursorFromConnectionFromPool
import pandas as pd
import numpy as np 
import os

df = pd.read_csv('~/Desktop/code/datasociety/project/data.csv')
df.fillna('')

for row in range(0,len(df)-1):
    with CursorFromConnectionFromPool() as cursor:
        query = "insert into public.chicago_employees values (default, \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\');" % (df['Name'][row].replace("'", ""), df['Job Titles'][row].replace("'", ""), df['Department'][row].replace("'", ""), df['Full or Part-Time'][row], df['Salary or Hourly'][row], df['Typical Hours'][row], df['Annual Salary'][row], df['Hourly Rate'][row])
        cursor.execute(query)

print(df.head())