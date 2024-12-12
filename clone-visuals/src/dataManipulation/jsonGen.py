import json
import hashlib
from collections import defaultdict

def main():

    # Remove the path of your personal machine from the project path
    path_to_remove = "/Users/james/OneDrive/Desktop/SEseries/series2Rascal/series2jan/"
    lcos_per_file_path = "/Users/james/OneDrive/Desktop/SEseries/series2Rascal/series2jan/src/main/locPerFileTest.json"
    write_path = "../finalData/locsPerFilePath.json"
    remove_locs_per_file_personal_path(lcos_per_file_path, path_to_remove, write_path)

    clone_class_path = "/Users/james/OneDrive/Desktop/SEseries/series2Rascal/series2jan/src/main/cloneClassTest.json"
    write_path = "../finalData/cloneClassPath.json"
    remove_clone_class_personal_path(clone_class_path, path_to_remove, write_path)

    # Extract the code snippets and combine into one json
    clone_class_path = "../finalData/cloneClassPath.json"
    locs_per_file_path = "../finalData/locsPerFilePath.json"
    out_file = "../finalData/codeExample.json"
    extract_code_snippets(clone_class_path, locs_per_file_path, out_file)

    # Create the shared clones file 
    code_example_json = "../finalData/codeExample.json"
    shared_clones_json = "../finalData/sharedClones.json"
    generate_shared_clones(code_example_json, shared_clones_json)

    # Generate json for the bar chart 
    bar_char_json = "../finalData/barChart.json"
    generate_data_for_bar_chart(code_example_json, bar_char_json)

    # Reformat the json so it shows the hierarchy
    hierarchy_data = "../finalData/hierarchyData.json"
    reformat_to_show_structure(code_example_json, hierarchy_data)

    # Add percent of clones field 
    poc_data = "../finalData/pocData.json"
    calculate_poc(code_example_json, hierarchy_data, poc_data)

    # Replace the clones field with the files where those clones are located 
    tree_map_data = "../finalData/treeMap.json"
    update_clones_field(poc_data, shared_clones_json, tree_map_data)




# def traverse(node, result):
#         if 'children' in node:
#             for child in node['children']:
#                 traverse(child, result)
#         else:
#             result[node['name']] = node['clones']

# def extract_clones(data):
#     result = {}

#     for item in data:
#         traverse(item, result)

#     return result

# def get_clone_files(data):
#     result = {}
#     for clone in data:
#         result[clone] = data[clone]

#     return result

# def get_connected_clones(file_clones, clone_files):
#     connected_files = {}

#     # for file in file_clones:
#     #     connected_files[file] = set()
#     #     for clone in file_clones[file]:
#     #         for class_clone in clone_files[clone]:
#     #             connected_files[file].add(class_clone)

#     connected_files = {
#         file: {class_clone for clone in file_clones[file] for class_clone in clone_files[clone]}
#         for file in file_clones
#     }

#     return connected_files

# # Changes the clones feild in the json
# def replace_clones(data, connected_clones):
#     def traverse(node):
#         if 'children' in node:
#             for child in node['children']:
#                 traverse(child)
#         else:
#             if node['name'] in connected_clones:
#                 node['clones'] = connected_clones[node['name']]

#     for item in data:
#         traverse(item)

# def merge_json(initial_data, initial_shared_clones, output_file):
    
#     # Get what clones are in each file 
#     file_clones = extract_clones(initial_data)    

#     clone_files = get_clone_files(initial_shared_clones)

#     # print(file_clones) # {'File A': ['a', 'b', 'c', 'd'], 'File B': ['b', 'e', 'f']...}
#     # print(clone_files) # {'a': ['File A'], 'b': ['File A', 'File B'], 'c': ['File A', 'File B', 'File C']...

#     connected_clones = get_connected_clones(file_clones, clone_files)
    
#      # Convert sets to lists for JSON serialization
#     connected_clones = {file: list(clones) for file, clones in connected_clones.items()}

#     # Replace the clones field in the original data
#     replace_clones(initial_data, connected_clones)

#     with open(output_file, "w") as json_file:
#         json.dump(initial_data, json_file, indent=2)

# def add_depth(node, depth=0):
#     node['depth'] = depth
#     if 'children' in node:
#         for child in node['children']:
#             add_depth(child, depth + 1)

# def write_depth():
#     with open("data/connected_clones.json", "r") as json_file:
#         initial_connected_clones = json.load(json_file)

def remove_locs_per_file_personal_path(file_path, path_to_remove, write_path):
    
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Modify the paths
    for item in data:
        item[0]['path'] = item[0]['path'].replace(path_to_remove, '')

    # Write the updated data back to the file
    with open(write_path, 'w') as file:
        json.dump(data, file, indent=2)

def remove_clone_class_personal_path(file_path, path_to_remove, write_path):
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Modify the paths
    for item in data:
        item['path'] = item['path'].replace(path_to_remove, '')

    # Write the updated data back to the file
    with open(write_path, 'w') as file:
        json.dump(data, file, indent=2)

def generate_hash(value):
    return hashlib.md5(value.encode()).hexdigest()

def extract_code_snippets(clone_class_path_file, locs_per_file_path_file, output_file):
    # Load the JSON data from the files
    with open(clone_class_path_file, 'r') as file:
        clone_class_data = json.load(file)
    
    with open(locs_per_file_path_file, 'r') as file:
        locs_per_file_data = json.load(file)
    
    # Create a dictionary for quick lookup of locs per file data by path
    locs_per_file_dict = {item[0]['path']: item[1] for item in locs_per_file_data}
    
    # Prepare the output data
    output_data = []
    
    for clone in clone_class_data:
        path = clone['path']
        begin_line, begin_col = clone['begin']
        end_line, end_col = clone['end']
        
        # Get the lines of code from locs_per_file_data
        if path in locs_per_file_dict:
            lines = locs_per_file_dict[path][1]
            snippet_lines = lines[begin_line-1:end_line]
            
            # Adjust the first and last line to the correct columns
            snippet_lines[0] = snippet_lines[0][begin_col-1:]
            snippet_lines[-1] = snippet_lines[-1][:end_col]
            
            # Join the lines to form the code snippet
            code_snippet = ''.join(snippet_lines)
            
            # Calculate the clone size
            clone_size = end_line - begin_line + 1
            
            # Generate the hashes
            clone_id = generate_hash(f"{path}:{begin_line}-{end_line}")
            clone_hash = generate_hash(f"{code_snippet}")
            
            # Create the output entry
            output_entry = {
                'path': path,
                'size': locs_per_file_dict[path][0],
                'example': code_snippet,
                'cloneID': clone_id,
                'clone': clone_hash,
                'cloneSize': clone_size
            }
            output_data.append(output_entry)
    
    # Write the output data to the file
    with open(output_file, 'w') as file:
        json.dump(output_data, file, indent=2)

def generate_shared_clones(input_file, output_file):
    # Load the JSON data from the input file
    with open(input_file, 'r') as file:
        code_examples = json.load(file)
    
    # Create a dictionary to store the shared clones
    shared_clones = defaultdict(set)
    
    # Populate the dictionary with clone data
    for example in code_examples:
        clone_hash = example['clone']
        path = example['path']
        shared_clones[clone_hash].add(path)
    
    # Convert the sets to lists for JSON serialization
    shared_clones = {k: list(v) for k, v in shared_clones.items()}
    
    # Write the shared clones data to the output file
    with open(output_file, 'w') as file:
        json.dump(shared_clones, file, indent=2)

def generate_data_for_bar_chart(input_file, output_file):
    # Load the JSON data from the input file
    with open(input_file, 'r') as file:
        code_examples = json.load(file)
    
    # Create dictionaries to store the locCloneProduct and occurrences data
    loc_clone_product = defaultdict(int)
    occurrences = defaultdict(int)
    
    # Populate the dictionaries with locCloneProduct and occurrences data
    for example in code_examples:
        clone_hash = example['clone']
        clone_size = example['cloneSize']
        loc_clone_product[clone_hash] += clone_size
        occurrences[clone_hash] += 1
    
    # Prepare the output data
    output_data = []
    for clone_hash, total_clone_size in loc_clone_product.items():
        output_entry = {
            'clone': clone_hash,
            'occurrences': occurrences[clone_hash],
            'locCloneProduct': occurrences[clone_hash] * total_clone_size,
            'cloneSize': total_clone_size
        }
        output_data.append(output_entry)
    
    # Write the output data to the file
    with open(output_file, 'w') as file:
        json.dump(output_data, file, indent=2)


def reformat_to_show_structure(input_file, output_file):
    # Load the JSON data from the input file
    with open(input_file, 'r') as file:
        code_examples = json.load(file)
    
    # Create a dictionary to store the reformatted data
    reformatted_data = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    
    # Populate the dictionary with reformatted data
    for example in code_examples:
        path_parts = example['path'].split('/')
        root = path_parts[0]
        subdir = path_parts[1]
        filename = path_parts[2]
        
        reformatted_data[root][subdir][filename].append({
            'name': example['cloneID'],
            'size': example['size'],
            'clones': example['clone']
        })
    
    # Convert the dictionary to the desired format
    output_data = []
    for root, subdirs in reformatted_data.items():
        root_entry = {'name': root, 'children': []}
        for subdir, files in subdirs.items():
            subdir_entry = {'name': subdir, 'children': []}
            for filename, clones in files.items():
                clones_set = set()
                for clone in clones:
                    clones_set.add(clone['clones'])
                subdir_entry['children'].append({
                    'name': filename,
                    'size': clones[0]['size'],
                    'clones': list(clones_set)
                })
            root_entry['children'].append(subdir_entry)
        output_data.append(root_entry)
    
    # Write the output data to the file
    with open(output_file, 'w') as file:
        json.dump(output_data, file, indent=2)

def calculate_poc(code_example_file, hierarchy_data_file, output_file):
    # Load the JSON data from the files
    with open(code_example_file, 'r') as file:
        code_examples = json.load(file)
    
    with open(hierarchy_data_file, 'r') as file:
        hierarchy_data = json.load(file)
    
    # Create a dictionary to store the clone sizes
    clone_size_map = {}
    for example in code_examples:
        clone = example['clone']
        clone_size = example['cloneSize']
        clone_size_map[clone] = clone_size
    
    # Function to recursively update the hierarchy data with poc
    def update_poc(node):
        if 'children' in node:
            for child in node['children']:
                update_poc(child)
        else:
            total_clone_size = 0
            for clone in node.get('clones', []):
                if clone in clone_size_map:
                    total_clone_size += clone_size_map[clone]
            poc = (total_clone_size / node['size']) * 100 if node['size'] > 0 else 0
            node['poc'] = poc
    
    # Update the hierarchy data with poc
    for root in hierarchy_data:
        update_poc(root)
    
    # Write the updated hierarchy data to the output file
    with open(output_file, 'w') as file:
        json.dump(hierarchy_data, file, indent=2)

def update_clones_field(poc_data_file, shared_clones_file, output_file):
    # Load the JSON data from the files
    with open(poc_data_file, 'r') as file:
        poc_data = json.load(file)
    
    with open(shared_clones_file, 'r') as file:
        shared_clones = json.load(file)
    
    # Create a dictionary to store the file locations for each clone
    clone_locations = {}
    for clone, files in shared_clones.items():
        clone_locations[clone] = files
    
    # Function to recursively update the clones field in the hierarchy data
    def update_clones(node):
        if 'children' in node:
            for child in node['children']:
                update_clones(child)
        else:
            updated_clones = set()
            for clone in node.get('clones', []):
                if clone in clone_locations:
                    updated_clones.update(clone_locations[clone])
            node['clones'] = list(updated_clones)
    
    # Update the hierarchy data with the new clones field
    for root in poc_data:
        update_clones(root)
    
    # Write the updated hierarchy data to the output file
    with open(output_file, 'w') as file:
        json.dump(poc_data, file, indent=2)


main()