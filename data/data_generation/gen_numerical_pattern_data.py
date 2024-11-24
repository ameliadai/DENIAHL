import random
import json
import argparse
import string


def export_to_json(data, file_path):
    with open(file_path, "w") as json_file:
        json.dump(data, json_file, indent=4)


import random


def generate_dictionary(num_pairs):
    num_dicts = 100
    list_of_dicts = []
    for _ in range(num_dicts):

        random_w = random.randint(1, 10)
        random_b = random.randint(0, 20)
        my_dict = {}
        for i in range(1, num_pairs + 1):
            my_dict[i] = i * random_w + random_b

        list_of_dicts.append(my_dict)

    return list_of_dicts




# Python code to generate a JSON object with complex relationships

def generate_longer_window(num_pairs):
    data = {}

    base_value = 5
    increment = 10

    previous_value = 5

    for key in range(1, num_pairs):
        if key % 5 == 0:
            data[key] = base_value
            base_value += increment
        else:
            if key % 5 == 1:
                previous_value = data[key - 1] if key > 1 else previous_value
            data[key] = 2 * previous_value
            previous_value = data[key]

    return data

def generate_shorter_window(num_pairs):
    data = {}
    for i in range(1, num_pairs + 1):
        if i % 2 == 0:
            data[i] = 2 * i
        else:
            data[i] = 2 * i**2 + 1

    return data

def generate_letter_pattern(num_pairs):
    def generate_unique_key(existing_keys):
        while True:
            new_key = random.choice(string.ascii_lowercase) + random.choice(string.ascii_lowercase)
            if new_key not in existing_keys:
                return new_key

# Generate a list of 100 dictionaries, each with 100 unique key-value pairs
    list_of_dicts = []
    for _ in range(100):
        keys = set()  # Set to track existing keys
        current_dict = {}
        while len(current_dict) < num_pairs:
            key = generate_unique_key(keys)
            current_dict[key] = key.upper()
            keys.add(key)
        list_of_dicts.append(current_dict)
    return list_of_dicts


import random


def generate_numerical_pattern(num_pairs = 100, num_dicts = 100, base_start = 5, increment_start = 10, interval=5):
    dicts_list = []

    # Generate multiple dictionaries
    for _ in range(num_dicts):
        data = {}
        # base_value = base_start
        # increment = increment_start
        base_value = random.randint(base_start - 5, base_start + 5)  # Randomize starting base within a range
        increment = random.randint(increment_start - 5, increment_start + 5)  # Randomize increment within a range
        previous_value = base_value  # Start with the initial base value

        for key in range(1, num_pairs + 1):
            if key % interval == 1 or key == 1:
                data[key] = base_value
                base_value += increment
            elif key > 1:
                previous_value = data[key - 1]
                data[key] = 2 * previous_value

        dicts_list.append(data)

    return dicts_list





def main():
    random_dict = {}
    parser = argparse.ArgumentParser(
        description="Generate and export random key-value pairs to a JSON file."
    )
    parser.add_argument(
        "--num_pairs",
        type=int,
        default=100,
        help="Number of key-value pairs to generate.",
    )
    parser.add_argument(
        "--output_file", default="new_numerical_pattern_easy.json", help="Output JSON file name."
    )
    parser.add_argument(
        "--pattern_mode", default=1, help="Select the pattern mode."
    )
    args = parser.parse_args()

    if args.pattern_mode == 1:
        random_dict = generate_dictionary(args.num_pairs)
    elif args.pattern_mode == 2:
        random_dict = generate_shorter_window(args.num_pairs)
        print('11')
        print(random_dict)
    elif args.pattern_mode == 3:
        random_dict = generate_longer_window(args.num_pairs)
    elif args.pattern_mode == 4:
        random_dict = generate_letter_pattern(args.num_pairs)
    elif args.pattern_mode == 5:
        random_dict = generate_numerical_pattern(num_pairs=args.num_pairs)
    export_to_json(random_dict, args.output_file)




if __name__ == "__main__":
    main()