import os
from pprint import pprint
from glob import glob
import json

BOOK_DIR_PATH = '../../../data/scielobooks_sample/'

def largest_and_smallest_samples():
    sizes = []
    for data_path in glob(os.path.join(BOOK_DIR_PATH, '*')):
        _, book_id = os.path.split(data_path)
        sizes.append((os.stat(os.path.join(data_path, 'data.json')).st_size, book_id))

    sizes.sort()
    sizes.reverse()
    return (sizes[0], sizes[-1])

#pprint(largest_and_smallest_samples())

for size, book_id in largest_and_smallest_samples():
    in_path = os.path.join(BOOK_DIR_PATH, book_id, 'data.json')
    out_path = book_id+'.json'
    with open(in_path) as in_file, open(out_path, 'wb') as out_file:
        book_data = json.load(in_file)
        json.dump(book_data, out_file, indent=2)
