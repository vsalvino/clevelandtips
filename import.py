"""
Imports from CSV and alphabetizes the data.json file.

TODO: import from Google sheets CSV.
"""
import csv
import json
import os


def parse_username(username: str):
    """
    Parses URLs and usernames into a consistent format for paypal, venmo, cashapp.
    """
    # Strip trailing slashes and user symbols, then take part after last slash.
    return username.strip(" /@$").split("/")[-1]


# Load the current data file.
path = os.path.join("site", "data", "data.json")
data = []
with open(path, "r") as jfile:
    data = json.loads(jfile.read())

# Load the CSV form responses.
responses = []
with open("raw.csv", "r") as csvfile:
    rdr = csv.reader(csvfile)

    # Loop through rows
    rownum = 0
    for row in rdr:
        rownum += 1
        # Skip first row of titles.
        if rownum == 1:
            continue

        # Loop through columns
        record = {
            "name": "",
            "place": "",
            "paypal": "",
            "venmo": "",
            "cashapp": "",
            "phoneNumber": ""
        }
        colnum = 0
        for col in row:
            colnum += 1
            # Skip first column with date
            if colnum == 1:
                continue
            if colnum == 2:
                record["name"] = col.strip()
            if colnum == 3:
                record["place"] = col.strip()
            if colnum == 4:
                record["paypal"] = parse_username(col)
            if colnum == 5:
                record["venmo"] = parse_username(col)
            if colnum == 6:
                record["cashapp"] = parse_username(col)
            # Is phoneNumber col 7?
            if colnum == 7:
                record["phoneNumber"] = col.strip()

        # Add parsed response to the list.
        responses.append(record)

# Next, cross reference existing data and only add new names.)
for person in responses:
    place_exists = False
    pix = -1
    for place in data:
        pix += 1
        # If the place appears to match...
        if place["name"].lower() == person["place"].lower():
            place_exists = True
            # Then loop through existing workers and check.
            person_exists = False
            for worker in place["workers"]:
                if person["name"].lower() == worker["name"].lower():
                    person_exists = True
                    break
            # Add this worker.
            if not person_exists:
                data[pix]["workers"].append({
                    "name": person["name"],
                    "paypal": person["paypal"],
                    "venmo": person["venmo"],
                    "cashapp": person["cashapp"],
                    "phoneNumber": person["phoneNumber"]
                })

    # Add this new place and worker.
    if not place_exists:
        data.append({
            "name": person["place"],
            "website": "",
            "note": "",
            "workers": [{
                "name": person["name"],
                "paypal": person["paypal"],
                "venmo": person["venmo"],
                "cashapp": person["cashapp"],
                "phoneNumber": person["phoneNumber"]
            }]
        })

# Alphabetize the places.
data = sorted(data, key=lambda x: x["name"])

# Alphabetize the workers in each place.
for i in range(0, len(data)):
    data[i]["workers"] = sorted(data[i]["workers"], key=lambda x: x["name"])

# Write the file back.
with open(path, "w") as jfile:
    jfile.write(json.dumps(data, indent=2))

print(f"Written to {path}")
