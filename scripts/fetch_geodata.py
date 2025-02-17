import requests
import json

geo_data = {
    "type": "FeatureCollection",
    "name": "World Country Subdivision Collection",
    "features": []
}

output = "provinces.geo.json"
url = "https://geodata.ucdavis.edu/gadm/gadm4.1/json/gadm41_{country_code}_{level}.json"

# List of countries we want to download subdivision data for.
countries = [
    ("DEU", 1),
    ("POL", 1),
    ("MKD", 0),
    ("NLD", 0),
    ("BEL", 1),
    ("LUX", 0),
    ("FRA", 1),
    ("CHE", 0),
    ("ITA", 1),
    ("CZE", 0),
    ("AUT", 0),
    ("SVN", 0),
    ("SVK", 0),
    ("HUN", 0),
    ("MDA", 0),
    ("SRB", 0),
    ("XKO", 0),
    ("MNE", 0),
    ("BIH", 0),
    ("HRV", 0),
    ("ALB", 0),
    ("GRC", 1),
    ("BGR", 0),
    ("ROU", 0),
    ("ESP", 1),
    ("PRT", 0),
    ("RUS", 1),
    ("DNK", 1),
    ("GBR", 1),
    ("IRL", 0),
    ("UKR", 0),
    ("BLR", 0),
    ("LVA", 0),
    ("LTU", 0),
    ("EST", 0),
    ("ISL", 0),
    ("FIN", 1),
    ("SWE", 0),
    ("NOR", 0),
    ("GRL", 0),
    ("MNG", 0),
    ("KAZ", 0),
    ("CHN", 1),
    ("KOR", 0),
    ("PRK", 0),
    ("TUR", 0),
    ("IND", 1),
    ("EGY", 0),
    ("LBY", 0),
    ("IRQ", 0),
    ("IRN", 0),
    ("SYR", 0),
    ("USA", 1),
    ("CAN", 1),
    ("MEX", 0),
    ("AUS", 1),
    ("NZL", 0),
    ("NPL", 0),
    ("MDG", 0),
    ("BRA", 1),
    ("COL", 0),
    ("VEN", 0),
    ("PER", 0),
    ("ARG", 0),
    ("CHL", 0),
    ("PAK", 0),
    ("BTN", 0)
]

# ID of a province.
id_counter = 0

# Download subdivision data for each country in the list.
for country in countries:
    print(f"Downloading data for {country[0]}")
    response = requests.get(
        url.format(country_code = country[0], level = country[1])
    )

    if response.status_code != 200:
        print(f"Failed to download data for {country[0]}")
        continue;
    
    country_data = response.json()["features"]

    for feature in country_data:
        # Some new properties we'll use.
        feature["properties"]["ID"] = id_counter
        feature["properties"]["NAME"] = "NA"

        if "NAME_1" in feature["properties"] and feature["properties"]["NAME_1"] != "NA":
            feature["properties"]["NAME"] = feature["properties"]["NAME_1"]
        elif "COUNTRY" in feature["properties"]:
            feature["properties"]["NAME"] = feature["properties"]["COUNTRY"]

        # Delete properties we won't need to save space in the file.
        feature["properties"].pop("GID_0", None)
        feature["properties"].pop("GID_1", None)
        feature["properties"].pop("COUNTRY", None)
        feature["properties"].pop("NAME_1", None)
        feature["properties"].pop("VARNAME_1", None)
        feature["properties"].pop("NL_NAME_1", None)
        feature["properties"].pop("TYPE_1", None)
        feature["properties"].pop("ENGTYPE_1", None)
        feature["properties"].pop("CC_1", None)
        feature["properties"].pop("HASC_1", None)
        feature["properties"].pop("ISO_1", None)

        id_counter += 1

    geo_data["features"].extend(country_data)

# Save geo data to a file.
with open(output, "w", encoding="utf-8") as f:
    json.dump(geo_data, f)
