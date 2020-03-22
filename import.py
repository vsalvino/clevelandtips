"""
Imports from CSV and alphabetizes the data.json file.

TODO: import from Google sheets CSV.
"""
import json
import os

# Load the data file.
path = os.path.join("site", "data", "data.json")
data = []
with open(path, "r") as jfile:
  data = json.loads(jfile.read())

# Alphabetize the places.
data = sorted(data, key=lambda x: x["name"])

# Alphabetize the workers in each place.
for i in range(0, len(data)):
  data[i]["workers"] = sorted(data[i]["workers"], key=lambda x: x["name"])

# Write the file back.
with open(path, "w") as jfile:
  jfile.write(json.dumps(data, indent=2))

print(f"Written to {path}")
