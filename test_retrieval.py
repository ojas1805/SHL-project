import json

with open("data/shl_catalog_fixed.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print("Total assessments:", len(data))
print("First assessment:", data[0]["name"])
print("Last assessment:", data[-1]["name"])
