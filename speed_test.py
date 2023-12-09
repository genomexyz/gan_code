from datasets import Dataset

data_df = Dataset.load_from_disk('dset_metar')
#print(data_df)
#print(data_df[0])

def merge_columns(example):
    example["prediction"] = example["prompt"] + " <|separator|> " + example["response"]
    return example

data_df = data_df.map(merge_columns)
print(data_df[0])

#for iter_df in range(len(data_df)):
#    data_df[iter_df]['prediction'] = data_df[iter_df]["prompt"] + " <|separator|> " + data_df[iter_df]["response"]
#
#print(data_df[0])