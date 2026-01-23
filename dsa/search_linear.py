def linear_search(data_list, target_id):
    for transaction in data_list:
        if transaction['id'] == target_id:
            return transaction
    return None
