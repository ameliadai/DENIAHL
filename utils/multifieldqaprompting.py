import random
def generate_prompt(index_prompt, data_loc, data):
    full_ds_dict = {}
    if data_loc[:21] == "data/multifieldqa_en/":
        ds = "MultifieldQA"
        base_prompt = """Read the following text and answer briefly.\n
{} \n
Now, answer the following question based on the above text, only give me the answer and do
not output any other words.\n
Question: {} 
Answer: \n
"""
    if index_prompt == 'full':
        prompts_to_return = []
        if ds == "MultifieldQA":
            full_ds_dict = {}
            for d in data:
                if(d['length']<=4096):
                    context=d['context']
                    question=d['input']
                    full_ds_dict.update(d)
                    prompts_to_return.extend([base_prompt.format(context,question)])
    return prompts_to_return,full_ds_dict
