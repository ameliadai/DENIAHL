
import random
import string

def generate_prompt(index_prompt, data_loc, data, num_kv=50, key_loc=0, prompt_type='json'):
    # generate the base prompt
    if prompt_type == "json":
        base_prompt = """Extract the value corresponding to the specified key in the JSON object below. \n
JSON data:
{} \n
Key: "{}" 
Corresponding value:"""
    elif prompt_type == "sentence":
        base_prompt = """Extract the value corresponding to the specified key in the data below. \n
Data:
{} \n
Key: "{}" 
Corresponding value:"""
    if "kv_retrieval_data" in data_loc:
        ds = "KVNelson"
    elif "kv_item_len_data" in data_loc:
        ds = "KVItemLen"
    elif "letter_pattern" in data_loc:
        ds = "letter_pattern"
    elif "numerical_pattern" in data_loc:
        ds = "numerical_pattern"
    elif "letter_num" or "main" in data_loc:
        ds = "letter_num"
    elif "niah" in data_loc:
        return data, {}, "1) Go to Dolores Park. 2) Eat at Tony's Pizza Napoletana. 3) Visit Alcatraz. 4) Hike up Twin Peaks. 5) Bike across the Golden Gate Bridge"
    else:
        base_prompt = "Extract the {}th element from the following 'Data': 'Data': "

    # get prompts
    if ds == "KVNelson":
        # get the json part
        full_ds_dict = {}
        prompts_to_return = []
        ground_truth = []
        for d in data:
            ds_subset = d['ordered_kv_records']
            ds_subset_dict = dict(ds_subset[:num_kv])
            full_ds_dict.update(ds_subset_dict)
            ds_subset_str = "{\n"
            for key, value in ds_subset_dict.items():
                ds_subset_str += f' "{key}": "{value}",\n'
            ds_subset_str += "}"

            # add the key in prompt
            if index_prompt == 'step':
                prompts_to_return.append(base_prompt.format(ds_subset_str, ds_subset[key_loc][0]))
                ground_truth.append(ds_subset[key_loc][1])

            elif index_prompt == 'full':
                prompts_to_return.extend(
                    [base_prompt.format(ds_subset_str, dp[0]) for n, dp in enumerate(ds_subset) if n < num_kv])
                ground_truth = [dp[1] for n, dp in enumerate(ds_subset) if n < num_kv]

    elif ds == "KVItemLen" or ds == "letter_num":
        full_ds_dict = {}
        prompts_to_return = []
        ground_truth = []
        for ds_subset in data:
            ds_subset_dict = dict([d for n, d in enumerate(ds_subset.items()) if n < num_kv])
            full_ds_dict.update(ds_subset_dict)
            if prompt_type == "json":
                ds_subset_str = "{\n"
                for key, value in ds_subset_dict.items():
                    ds_subset_str += f' "{key}": "{value}",\n'
                ds_subset_str += "}"
            elif prompt_type == "sentence":
                ds_subset_str = "{\n"
                for key, value in ds_subset_dict.items():
                    ds_subset_str += f'For key "{key}", the value is "{value}".\n'
                ds_subset_str += "}"

            keys = ds_subset_dict.keys()
            values = ds_subset_dict.values()

            if index_prompt == 'once':
                prompts_to_return.extend(
                    [base_prompt.format(ds_subset_str, k) for n, k in enumerate(keys) if n% 5 == 0 and n < num_kv])
                ground_truth.extend([v for n, v in enumerate(values) if n % 5 == 0 and n < num_kv])

            elif index_prompt == 'step':
                prompts_to_return.append(base_prompt.format(ds_subset_str, list(ds_subset_dict.items())[key_loc][0]))
                ground_truth.append(list(ds_subset_dict.items())[key_loc][1])



    elif ds == "letter_pattern" or ds == "numerical_pattern":
        full_ds_dict = {}
        prompts_to_return = []
        ground_truth = []
        for ds_subset in data:
            ds_subset_dict = dict([d for n, d in enumerate(ds_subset.items()) if n < num_kv])
            full_ds_dict.update(ds_subset_dict)
            ds_subset_str = "{\n"
            for i, (key, value) in enumerate(ds_subset_dict.items()):
                if i!= key_loc or index_prompt == 'original':
                    ds_subset_str += f' "{key}": "{value}",\n'
                else:
                    if ds == "numerical_pattern":
                        random_value = random.randint(1,1000)
                        while random_value == int(value):
                            random_value = random.randint(1,1000)
                    elif ds == "letter_pattern":
                        random_letters = random.choices(string.ascii_uppercase, k=2)
                        random_value = ''.join(random_letters)
                        while random_value == str(value):
                            random_letters = random.choices(string.ascii_uppercase, k=2)
                            random_value = ''.join(random_letters)
                    ds_subset_str += f' "{key}": "{random_value}",\n'
            ds_subset_str += "}"
            # step_mode: we have 50 datasets, 30 kv pairs,
            # 7 retrieval for each dataset, so in total we have 50*7 = 350 retrieval.random_index = [0, 5, 10, 15, 20, 25, 29]
            if index_prompt == 'step':
                prompts_to_return.append(base_prompt.format(ds_subset_str, list(ds_subset_dict.items())[key_loc][0]))
                ground_truth.append(random_value)
            elif index_prompt == 'original':
                prompts_to_return.append(base_prompt.format(ds_subset_str, list(ds_subset_dict.items())[key_loc][0]))
                ground_truth.append(list(ds_subset_dict.items())[key_loc][1])


    else:
        indices = list(range(0, max_i))
        prompts_to_return = [base_prompt.format(i) for i in indices]

    return prompts_to_return, full_ds_dict, ground_truth
