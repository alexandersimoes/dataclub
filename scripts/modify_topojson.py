import os, json

regions = {}

path = "dataviva/static/json/coords/bra/"
for filename in os.listdir(path):
    if ".json" == filename[-5:]:
        region = filename.split("_")[1][0]
        state = filename.split("_")[1][1:]
        regions[state] = region

path = "dataviva/static/json/coords/wld/"
for filename in os.listdir(path):
    if ".json" == filename[-5:]:

        print filename

        with open(path + filename, "r") as f:
            data = json.load(f)

            data["objects"]["geojson"] = data["objects"]["bra_states"]
            del data["objects"]["bra_states"]

            for row in data["objects"]["geojson"]["geometries"]:
                print regions[row["bra_id"]], row["bra_id"]
                row["id"] = regions[row["bra_id"]] + row["bra_id"]
                del row["bra_id"]
                del row["properties"]
                # row["id"] = row["bra_9"]
                # del row["bra_9"]
                # row["bra_id"] = region + row["bra_id"]

        with open(path + filename, "w") as f:
            f.write(json.dumps(data))
