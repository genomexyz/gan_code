import numpy as np
from metar import Metar
import re
import random
import string
from datasets import Dataset

#setting
total_dataset = 100000
stasiun_file = 'list_stasiun.csv'
sandi_file = 'sandi_metarv2.txt'
wrong_pattern = ['missing', 'merge', 'add']


def generate_random_ascii():
    # ASCII range for printable characters is 32 to 126
    random_ascii = chr(random.randint(32, 126)).upper()
    return random_ascii

#print(generate_random_ascii())
#exit()

def generate_random_icao(length=4):
    uppercase_letters = string.ascii_uppercase
    random_string = ''.join(random.choice(uppercase_letters) for _ in range(length))
    return random_string

def logistic_function(x, fairness=1):
    # Logistic function for probability transformation
    return (1 / (1 + np.exp(-x)))**fairness

def weighted_logistic_prob(N, fairness=1):
    probabilities = np.array([logistic_function(-0.5 * (number - 1), fairness) for number in range(1, N + 1)])
    probabilities = probabilities / np.sum(probabilities)
    print('cek prob', probabilities)
    return probabilities

def weighted_logistic_random_choice(N, fairness=1):
    probabilities = np.array([logistic_function(-0.5 * (number - 1), fairness) for number in range(1, N + 1)])
    probabilities = probabilities / np.sum(probabilities)
    choice = np.arange(len(probabilities))
    choice += 1

    random_number = np.random.uniform()
    cumulative_probability = 0
    for i in range(len(probabilities)):
        probability = probabilities[i]
        cumulative_probability += probability
        chosen_number = choice[i]
        if random_number < cumulative_probability:
            break
    return chosen_number

    # Initialize cumulative probability
    #cumulative_probability = 0
#
    ## Iterate through the probabilities and choose the corresponding number
    #for number, probability in probabilities.items():
    #    cumulative_probability += probability
    #    if random_number < cumulative_probability:
    #        chosen_number = number
    #        break
#
    #return chosen_number
#N = 10
#prob = weighted_logistic_random_choice(N)
#cum = 0
#for i in range(10):
#    cum += prob[i+1]
#print('total cum', np.sum(prob))
#exit()


with open(sandi_file) as f:
    real_raw = f.read()
real_raw = real_raw.strip()
all_correct_sandi = real_raw.split('\n')



question_all_new = []
answer_all_new = []
for i in range(total_dataset):
    print('progress %s/%s'%(i+1, total_dataset))
    idx_sandi = np.random.randint(0,len(all_correct_sandi))
    sandi_choose = all_correct_sandi[idx_sandi]
    sandi_choose_arr = sandi_choose.split(' ')
    
    random_icao = generate_random_icao()
    sandi_choose_new = sandi_choose.replace(' WAFF ', ' %s '%(random_icao))
    sandi_arr = sandi_choose_new.split(' ')

    #chance for right sandi
    chance = np.random.uniform()
    if chance < 0.05:
        question_all_new.append(sandi_choose_new)
        answer_all_new.append(sandi_choose_new+'<|endoftext|>')
        continue

    total_wrong = weighted_logistic_random_choice(len(sandi_arr), 4)
    idx_choosen = np.random.choice(len(sandi_arr), total_wrong)
    for iter_wrong in range(total_wrong):
        minus_plus_chance = np.random.uniform()
        if minus_plus_chance < 0.5:
            back_front = np.random.uniform()
            if back_front < 0.5:
                sandi_arr[idx_choosen[iter_wrong]] = sandi_arr[idx_choosen[iter_wrong]][1:]
            else:
                sandi_arr[idx_choosen[iter_wrong]] = sandi_arr[idx_choosen[iter_wrong]][:-1]
        else:
            back_front = np.random.uniform()
            if back_front < 0.5:
                sandi_arr[idx_choosen[iter_wrong]] = generate_random_ascii() + sandi_arr[idx_choosen[iter_wrong]]
            else:
                sandi_arr[idx_choosen[iter_wrong]] = sandi_arr[idx_choosen[iter_wrong]] + generate_random_ascii()
    
    sandi_wrong = ' '.join(sandi_arr)
    sandi_right = sandi_choose_new
    question_all_new.append(sandi_wrong)
    answer_all_new.append(sandi_right+'<|endoftext|>')

dict_df = {}
dict_df['prompt'] = question_all_new
dict_df['response'] = answer_all_new

# Step 3: Create a Hugging Face Dataset
custom_dataset = Dataset.from_dict(dict_df)

# Step 3: Save the dataset in the desired format (JSON in this example)
dataset_save_path = "dset_metar"
custom_dataset.save_to_disk(dataset_save_path)