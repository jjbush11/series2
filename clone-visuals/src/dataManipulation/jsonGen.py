import json
import hashlib
from collections import defaultdict

def main():

 # Remove the path of your personal machine from the project path
    path_to_remove = "/Users/james/OneDrive/Desktop/SEseries/series2Rascal/series2jan/"
    lcos_per_file_path = "/home/jan/Nextcloud/uni/SEvolution/series2_james/clone-visuals/src/outputFromRascal/locPerFileTest.json"
    write_path = "/home/jan/Nextcloud/uni/SEvolution/series2_james/clone-visuals/src/finalData/locsPerFilePath.json"
    remove_locs_per_file_personal_path(lcos_per_file_path, path_to_remove, write_path)
    
    clone_class_path = "/home/jan/Nextcloud/uni/SEvolution/series2_james/clone-visuals/src/outputFromRascal/cloneClassTest.json"
    write_path = "/home/jan/Nextcloud/uni/SEvolution/series2_james/clone-visuals/src/finalData/cloneClassPath.json"
    remove_clone_class_personal_path(clone_class_path, path_to_remove, write_path)
    
    # Extract the code snippets and combine into one json
    clone_class_path = "/home/jan/Nextcloud/uni/SEvolution/series2_james/clone-visuals/src/finalData/cloneClassPath.json"
    locs_per_file_path = "/home/jan/Nextcloud/uni/SEvolution/series2_james/clone-visuals/src/finalData/locsPerFilePath.json"
    out_file = "/home/jan/Nextcloud/uni/SEvolution/series2_james/clone-visuals/src/finalData/codeExample.json"
    extract_code_snippets(clone_class_path, locs_per_file_path, out_file)
    
    # Create the shared clones file 
    code_example_json = "/home/jan/Nextcloud/uni/SEvolution/series2_james/clone-visuals/src/finalData/codeExample.json"
    shared_clones_json = "/home/jan/Nextcloud/uni/SEvolution/series2_james/clone-visuals/src/finalData/sharedClones.json"
    generate_shared_clones(code_example_json, shared_clones_json)
    
    # Generate json for the bar chart 
    bar_char_json = "/home/jan/Nextcloud/uni/SEvolution/series2_james/clone-visuals/src/finalData/barChart.json"
    generate_data_for_bar_chart(code_example_json, bar_char_json)
    
    # Reformat the json so it shows the hierarchy
    hierarchy_data = "/home/jan/Nextcloud/uni/SEvolution/series2_james/clone-visuals/src/finalData/hierarchyData.json"
    reformat_to_show_structure(code_example_json, hierarchy_data)
    
    # Add percent of clones field 
    poc_data = "/home/jan/Nextcloud/uni/SEvolution/series2_james/clone-visuals/src/finalData/pocData.json"
    calculate_poc(code_example_json, hierarchy_data, poc_data)
    
    # Replace the clones field with the files where those clones are located 
    tree_map_data = "/home/jan/Nextcloud/uni/SEvolution/series2_james/clone-visuals/src/finalData/treeMap.json"
    update_clones_field(poc_data, shared_clones_json, tree_map_data)


def remove_locs_per_file_personal_path(file_path, path_to_remove, write_path):
    
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # # Modify the paths
    # for item in data:
    #     item[0]['path'] = item[0]['path'].replace(path_to_remove, '')

    # Write the updated data back to the file
    with open(write_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=2)

def remove_clone_class_personal_path(file_path, path_to_remove, write_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Modify the paths
    for item in data:
        item['path'] = item['path'].replace(path_to_remove, '')

    # Write the updated data back to the file
    with open(write_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=2)

def generate_hash(value):
    return hashlib.md5(value.encode()).hexdigest()

def extract_code_snippets(clone_class_path_file, locs_per_file_path_file, output_file):
    # Load the JSON data from the files
    with open(clone_class_path_file, 'r', encoding='utf-8') as file:
        clone_class_data = json.load(file)
    
    with open(locs_per_file_path_file, 'r', encoding='utf-8') as file:
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
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(output_data, file, indent=2)

def generate_shared_clones(input_file, output_file):
    # Load the JSON data from the input file
    with open(input_file, 'r', encoding='utf-8') as file:
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
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(shared_clones, file, indent=2)

def generate_data_for_bar_chart(input_file, output_file):
    # Load the JSON data from the input file
    with open(input_file, 'r', encoding='utf-8') as file:
        code_examples = json.load(file)
    
    # Create dictionaries to store the locCloneProduct and occurrences data
    loc_clone_product = defaultdict(int)
    occurrences = defaultdict(int)
    clone_ids = {}
    next_clone_id = 1
    
    # Populate the dictionaries with locCloneProduct and occurrences data
    for example in code_examples:
        clone_hash = example['clone']
        clone_size = example['cloneSize']
        loc_clone_product[clone_hash] += clone_size
        occurrences[clone_hash] += 1
        if clone_hash not in clone_ids:
            clone_ids[clone_hash] = next_clone_id
            next_clone_id += 1
    
    # Prepare the output data
    output_data = []
    for clone_hash, total_clone_size in loc_clone_product.items():
        output_entry = {
            'clone': clone_hash,
            'cloneID': clone_ids[clone_hash],
            'occurrences': occurrences[clone_hash],
            'locCloneProduct': total_clone_size,
            'cloneSize': clone_size
        }
        output_data.append(output_entry)
    
    # Write the output data to the file
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(output_data, file, indent=2)


def reformat_to_show_structure(input_file, output_file):
    # Load the JSON data from the input file
    with open(input_file, 'r', encoding='utf-8') as file:
        code_examples = json.load(file)
    
    # Create a dictionary to store the reformatted data
    reformatted_data = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))
    
    # Populate the dictionary with reformatted data
    for example in code_examples:
        path_parts = example['path'].split('/')
        current_level = reformatted_data
        for part in path_parts[:-1]:
            if part not in current_level:
                current_level[part] = defaultdict(dict)
            current_level = current_level[part]
        filename = path_parts[-1]
        if filename not in current_level:
            current_level[filename] = []
        current_level[filename].append({
            'name': example['cloneID'],
            'size': example['size'],
            'clones': example['clone'],
            'path': example['path']
        })
    
    # Function to recursively convert the dictionary to the desired format
    def convert_to_hierarchy(data):
        result = []
        for key, value in data.items():
            if isinstance(value, dict):
                children = convert_to_hierarchy(value)
                result.append({'name': key, 'children': children})
            else:
                clones_set = set()
                for clone in value:
                    clones_set.add(clone['clones'])
                result.append({
                    'name': key,
                    'size': value[0]['size'],
                    'path': value[0]['path'],
                    'clones': list(clones_set)
                })
        return result
    
    # Convert the dictionary to the desired format
    output_data = convert_to_hierarchy(reformatted_data)
    
    # Write the output data to the file
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(output_data, file, indent=2)

def calculate_poc(code_example_file, hierarchy_data_file, output_file):
    # Load the JSON data from the files
    with open(code_example_file, 'r', encoding='utf-8') as file:
        code_examples = json.load(file)
    
    with open(hierarchy_data_file, 'r', encoding='utf-8') as file:
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
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(hierarchy_data, file, indent=2)

def update_clones_field(poc_data_file, shared_clones_file, output_file):
    # Load the JSON data from the files
    with open(poc_data_file, 'r', encoding='utf-8') as file:
        poc_data = json.load(file)
    
    with open(shared_clones_file, 'r', encoding='utf-8') as file:
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
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(poc_data, file, indent=2)


main()