import json
from key_value_gen import generate_key_value_pairs

num_dateset = 100
num_pairs = 100
random_key_length = False
random_value_length = False

len_list = [24, 40, 48, 56]
for l in len_list:
    full_data = []
    max_key_length = max_value_length = l
    for _ in range(num_dateset):
        data = generate_key_value_pairs(
            num_pairs, max_key_length, max_value_length, random_key_length, random_value_length
        )
        full_data.append(data)

    save_file = f"kv-retrieval_item_len-{l}"
    with open(f'../kv_item_len_data/{save_file}.json', 'w', encoding='utf-8') as outfile:
        json.dump(full_data, outfile, indent=4)