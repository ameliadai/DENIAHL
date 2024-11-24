
from utils.load_data import get_data
from utils.load_model import get_model
from utils.prompting import generate_prompt
from utils.logger import log_to_wandb
from utils.mysecrets import get_api_key
from evaluate import evaluate_model

import logging

from tqdm import tqdm
from xopen import xopen
import torch

import argparse

"""
e.g.
python run.py -dl 'data/main_data/json_letters_len=20.json' -m 'exact' -llm 'llama' -llama 'Llama-2-7b-chat-hf' -ip 'step' -size 5 -kv 10 -loc 0 -exp 'test'
"""

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def run_llm_on_data(llm, prompts, results=None):
    if results is None:
        results = []
    for p in tqdm(prompts):
        if args.llm == 'GPT':
            response = llm.completions.create(
                model="gpt-3.5-turbo-instruct",
                prompt=p,
                max_tokens=300
            )
            results.append(response.choices[0].text)

        elif args.llm == 'llama':
            if 'chat' in args.llama_model_name:
                p = f"""<s>[INST] <<SYS>>
You are a helpful, respectful and honest assistant.
<</SYS>>

{p} [/INST]"""
            tokenizer, model = llm
            input_ids = tokenizer(p, return_tensors="pt").input_ids
            input_ids = input_ids.to(device)
            outputs = model.generate(input_ids, max_new_tokens=300)
            response = tokenizer.decode(outputs[0], skip_special_tokens=True)
            results.append(response[len(p)-1:])
            print(response)

        elif args.llm == 'mistral':
            tokenizer, model = llm
            input_ids = tokenizer(p, return_tensors="pt").input_ids
            input_ids = input_ids.to(device)
            outputs = model.generate(input_ids, max_new_tokens=150)
            response = tokenizer.decode(outputs[0], skip_special_tokens=True)[len(p):]
            results.append(response)

            '''
            messages = [
                {"role": "user", "content": "What is your favourite condiment?"},
                {"role": "assistant",
                 "content": "Well, I'm quite partial to a good squeeze of fresh lemon juice. It adds just the right amount of zesty flavour to whatever I'm cooking up in the kitchen!"},
                {"role": "user", "content": "Do you have mayonnaise recipes?"}
            ]
            encodeds = tokenizer.apply_chat_template(messages, return_tensors="pt")

            model_inputs = encodeds.to(device)
            model.to(device)

            generated_ids = model.generate(model_inputs, max_new_tokens=1000, do_sample=True)
            response = tokenizer.batch_decode(generated_ids)
            #print(response[0])
            results.append(response[0])
            '''

    return results


def main():
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser()

    # Add arguments
    parser.add_argument('-dl', '--data_loc', type=str, help='Data to run experiment on', required=True)
    parser.add_argument('-m', '--metric', default='exact', type=str,
                        help='The metric used to evaluate: exact or hamming', required=True)
    parser.add_argument('-llm', '--llm', type=str, help='The llm to run', required=True)
    parser.add_argument('-llama', '--llama_model_name', default='Llama-2-7b-chat-hf', type=str,
                        help='The llama model name if llm=llama', required=False)
    parser.add_argument('-ip', '--index_prompt', default='step', type=str, help='The indices to query (full/step/etc)',
                        required=False)
    parser.add_argument('-loc', '--key_loc', default=0, type=int,
                        help='The location of the key-value pair if index_prompt=step', required=False)
    parser.add_argument('-exp', '--experiment_name', default='test', type=str, help='The name of experiment',
                        required=True)
    parser.add_argument('-size', '--num_data', default=50, type=int, help='Number of dataset we want to test',
                        required=False)
    parser.add_argument('-kv', '--num_kv', default=40, type=int, help='Number of key value pairs we want to test',
                        required=False)
    parser.add_argument('-prompt', '--prompt_type', default='json', type=str,
                        help='json/sentence', required=False)

    # Parse arguments
    global args
    args = parser.parse_args()

    # data should look something like a dictionary
    logging.info("Getting data from location: %s", args.data_loc)
    data = get_data(args.data_loc,
                    args.num_data)  # change it to be the number of dataset, we use 50 of 100 dataset for evaluating length
    logging.info("Data retrieval successful.")

    # Logging statements for generating prompt
    logging.info("Generating prompt...")
    prompts, full_ds_dict, ground_truth = generate_prompt(args.index_prompt,
                                                          args.data_loc,
                                                          data,
                                                          num_kv=args.num_kv,
                                                          # change it to be the number of key-value pairs in one dataset, we use 30 of 100 kv pairs for evaluating length
                                                          key_loc=args.key_loc,
                                                          prompt_type=args.prompt_type)
    logging.info("Prompt generation complete.")

    if args.llm == 'GPT':
        # Logging statements for getting API key
        logging.info("Getting API key for model: %s", args.llm)
        api_key = get_api_key('.secrets', f'{args.llm}_API_KEY')
        logging.info("API key retrieval successful.")
    elif args.llm == 'llama':
        api_key = None

    # Logging statements for getting model
    logging.info("Loading language model: %s", args.llm)
    llm = get_model(args.llm, api_key, args.llama_model_name)
    logging.info("Language model loaded successfully.")

    # Logging statements for running language model on data
    results = []
    logging.info("Running language model on data...")
    results = run_llm_on_data(llm, prompts, results)
    logging.info("Language model execution complete.")

    # Logging statements for model evaluation
    logging.info("Evaluating model performance...")
    accuracy = evaluate_model(ground_truth, results, args.metric)
    logging.info("Model evaluation complete.")

    # metrics = log_to_wandb(full_ds_dict, results, metrics, experiment_name)
    logging.info("Evaluating model metrics in wandb...")
    wandb_results = log_to_wandb(prompts, ground_truth, results, accuracy, args.experiment_name)
    logging.info("Model evaluation complete.")


# log_to_wandb(results, metrics)

if __name__ == "__main__":
    main()
