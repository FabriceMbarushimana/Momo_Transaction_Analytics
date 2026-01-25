def transaction_dictionary(data_list):
    return {item['id']: item for item in data_list}

def dict_lookup(data_dict, target_id):
    return data_dict.get(target_id)
