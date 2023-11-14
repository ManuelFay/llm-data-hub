import datasets
from datasets import load_dataset

ds = load_dataset("rcds/swiss_legislation", split="train")
df = ds.to_pandas()
# filter out the ones that are not in French
df = df[df.language == "fr"].reset_index(drop=True)
# keep only pdf_content column that you rename as text, and uuid column renamed as id
df = df[["pdf_content", "uuid"]].rename(columns={"pdf_content": "text", "uuid": "id"})
ds = datasets.Dataset.from_pandas(df)
print(ds)

ds.push_to_hub("manu/swiss_legislation",  private=False)
