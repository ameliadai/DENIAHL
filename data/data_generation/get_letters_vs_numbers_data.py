import json
import os
from gen_letters_vs_numbers import generate_dictionary, dict_to_sentences

num_dateset = 100
num_pairs = 100
len_items = [10, 20, 30, 40]
modes = ['letters', 'numbers', 'mixed']

dir_path = "../main_data"

if not os.path.exists(dir_path):
    os.makedirs(dir_path)


for len_item in len_items:
    for mode in modes:
        full_json_data = []
        full_sentence_data = []
        for _ in range(num_dateset):
            # json data
            data = generate_dictionary(num_pairs, mode, len_item)
            full_json_data.append(data)
            with open(f'../main_data/json_{mode}_len={len_item}.json', 'w', encoding='utf-8') as outfile:
                json.dump(full_json_data, outfile, indent=4)

            # # sentence data
            # sentence_data = dict_to_sentences(data)
            # full_sentence_data.append(sentence_data)
            # with open(f'../main_data/sentence_{mode}_len={len_item}.txt', 'w') as outfile:
            #     full_data_str = '\n'.join(full_sentence_data)
            #     outfile.write(full_data_str)