#################################################
# Reads through the provided json labels and    #
# converts them into YOLO-formatted labels.     #
#                                               #
# Change the "json_file_path" and "output_dir"  #
# for each of training, validation, and testing #
# images.                                       #
#                                               #
# Also, run get_categories.py to make sure all  #
# classes are able to be identified, although   #
# the same classes are presumably used across   #
# training, validation, and testing sets.       #
#################################################

import json
import os
import shutil

# File paths
json_file_path = 'bdd100k_det_20_labels_trainval/bdd100k/labels/det_20/det_train.json'  # path to your JSON file
output_dir = 'yolo_labels/train/'  # Directory where YOLO labels will be saved
classes = ['bicycle', 'bus', 'car', 'motorcycle', 'other person', 'other vehicle', 'pedestrian',
            'rider', 'traffic light', 'traffic sign', 'trailer', 'train', 'truck']  # Define the classes

print("running script...")

print("removing existing files...")

# Ensure the output directory exists
if os.path.exists(output_dir):
    shutil.rmtree(output_dir)  # Remove any existing files
os.makedirs(output_dir)

# Helper function to get normalized coordinates
def convert_to_yolo_format(x1, y1, x2, y2, image_width, image_height):
    x_center = (x1 + x2) / 2 / image_width
    y_center = (y1 + y2) / 2 / image_height
    width = (x2 - x1) / image_width
    height = (y2 - y1) / image_height
    return x_center, y_center, width, height

print("reading JSON file...")

# Read the JSON file
with open(json_file_path, 'r') as f:
    json_data = json.load(f)

print("going through each entry in JSON data...")

# Iterate through each entry in the JSON data
for entry in json_data:
    image_name = entry['name']
    image_width = 1280  # Assume fixed image width (adjust as needed)
    image_height = 720  # Assume fixed image height (adjust as needed)
    
    # Prepare the label file for each image
    label_file_path = os.path.join(output_dir, f"{os.path.splitext(image_name)[0]}.txt")
    
    with open(label_file_path, 'w') as label_file:
        # Check if 'labels' exists in the current entry
        if 'labels' in entry:
            # Process each label in the image
            for label in entry['labels']:
                category = label['category']
                if category not in classes:
                    print(f'label {category} in image {image_name} was not in the predefined class list')
                    continue  # Skip labels not in the predefined classes
                
                # Convert category to class ID
                class_id = classes.index(category)

                # Get bounding box coordinates
                box = label['box2d']
                x1, y1, x2, y2 = box['x1'], box['y1'], box['x2'], box['y2']

                # Convert to YOLO format and write to the label file
                x_center, y_center, width, height = convert_to_yolo_format(x1, y1, x2, y2, image_width, image_height)
                label_file.write(f"{class_id} {x_center} {y_center} {width} {height}\n")
        else:
            print(f"No 'labels' key found in entry for image {image_name}, writing blank file")
            label_file.write("")

print("YOLO formatted labels have been generated.")
