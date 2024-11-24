# DENIAHL: In-Context Features Influence LLM Needle-In-A-Haystack Abilities

[📝 paper](https://github.com/danpechi/DENIAHL/blob/main/DENIAHL.pdf)

The needle-in-a-haystack (NIAH) test is a general task used to assess language models' (LMs') abilities to recall particular information from long input context. This framework however does not provide a means of analyzing what factors, beyond context length, contribute to LMs' abilities or inabilities to separate and recall needles from their haystacks. To provide a systematic means of assessing what features contribute to LMs' NIAH capabilities, we developed a synthetic benchmark called **DENIAHL** (Data-oriented Evaluation of NIAH for LLM's). Our work expands on previous NIAH studies by ablating NIAH features beyond typical context length including data type, size, and patterns. We find stark differences between GPT-3.5 and LLaMA 2-7B's performance on DENIAHL, and drops in recall performance when features like item size are increased, and to some degree when data type is changed from numbers to letters. This has implications for increasingly large context models, demonstrating factors beyond item-number impact NIAH capabilities.

*Our work is inspired by Liu, N. F., Lin, K., Hewitt, J., Paranjape, A., Bevilacqua, M., Petroni, F., & Liang, P. (2024). Lost in the middle: How language models use long contexts. *Transactions of the Association for Computational Linguistics*.

---
**Args for run.py**
- `-dl`: data path
- `-m`: metric for evaluation (`exact` or `hamming`)
- `-llm`: support `GPT` or `llama`
- `-llama` (optional): llama_model_name if `llm=llama`
- `-ip`: index_prompt, `full` or `step`. `full` means for the dataset, we want to generate prompt for every position, while `step` would only generate the prompt at `loc` position
- `-loc` (optional): if `ip=step`, specify the key-value location
- `-exp`: the experiment name when logging to wandb

Here are examples of how to run experiments using this repository 

**Run GPT on Nelson's kv**    
`python run.py -dl 'data/kv_retrieval_data/kv-retrieval-75_keys.jsonl.gz' -m 'exact' -llm 'GPT' -ip 'full'`    
`python run.py -dl 'data/kv_retrieval_data/kv-retrieval-75_keys.jsonl.gz' -m 'exact' -llm 'GPT' -ip 'step' -loc 49 -exp 'test_gpt_loc=49'`    
**Run llama on Nelson's kv**   
`python run.py -dl 'data/kv_retrieval_data/kv-retrieval-75_keys.jsonl.gz' -m 'exact' -llm 'llama' -llama 'Llama-2-7b-hf' -ip 'step' -loc 0 -exp 'test_llama'`

**Run llama kv on item length**  
`python run.py -dl 'data/kv_item_len_data/kv-retrieval_item_len-08.json' -m 'exact' -llm 'llama' -llama 'Llama-2-7b-hf' -ip 'step' -loc 0 -exp 'llama-7b-30kv-len=08'`


**Run GPT kv on item length** 
`python run.py -dl 'data/kv_item_len_data/kv-retrieval_item_len-64.json' -m 'exact' -llm 'GPT' -ip 'step' -loc 29 -exp 'gpt-30kv-len=64loc=29'`

**Run GPT kv on custom length** 
`python run.py -dl 'data/kv_item_len_data/kv-retrieval_item_len-32.json' -m 'exact' -llm 'GPT' -ip 'step' -loc 5 -exp 'gpt-30kv-len=32-loc=5'`

**Run GPT on pattern**   
*letter pattern*\
`python run.py -dl 'data/pattern_data/letter_pattern.json' -m 'exact' -llm 'GPT'  -ip 'step' -loc 99 -exp 'gpt-letter-pattern-loc=99'`

*numerical pattern*\
`python run.py -dl 'data/pattern_data/new_numerical_pattern_easy.json' -m 'exact' -llm 'GPT' -ip 'step' -loc 99 -exp 'gpt-numerical-pattern-easy-loc=99'`

**Run llama on pattern**   
`python run.py -dl 'data/pattern_data/new_numerical_pattern_easy.json' -m 'exact' -llm 'llama' -llama 'Llama-2-7b-hf' -ip 'step' -loc 0 -exp 'llama-7b-numerical-pattern-easy-loc=0'`   

**Run llama on letter vs numbers**   
`python run.py -dl 'data/letter_num_data/numbers.json' -m 'exact' -llm 'llama' -llama 'Llama-2-7b-hf' -ip 'step' -loc 0 -exp 'llama-7b-numbers-loc=0'`   

**Run GPT on letter vs numbers** 
 `python run.py -dl 'data/letter_num_data/letters.json' -m 'exact' -llm 'GPT' -ip 'step' -loc 0 -exp "gpt-letters-loc=0"`


**Run llama on letter vs numbers + various item len**   
`python run.py -dl 'data/letter_num_data/mixed_len=8.json' -m 'exact' -llm 'llama' -llama 'Llama-2-7b-hf' -ip 'step' -kv 30 -loc 0 -exp 'llama-7b-mixed_len-len=08-loc=0'` 


**Run llama on niah**     
`python run.py -dl 'data/niah_data/niah_len_1k.json' -m 'rouge' -llm 'llama' -llama 'Llama-2-7b-hf'  -exp 'llama-7b-niah-1k'`  

**Run GPT on niah** 
`python run.py -dl 'data/niah_data/niah_len_1k.json' -m 'rouge' -llm 'GPT'  -exp 'gpt-numbers-niah-1k'`

****
This project is done by Amelia Dai, Dan Pechi, Christina Yang, Garvit Banga,and  Raghav Mantri.

