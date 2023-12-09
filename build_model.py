import math
import os
from tempfile import TemporaryDirectory
from typing import Tuple
import numpy as np
from collections import Counter, OrderedDict

import torch
from torch import nn, Tensor
from torch.nn import TransformerEncoder, TransformerEncoderLayer
from torch.utils.data import dataset

from torchtext.datasets import WikiText2
from torchtext.data.utils import get_tokenizer
from torchtext.vocab import build_vocab_from_iterator
from torchtext.vocab import vocab
from torchtext.data.utils import get_tokenizer
from datasets import Dataset

from transformers import PreTrainedTokenizerFast

device = 'cpu'
sandi_filename = 'sandi_metarv2.txt'

class TransformerModel(nn.Module):

    def __init__(self, ntoken: int, d_model: int, nhead: int, d_hid: int,
                 nlayers: int, dropout: float = 0.5):
        super().__init__()
        self.model_type = 'Transformer'
        self.pos_encoder = PositionalEncoding(d_model, dropout)
        encoder_layers = TransformerEncoderLayer(d_model, nhead, d_hid, dropout)
        self.transformer_encoder = TransformerEncoder(encoder_layers, nlayers)
        self.embedding = nn.Embedding(ntoken, d_model)
        self.d_model = d_model
        self.linear = nn.Linear(d_model, ntoken)

        self.init_weights()

    def init_weights(self) -> None:
        initrange = 0.1
        self.embedding.weight.data.uniform_(-initrange, initrange)
        self.linear.bias.data.zero_()
        self.linear.weight.data.uniform_(-initrange, initrange)

    def forward(self, src: Tensor, src_mask: Tensor = None) -> Tensor:
        """
        Arguments:
            src: Tensor, shape ``[seq_len, batch_size]``
            src_mask: Tensor, shape ``[seq_len, seq_len]``

        Returns:
            output Tensor of shape ``[seq_len, batch_size, ntoken]``
        """
        src = self.embedding(src) * math.sqrt(self.d_model)
        src = self.pos_encoder(src)
        if src_mask is None:
            """Generate a square causal mask for the sequence. The masked positions are filled with float('-inf').
            Unmasked positions are filled with float(0.0).
            """
            src_mask = nn.Transformer.generate_square_subsequent_mask(len(src)).to(device)
        output = self.transformer_encoder(src, src_mask)
        output = self.linear(output)
        return output

class PositionalEncoding(nn.Module):

    def __init__(self, d_model: int, dropout: float = 0.1, max_len: int = 5000):
        super().__init__()
        self.dropout = nn.Dropout(p=dropout)

        position = torch.arange(max_len).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2) * (-math.log(10000.0) / d_model))
        pe = torch.zeros(max_len, 1, d_model)
        pe[:, 0, 0::2] = torch.sin(position * div_term)
        pe[:, 0, 1::2] = torch.cos(position * div_term)
        self.register_buffer('pe', pe)

    def forward(self, x: Tensor) -> Tensor:
        """
        Arguments:
            x: Tensor, shape ``[seq_len, batch_size, embedding_dim]``
        """
        x = x + self.pe[:x.size(0)]
        return self.dropout(x)

def data_process(raw_text_iter) -> Tensor:
    """Converts raw text into a flat Tensor."""
    data = [torch.tensor(vocab(tokenizer(item)), dtype=torch.long) for item in raw_text_iter]
    return torch.cat(tuple(filter(lambda t: t.numel() > 0, data)))

#def get_train_data():
#    for i in range(len(data_raw_arr)):
#        yield data_raw_arr[i]

def data_process(raw_text_iter: dataset.IterableDataset) -> Tensor:
    """Converts raw text into a flat Tensor."""
    data = [torch.tensor(tokenizer(item)['input_ids'], dtype=torch.long) for item in raw_text_iter]
    return torch.cat(tuple(filter(lambda t: t.numel() > 0, data)))

with open(sandi_filename) as f:
    data_raw = f.read()

#data_raw_arr = data_raw.split('\n')
#if data_raw_arr[-1] == '':
#    data_raw_arr = data_raw_arr[:-1]
#
#data_raw_arr = data_raw_arr[:10]


#data_raw_arr = np.array(data_raw_arr, dtype=str)
#print(data_raw_arr)

tokenizer = PreTrainedTokenizerFast(tokenizer_file="token.json")
#print(tokenizer('METAR WAFF'))
#data_arr = data_process(data_raw_arr)
#print(data_arr)
#print(data_arr.size())
#vocabs = tokenizer.get_vocab()
#print(vocabs)

data_df = Dataset.load_from_disk('dset_metar')
print(data_df)
print(data_df[0])

def merge_columns(example):
    example["prediction"] = example["prompt"] + " <|separator|> " + example["response"]
    return example

data_df = data_df.map(merge_columns)
data_df = data_df.map(lambda samples: tokenizer(samples['prediction']), batched=True)
print(data_df[0])

batch_size = 20
seq_len = 40

#data_train_param_torch = []
#data_train_label_torch = []
#break_already = False
#for iter_df in range(len(data_df['input_ids'])):
#    single_row_ids = data_df['input_ids'][iter_df]
#    for iter_ids in range(len(single_row_ids)-seq_len-1):
#        single_seq = torch.tensor(single_row_ids[iter_ids:iter_ids+seq_len])
#        single_seq2 = torch.tensor(single_row_ids[iter_ids+1:iter_ids+seq_len+1])
#        if len(data_train_param_torch) == 0:
#            data_train_param_torch = single_seq.view(1, seq_len)
#            data_train_label_torch = single_seq2.view(1, seq_len)
#        else:
#            data_train_param_torch = torch.cat([data_train_param_torch, single_seq.view(1, seq_len)])
#            data_train_label_torch = torch.cat([data_train_label_torch, single_seq2.view(1, seq_len)])
#        print('len', data_train_param_torch.size(0))
#        if data_train_param_torch.size(0) >= 10000:
#            break_already = True
#            break
#    if break_already:
#        break
#print(data_train_param_torch, data_train_param_torch.size(), data_train_label_torch.size())

data_train_param_torch = []
data_train_label_torch = []
break_already = False
for iter_df in range(len(data_df['input_ids'])):
    single_row_ids = data_df['input_ids'][iter_df]
    for iter_ids in range(len(single_row_ids)-seq_len-1):
        single_seq = torch.tensor(single_row_ids[iter_ids:iter_ids+seq_len])
        single_seq2 = torch.tensor(single_row_ids[iter_ids+1:iter_ids+seq_len+1])
        data_train_param_torch.append(single_seq)
        data_train_label_torch.append(single_seq2)
        print('len', len(data_train_label_torch))
        if len(data_train_param_torch) >= 10000:
            break_already = True
            break
    if break_already:
        break
data_train_param_torch = torch.cat(data_train_param_torch)
data_train_label_torch = torch.cat(data_train_label_torch)
print(data_train_param_torch, data_train_param_torch.size(), data_train_label_torch.size())