import uuid
import random
import json
import argparse


def generate_random_key_value_pair(
    max_key_length, max_value_length, random_key_length, random_value_length
):
    if random_key_length:
        key_length = random.randint(3, max_key_length)
    else:
        key_length = max_key_length

    key = (str(uuid.uuid4())+'-'+str(uuid.uuid4()))[:key_length]

    if random_value_length:
        value_length = random.randint(10, max_value_length)
    else:
        value_length = max_value_length

    value = (str(uuid.uuid4())+'-'+str(uuid.uuid4()))[:value_length]
    # value = "".join(
    #     random.choices(
    #         "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
    #         k=value_length,
    #     )
    # )

    return key, value


def generate_key_value_pairs(
    num_pairs, max_key_length, max_value_length, random_key_length, random_value_length
):
    return {
        key: value
        for key, value in [
            generate_random_key_value_pair(
                max_key_length, max_value_length, random_key_length, random_value_length
            )
            for _ in range(num_pairs)
        ]
    }


def export_to_json(data, file_path):
    with open(file_path, "w") as json_file:
        json.dump(data, json_file, indent=4)


def main():
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
        "--max_key_length", type=int, default=32, help="Maximum length of the key."
    )
    parser.add_argument(
        "--max_value_length", type=int, default=100, help="Maximum length of the value."
    )
    parser.add_argument(
        "--random_key_length", action="store_true", help="Generate random key lengths."
    )
    parser.add_argument(
        "--random_value_length",
        action="store_true",
        help="Generate random value lengths.",
    )
    parser.add_argument(
        "--output_file", default="key_value_pairs.json", help="Output JSON file name."
    )

    args = parser.parse_args()

    # Generate key-value pairs
    result = generate_key_value_pairs(
        args.num_pairs,
        args.max_key_length,
        args.max_value_length,
        args.random_key_length,
        args.random_value_length,
    )

    # Export key-value pairs to a JSON file
    export_to_json(result, args.output_file)

    print(f"Key-value pairs exported to '{args.output_file}'")


if __name__ == "__main__":
    main()
