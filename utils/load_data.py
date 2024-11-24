from tqdm import tqdm
from xopen import xopen
import json

#TODO: generalize this beyond just kv data
def get_data(input_path, limit=-1):
    if input_path.endswith('.gz'):
        all_examples = []
        with xopen(input_path) as fin:
            for line in tqdm(fin):
                input_example = json.loads(line)
                all_examples.append(input_example)
        return all_examples[:limit]
        
    elif input_path.endswith('.json'):
        with open(input_path, 'r') as file:
            all_examples = json.load(file)
        return all_examples[:limit]