import os, json

ids = {}

filename = "dataviva/static/json/networks/network_cnae.json"
with open(filename, "r") as f:
    data = json.load(f)

    # for i, node in enumerate(data["nodes"]):
        # node["cnae_6"] = node["cnae_id"]
        # del node["cnae_id"]
        # node["x"] = float(node["x"])
        # node["y"] = float(node["y"])
        # print node
    #     node_id = node["hs_id"]
    #     del node["hs_id"]
    #     node["hs_6"] = node_id
    #     ids[i] = node_id
    #
    for edge in data["edges"]:
        print edge
    #     edge["source"] = ids[edge["source"]]
    #     edge["target"] = ids[edge["target"]]

# with open(filename, "w") as f:
#     f.write(json.dumps(data))
