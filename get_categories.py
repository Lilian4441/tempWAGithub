##############################################
# Looks through the det_train.json file and  #
# extracts all of the different categories   #
# so we can make sure each class is used     #
#                                            #
# It prints the output formatted as a Python #
# list to easily copy into test_parse.py     #
##############################################

import re

# change to the filename we want to find the categories in
filename = 'bdd100k_det_20_labels_trainval/bdd100k/labels/det_20/det_train.json'

def extract_categories(filename):
    categories = set()
    pattern = re.compile(r'"category":\s*"([^"]+)"')
    
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            match = pattern.search(line)
            if match:
                category = match.group(1)
                categories.add(category)
    
    return categories

print("running script...")

categories = extract_categories(filename)
print("Unique Categories Found:")

formatted_output = "classes = [" + ", ".join(f"'{category}'" for category in sorted(categories)) + "]"
print(str(sorted(categories)))