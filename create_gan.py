import numpy as np
from metar import Metar
import re
import random
import string
from datasets import Dataset

#setting
total_dataset = 5000000
stasiun_file = 'list_stasiun.csv'
sandi_file = 'sandi_metarv2.txt'
pattern = r'TAF\s+(\w{3}\s+)?(\w{4}\s+)(\d{6}Z\s+)(\d{4}/\d{4}\s+)((VRB|\d{3})\d{2}KT\s+)(\d{4}\s+)(([\+\-])?([A-Z]{2,5}\s+))?((SCT|FEW|BKN|OVC)(\d{3})(CB)?\s+)((SCT|FEW|BKN|OVC)(\d{3})(CB)?\s+)?((SCT|FEW|BKN|OVC)(\d{3})(CB)?\s+)?(PROB\d{2}\s+)?(BECMG\s+|TEMPO\s+)(\d{4}/\d{4}\s+)((VRB|\d{3})\d{2}KT(\s+|))?(\d{4}(\s+|))?(([\+\-]?[A-Z]{2,5})(\s+|))?((SCT|FEW|BKN|OVC)(\d{3})(CB)?\s+)?((SCT|FEW|BKN|OVC)(\d{3})(CB)?\s+)?((SCT|FEW|BKN|OVC)(\d{3})(CB)?\s+)?(PROB\d{2}\s+)?(BECMG\s+|TEMPO\s+)?(\d{4}/\d{4}\s+)?((VRB|\d{3})\d{2}KT(\s+|))?(\d{4}(\s+|))?(([\+\-]?[A-Z]{2,5})(\s+|))?((SCT|FEW|BKN|OVC)(\d{3})(CB)?\s+)?((SCT|FEW|BKN|OVC)(\d{3})(CB)?\s+)?((SCT|FEW|BKN|OVC)(\d{3})(CB)?\s+)?(PROB\d{2}\s+)?(BECMG\s+|TEMPO\s+)?(\d{4}/\d{4}\s+)?((VRB|\d{3})\d{2}KT(\s+|))?(\d{4}(\s+|))?(([\+\-]?[A-Z]{2,5})(\s+|))?((SCT|FEW|BKN|OVC)(\d{3})(CB)?\s+)?((SCT|FEW|BKN|OVC)(\d{3})(CB)?\s+)?((SCT|FEW|BKN|OVC)(\d{3})(CB)?\s+)?(PROB\d{2}\s+)?(BECMG\s+|TEMPO\s+)?(\d{4}/\d{4}\s+)?((VRB|\d{3})\d{2}KT(\s+|))?(\d{4}(\s+|))?(([\+\-]?[A-Z]{2,5})(\s+|))?((SCT|FEW|BKN|OVC)(\d{3})(CB)?\s+)?((SCT|FEW|BKN|OVC)(\d{3})(CB)?\s+)?((SCT|FEW|BKN|OVC)(\d{3})(CB)?)?(=)'
wrong_pattern = ['missing', 'merge', 'add']

with open(sandi_file) as f:
    real_raw = f.read()
real_raw = real_raw.strip()
real_raw_arr = real_raw.split('\n')

max_len = 0
arr_len = []
for i in range(len(real_raw_arr)):
    len_raw = len(real_raw_arr[i])
    arr_len.append(len_raw)
    if len_raw > max_len:
        max_len = len_raw
        print(real_raw_arr[i])

print('max len', max_len)

arr_len = np.array(arr_len)
print(np.min(arr_len), np.mean(arr_len), np.max(arr_len))