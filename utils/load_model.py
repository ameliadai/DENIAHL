from openai import OpenAI
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch


def get_model(model_name, api_key = None, llama_model_name = "Llama-2-7b-hf"):
    if model_name == 'GPT':
        client = OpenAI(api_key=api_key)

        return client

    elif model_name == 'llama':
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        local_cache_dir = f"/vast/work/public/ml-datasets/llama-2/{llama_model_name}"
        tokenizer = AutoTokenizer.from_pretrained(local_cache_dir)
        model = AutoModelForCausalLM.from_pretrained(local_cache_dir)
        model.to(device)

        return tokenizer, model

    elif model_name == 'mistral':
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct-v0.2")
        model = AutoModelForCausalLM.from_pretrained("mistralai/Mistral-7B-Instruct-v0.2")
        model.to(device)

        return tokenizer, model
