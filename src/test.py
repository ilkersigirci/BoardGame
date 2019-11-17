import json
result = {"cells":[],"players":[]}
#result = {}
#result["cells"] = {}
#esult["cell_desp"].add({"cellNo":3,"cellDescription":2})
result["cells"].append({"cellNo":3,"cellDescription":2})
result["cells"].append({"cellNo":2,"cellDescription":3})
#result["cells"]["cell2"] = {"cellNo":2,"cellDescription":3}

print(json.dumps(result, indent = 4))
