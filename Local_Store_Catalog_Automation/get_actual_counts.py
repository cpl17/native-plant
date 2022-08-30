import pandas as pd

df = pd.read_excel("./Data/PA Wildflower Database.xlsx",sheet_name="LOCAL")
df.groupby("SOURCE").size().to_csv("Data/Actual Counts.csv")