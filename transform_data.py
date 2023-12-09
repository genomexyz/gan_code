import numpy as np
from metar import Metar
import re
import random
import string
from datasets import Dataset

#setting
total_dataset = 50000
stasiun_file = 'list_stasiun.csv'
sandi_file = 'sandi_metar.txt'
pattern = r'TAF\s+(\w{3}\s+)?(\w{4}\s+)(\d{6}Z\s+)(\d{4}/\d{4}\s+)((VRB|\d{3})\d{2}KT\s+)(\d{4}\s+)(([\+\-])?([A-Z]{2,5}\s+))?((SCT|FEW|BKN|OVC)(\d{3})(CB)?\s+)((SCT|FEW|BKN|OVC)(\d{3})(CB)?\s+)?((SCT|FEW|BKN|OVC)(\d{3})(CB)?\s+)?(PROB\d{2}\s+)?(BECMG\s+|TEMPO\s+)(\d{4}/\d{4}\s+)((VRB|\d{3})\d{2}KT(\s+|))?(\d{4}(\s+|))?(([\+\-]?[A-Z]{2,5})(\s+|))?((SCT|FEW|BKN|OVC)(\d{3})(CB)?\s+)?((SCT|FEW|BKN|OVC)(\d{3})(CB)?\s+)?((SCT|FEW|BKN|OVC)(\d{3})(CB)?\s+)?(PROB\d{2}\s+)?(BECMG\s+|TEMPO\s+)?(\d{4}/\d{4}\s+)?((VRB|\d{3})\d{2}KT(\s+|))?(\d{4}(\s+|))?(([\+\-]?[A-Z]{2,5})(\s+|))?((SCT|FEW|BKN|OVC)(\d{3})(CB)?\s+)?((SCT|FEW|BKN|OVC)(\d{3})(CB)?\s+)?((SCT|FEW|BKN|OVC)(\d{3})(CB)?\s+)?(PROB\d{2}\s+)?(BECMG\s+|TEMPO\s+)?(\d{4}/\d{4}\s+)?((VRB|\d{3})\d{2}KT(\s+|))?(\d{4}(\s+|))?(([\+\-]?[A-Z]{2,5})(\s+|))?((SCT|FEW|BKN|OVC)(\d{3})(CB)?\s+)?((SCT|FEW|BKN|OVC)(\d{3})(CB)?\s+)?((SCT|FEW|BKN|OVC)(\d{3})(CB)?\s+)?(PROB\d{2}\s+)?(BECMG\s+|TEMPO\s+)?(\d{4}/\d{4}\s+)?((VRB|\d{3})\d{2}KT(\s+|))?(\d{4}(\s+|))?(([\+\-]?[A-Z]{2,5})(\s+|))?((SCT|FEW|BKN|OVC)(\d{3})(CB)?\s+)?((SCT|FEW|BKN|OVC)(\d{3})(CB)?\s+)?((SCT|FEW|BKN|OVC)(\d{3})(CB)?)?(=)'
wrong_pattern = ['missing', 'merge', 'add']


#print(generate_random_ascii())
#exit()

def generate_random_icao(length=4):
    uppercase_letters = string.ascii_uppercase
    random_string = ''.join(random.choice(uppercase_letters) for _ in range(length))
    return random_string





with open(sandi_file) as f:
    real_raw = f.read()
real_raw = real_raw.strip()
real_raw_arr = real_raw.split('\n')


all_sandi = []
for i in range(total_dataset):
    print('progress %s/%s'%(i+1, total_dataset))
    idx_sandi = np.random.randint(0,len(real_raw_arr))
    sandi_choose = real_raw_arr[idx_sandi]
    sandi_choose_arr = sandi_choose.split(' ')
    
    random_icao = generate_random_icao()
    sandi_choose_new = sandi_choose.replace(' WAFF ', ' %s '%(random_icao))
    all_sandi.append(sandi_choose_new)

all_sandi_str = '\n'.join(all_sandi)

with open('sandi_metarv2.txt', 'w') as f:
    f.write(all_sandi_str)