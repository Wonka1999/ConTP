def merge_dicts(dict_list):
    # Merge dictionaries; for duplicate keys, later values override earlier ones
    result = {}
    for d in dict_list:
        result.update(d)
    return result
