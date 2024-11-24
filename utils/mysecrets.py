def load_properties(filepath, sep='=', comment_char='#'):
    """
    Read the file passed as parameter as a properties file.
    """
    props = {}
    with open(filepath, "rt") as f:
        for line in f:
            line_stripped = line.strip()
            if line_stripped and not line_stripped.startswith(comment_char):
                key_value = line_stripped.split(sep)
                key = key_value[0].strip()
                value = sep.join(key_value[1:]).strip().strip('"')
                props[key] = value
    return props

def get_api_key(secrets_path, api_name):
    """
    get api key from properties file
    """
    config = load_properties(secrets_path)
    api_key = config[api_name]

    return api_key