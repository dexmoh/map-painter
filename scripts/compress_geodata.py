import json
import math

in_file = "provinces.geo.json"
out_file = "provinces_compressed.geo.json"

# Calculate a distance between two points on Earth.
def haversine(lat1, lon1, lat2, lon2):
    # Radius of the Earth in kilometers
    R = 6371.0
    
    # Convert latitude and longitude from degrees to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    # Differences in coordinates
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    # Haversine formula
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return R * c # km

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
                if len(points) < 50:
                    continue

                new_points = []
                for l, point in enumerate(points):
                    if (l == 0) or ((l + 1) >= len(points)):
                        new_points.append(point)
                        continue

                    if haversine(point[0], point[1], points[l + 1][0], points[l + 1][1]) > 1.0:
                        new_points.append(point)

                compressed_data["features"][i]["geometry"]["coordinates"][j][k] = new_points
    
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(compressed_data, f)

if __name__ == "__main__":
    main()
