import json

def main():
     # Read in json data 
    with open("data/data2.json", "r") as json_file:
        data = json.load(json_file)
   
    with open("data/shared_clones.json", "r") as json_file:
        shared_clones = json.load(json_file)

    # Get what clones are in each file 
    file_clones = extract_clones(data)    

    clone_files = get_clone_files(shared_clones)

    # print(file_clones) # {'File A': ['a', 'b', 'c', 'd'], 'File B': ['b', 'e', 'f']...}
    # print(clone_files) # {'a': ['File A'], 'b': ['File A', 'File B'], 'c': ['File A', 'File B', 'File C']...

    connected_clones = get_connected_clones(file_clones, clone_files)
    
     # Convert sets to lists for JSON serialization
    connected_clones = {file: list(clones) for file, clones in connected_clones.items()}

    # Replace the clones field in the original data
    replace_clones(data, connected_clones)

    with open("data/connected_clones.json", "w") as json_file:
        json.dump(data, json_file, indent=2)
    




def traverse(node, result):
        if 'children' in node:
            for child in node['children']:
                traverse(child, result)
        else:
            result[node['name']] = node['clones']

def extract_clones(data):
    result = {}

    for item in data:
        traverse(item, result)

    return result

def get_clone_files(data):
    result = {}
    for clone in data:
        result[clone] = data[clone]

    return result

def get_connected_clones(file_clones, clone_files):
    connected_files = {}

    # for file in file_clones:
    #     connected_files[file] = set()
    #     for clone in file_clones[file]:
    #         for class_clone in clone_files[clone]:
    #             connected_files[file].add(class_clone)

    connected_files = {
        file: {class_clone for clone in file_clones[file] for class_clone in clone_files[clone]}
        for file in file_clones
    }

    return connected_files

# Changes the clones feild in the json
def replace_clones(data, connected_clones):
    def traverse(node):
        if 'children' in node:
            for child in node['children']:
                traverse(child)
        else:
            if node['name'] in connected_clones:
                node['clones'] = connected_clones[node['name']]

    for item in data:
        traverse(item)

main()