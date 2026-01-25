import time
from xml_parser import xmlParsing
from search_linear import linear_search
from search_dict import transaction_dictionary, dict_lookup

def run_performance_test():
    transactions = xmlParsing('modified_sms_v2.xml')
    transactions_dict = transaction_dictionary(transactions)

    target_ids = [t['id'] for t in transactions[:20]]

    start = time.perf_counter()
    for tid in target_ids:
        linear_search(transactions, tid)
    linear_time = time.perf_counter() - start

    start = time.perf_counter()
    for tid in target_ids:
        dict_lookup(transactions_dict, tid)
    dict_time = time.perf_counter() - start

    print(f"Results for 20 Records:")
    print(f"Linear Search Time: {linear_time:.8f}s")
    print(f"Dictionary Lookup Time: {dict_time:.8f}s")
    print(f"Efficiency Gain: {linear_time / dict_time:.2f}x faster")

if __name__ == "__main__":
    run_performance_test()
