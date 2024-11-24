import os
import glob
import json

haystack_dir = "/data/paul/*.txt"



def find_nearest_sentence_break(context, insertion_point):
    # Search backward from the insertion point until a sentence break character is found
    while insertion_point > 0 and context[insertion_point - 1] not in (".", "!", "?"):
        insertion_point -= 1
    return insertion_point


def insert_needle(context, depth_percent, needle, prompt_len, needle_question):
    # Reducing the context length by buffer. This is to account for system message, the user question, and response.
    context_length = len(context) - len(needle) - prompt_len - len(needle_question)
    context = context[:context_length]
    if depth_percent == 100:
        # If the depth percent is 100 (which means the needle is to be inserted at the end), insert it at the end
        new_context = context + needle
    else:
        # Calculate the insertion point based on the depth percent
        insertion_point = int(len(context) * (depth_percent / 100))

        # Find the nearest sentence break before the insertion point
        insertion_point = find_nearest_sentence_break(context, insertion_point)

        # Insert the needle at the appropriate point
        new_context = (
            context[:insertion_point] + " " + needle + "." + context[insertion_point:]
        )

    return new_context


def read_context_files(max_context_length = 4096):
    context = ""
    base_dir = os.path.abspath(os.path.dirname(__file__))  # Package directory
    directory, file_name = os.path.split(base_dir)
    final_dir = directory + haystack_dir
    for file in glob.glob(final_dir):
        with open(file, "r") as f:
            context += f.read().strip('\n')
    return context[:max_context_length]


def generate_prompt(depth_percent, max_context_length):
    prompt_question = "You are a helpful AI bot that answers questions for a user. Keep your response short and direct.\n \n  Don't give information outside the document or repeat your findings  "
    prompt_len = len(prompt_question)
    needle = "The 5 best things to do in San Francisco are: 1) Go to Dolores Park. 2) Eat at Tony's Pizza Napoletana. 3) Visit Alcatraz. 4) Hike up Twin Peaks. 5) Bike across the Golden Gate Bridge"
    # needle_question = "What are the 5 best things to do in San Franscisco?"
    needle_question = "Question: What are the 5 best things to do in San Franscisco?"
    context = read_context_files(max_context_length)
    new_c = insert_needle(
        context=context,
        needle=needle,
        depth_percent=depth_percent,
        prompt_len=prompt_len,
        needle_question=needle_question,
    )
    # prompt = "You are a helpful AI bot that answers questions for a user. Keep your response short and direct.\n {}\n {} Don't give information outside the document or repeat your findings".format(
    #     new_c, needle_question
    # )

    prompt = "You are a helpful AI bot that answers questions for a user. Keep your response short and direct.\n {}\n {} Don't give information outside the document or repeat your findings. Answer:".format(
        new_c, needle_question
    )

    return prompt


# print(generate_prompt(depth_percent=1, max_context_length=4000))
# max_context_length = [1000, 2000, 3000, 4000, 5000]
needle_depth = [1, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]


full_data = []
for d in needle_depth:
    data = generate_prompt(depth_percent=d, max_context_length=15000)
    # print(data)
    full_data.append(data)

file_name = "len_4k"
with open(f'../data/niah_data/niah_{file_name}.json', 'w', encoding='utf-8') as outfile:
    json.dump(full_data, outfile, indent=4)