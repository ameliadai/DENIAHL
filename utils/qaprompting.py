import random


def generate_prompt(index_prompt, data_loc, data, max_i=10):
    full_ds_dict = {}
    if data_loc[:12] == "data/qa_data":
        ds = "QANelson"
        base_prompt = """Write a high-quality answer for the given question using only the provided search results (some of which might be irrelevant). \n
{} \n
Question: {} 
Answer: \n
"""
    if index_prompt == 'rand':
        n_samples = 100
        random_indices = [random.randint(0, max_i) for _ in range(n_samples)]
        prompts_to_return = [base_prompt.format(i) for i in random_indices]
    elif index_prompt == 'full':
        prompts_to_return = []
        if ds == "QANelson":
            full_ds_dict = {}
            for d in data:
                ds_subset = d['ctxs']
                indx=0
                ds_subset_str = "\n"
                for subsetdata in ds_subset[:max_i]:
                    ds_subset_dict = dict(subsetdata)
                    full_ds_dict.update(ds_subset_dict)
                    title=ds_subset_dict['title']
                    text=ds_subset_dict['text']
                    ds_subset_str += f' Document [{indx}] (Title: {title}) {text},\n'
                    indx+=1
                prompts_to_return.extend([base_prompt.format(ds_subset_str, d['question'])])
        else:
            indices = list(range(0, max_i))
            prompts_to_return = [base_prompt.format(i) for i in indices]
    return prompts_to_return, full_ds_dict
