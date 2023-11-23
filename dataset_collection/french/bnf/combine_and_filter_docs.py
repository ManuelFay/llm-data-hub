# import docs from data/monographies_gallica.xlsx and data/liste_monographies_gallica-integres_mars2021.csv in two dfs
import pandas as pd
import os

df2 = pd.read_csv("data/liste_monographies_gallica-integres_mars2021.csv")

# clean df2
interesting_columns = ["title", "author", "ark", "date", "rights", "mean_nqa", "subject"]

# contributor + creator column
df2["author"] = df2["creator"].fillna(df2["contributor"]).fillna("")
df2["mean_nqa"] = df2["nqamoyen"].fillna(0)

# keep only interesting columns
df2 = df2[interesting_columns]
df2["original_folder"] = "2021"
df2 = df2.fillna("")

# cast column types to string
for col in df2.columns:
    df2[col] = df2[col].astype(str)

df1 = pd.read_excel("data/monographies_gallica.xlsx")
# print columns
print(df1.columns)
# clean df1
df1["author"] = df1["AUTEURS"].fillna("")
df1["title"] = df1["TITRE"].fillna("")
df1["ark"] = df1["URL"].apply(lambda x: x.split("/")[-1]).fillna("")
df1["date"] = df1["DATES"].fillna("")
df1["rights"] = df1["DROITS"].fillna("")
df1["mean_nqa"] = df1["NQA Moyen (%)"].fillna(0)
df1["subject"] = df1["SUJETS"].fillna("")
df1 = df1[interesting_columns]
df1["original_folder"] = "2023"
df1 = df1.fillna("")
for col in df1.columns:
    df1[col] = df1[col].astype(str)


# merge
df = pd.concat([df1, df2])
# mean_nqa is float, and between 0 and 100
df["mean_nqa"] = df["mean_nqa"].astype(float)
df = df[(df["mean_nqa"] >= 0) & (df["mean_nqa"] <= 100)]

# export
print("Exporting to csv")
print("A few stats on the dataset")
print(f"Number of documents: {len(df)}")

# filter columns where title is empty, or author is empty
df = df[(df["title"] != "") & (df["author"] != "")]
print(f"Number of documents after filtering empty titles and authors: {len(df)}")

print(f"Number of unique authors: {len(df['author'].unique())}")
print(f"Number of unique titles: {len(df['title'].unique())}")
# Nqa
print(f"Mean nqa: {df['mean_nqa'].mean()}")


df.to_csv("data/gallica_clean_export.csv", index=False)

# ark whitelist - all documents with NQA > 90
ark_whitelist = set(df[df["mean_nqa"] > 90]["ark"].values)
print(f"Number of documents with NQA > 90: {len(ark_whitelist)}")
# export it as txt file with one ark per line
with open("data/ark_whitelist.txt", "w") as f:
    f.write("\n".join(ark_whitelist))
