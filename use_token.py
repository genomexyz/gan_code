from transformers import PreTrainedTokenizerFast

tokenizer = PreTrainedTokenizerFast(tokenizer_file="token_beta.json")

res = tokenizer('METAR MDNG 022100Z 17002KT 5000 SCT019 25/24 Q1013 NOSIG=')
split_st = tokenizer.tokenize('METAR MDNG 022100Z 17002KT 5000 SCT019 25/24 Q1013 NOSIG=')
print(res)
print(split_st)