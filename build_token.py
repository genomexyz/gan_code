from tokenizers import (
    decoders,
    models,
    normalizers,
    pre_tokenizers,
    processors,
    trainers,
    Tokenizer,
)
import torch
from datasets import load_dataset

#setting
sandi_filename = 'sandi_metarv2.txt'

#models.WordPiece
#tokenizer = Tokenizer(models.WordLevel(unk_token="[UNK]"))
tokenizer = Tokenizer(models.WordPiece(unk_token="[UNK]"))
tokenizer.normalizer = normalizers.Sequence(
    [normalizers.NFD(), normalizers.Lowercase(), normalizers.StripAccents()]
)


tokenizer.pre_tokenizer = pre_tokenizers.Sequence(
    [pre_tokenizers.WhitespaceSplit()]
)

special_tokens = ["[UNK]", "<|endoftext|>", "<|separator|>"]
trainer = trainers.WordPieceTrainer(vocab_size=30, special_tokens=special_tokens)
#trainer = trainers.WordLevelTrainer(special_tokens=special_tokens)


tokenizer.train(["sandi_metarv2.txt"], trainer=trainer)

print(tokenizer)

encoding = tokenizer.encode("METAR Q1009")

print(encoding)
print(encoding.tokens)

# Save the tokenizer to a directory
tokenizer.save('token.json', pretty=True)