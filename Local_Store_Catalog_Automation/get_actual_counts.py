import pandas as pd

df = pd.read_excel("PA Wildflower Database.xlsx",sheet_name="LOCAL")
df.groupby("SOURCE").size().to_csv("Actual Counts.csv")