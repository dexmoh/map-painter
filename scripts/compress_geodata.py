import json

# Number of vertices the program will 'skip' over,
# higher number results in more compression and less detail.
compression_level = 3

in_file = "provinces.geo.json"
out_file = "provinces_compressed.geo.json"

def main():
    data = {}
    with open(in_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not data:
        print("The data file is empty, or doesnt exist. Quitting...")
        return
    
    compressed_data = data.copy()
    
    # Loop through data for every province.
    for i, feature in enumerate(data["features"]):
        for j, polygons in enumerate(feature["geometry"]["coordinates"]):
            for k, points in enumerate(polygons):
                compressed_data["features"][i]["geometry"]["coordinates"][j][k] = points[::compression_level]
    
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(compressed_data, f)

if __name__ == "__main__":
    main()
