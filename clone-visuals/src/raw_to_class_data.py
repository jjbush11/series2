import json

def main():
    # Read in json data 
    with open("/home/jan/Nextcloud/uni/SEvolution/series2_james/clone-visuals/src/data/clone_classes_from_Rascal.json", "r") as json_file:
        raw_data = json.load(json_file)

    processed_data = []
    for item in raw_data:
        class_id = item["classID"]
        loc_size = int(item["locSize"])
        clone_count = len(item["clones"])
        loc_clone_product = loc_size * clone_count
        processed_data.append({
            "classID": class_id,
            "volume": loc_clone_product,
            "locSize": loc_size,
            "occurrences": clone_count
        })
    #Save the processed data to a JSON file
    output_file = "/home/jan/Nextcloud/uni/SEvolution/series2_james/clone-visuals/src/data/class_data.json"
    with open(output_file, "w") as f:
        json.dump(processed_data, f, indent=4)

    print(f"Processed data saved to {output_file}")


main()
