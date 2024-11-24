import argparse
import random
import string
import json


# def export_to_json(data, file_path):
#     with open(file_path, "w") as json_file:
#         json.dump(data, json_file, indent=4)


def dict_to_sentences(dictionary):
    sentences = ""
    for key, value in dictionary.items():
        sentences += f"The {key} value is {value}.\n"
    return sentences

def generate_sentences(num_items, mode, len_items):
    """
    Generate a list of sentence with specified number of items.

    :param num_items: Number of items in the dictionary
    :param mode: 'numbers' for sequential numbers, 'letters' for random characters, 'mixed' for letters and special characters
    :return: Dictionary with specified values according to the mode
    """
    dict = generate_dictionary(num_items, mode, len_items)
    return dict_to_sentences(dict)


def generate_dictionary(num_items, mode, len_items):
    """
    Generate a dictionary with specified number of items.

    :param num_items: Number of items in the dictionary
    :param mode: 'numbers' for sequential numbers, 'letters' for random characters, 'mixed' for letters and special characters
    :return: Dictionary with specified values according to the mode
    """
    my_dict = {}

    if mode == "numbers":
        for i in range(1, num_items + 1):
            key = str(
                "".join(
                    random.choices(
                        "0123456789",
                        k=len_items,
                    )
                )
            )
            while key in my_dict.keys():
                key = str(
                "".join(
                    random.choices(
                        "0123456789",
                        k=len_items,
                        )
                    )
                )
            my_dict[key] = str(
                "".join(
                    random.choices(
                        "0123456789",
                        k=len_items,
                    )
                )
            )
    elif mode == "letters":
        for i in range(num_items):
            # letter_index = i % 52
            # letter = string.ascii_letters[letter_index]

            # if i >= 52:
            #     letter = (letter * (i // 52 + 1))[:2]

            key = "".join(random.choices(string.ascii_letters, k=len_items))
            while key in my_dict.keys():
                key = "".join(random.choices(string.ascii_letters, k=len_items))
            my_dict[key] = "".join(random.choices(string.ascii_letters, k=len_items))

    elif mode == "mixed":
        possible_values = string.ascii_letters + "0123456789"
        for i in range(1, num_items + 1):
            key = "".join(random.choices(possible_values, k=len_items))
            while key in my_dict.keys():
                key = "".join(random.choices(possible_values, k=len_items))
            my_dict[key] = "".join(random.choices(possible_values, k=len_items))

    return my_dict


# def main():
#     parser = argparse.ArgumentParser(
#         description="Generate a dictionary with numbers, letters, or mixed values."
#     )
#     parser.add_argument("num_items", type=int, help="Number of items in the dictionary")
#     parser.add_argument(
#         "mode",
#         type=str,
#         choices=["numbers", "letters", "mixed"],
#         help='Type of values in the dictionary: "numbers", "letters", or "letters and special characters"',
#     )
#     parser.add_argument("len_items", type=int, help="Length of items in the dictionary")
#     parser.add_argument(
#         "--output_file",
#         default="letters_numbers_gen_data.json",
#         help="Output JSON file name.",
#     )
#     args = parser.parse_args()

#     result_dict = generate_dictionary(args.num_items, args.mode, args.len_items)

#     export_to_json(result_dict, args.output_file)


# if __name__ == "__main__":
#     main()
