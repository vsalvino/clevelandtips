"""
Imports from CSV and alphabetizes the data.json file.

This script is wildly hacky and inefficient ¯\_(ツ)_/¯
"""
import csv
import json
import os
import re
import string
import sys
import urllib.request


def string_for_compare(val: str) -> str:
    junk = list(string.digits + string.punctuation + "–—“”‘’") + [" a ", " and ", " at ", " by ", " in ", " on ", " the "]
    # lowercase.
    val = val.lower().strip()
    # Strip preceding The's
    if val.startswith("the "):
        val = re.sub(r"^the ", "", val)
    # Strip junk words/characters.
    for item in junk:
        val = val.replace(item, "")
    # Finally strip all spaces.
    val = val.replace(" ", "")
    return val


def parse_username(username: str):
    """
    Parses URLs and usernames into a consistent format for paypal, venmo, cashapp.
    """
    # If URL is a venmo code, try to resolve it.
    if username.startswith("https://venmo.com/code?user_id"):
        try:
            username = urllib.request.urlopen(username).url
        except:
            pass
    # Strip querystrings
    elif username.startswith("https://"):
        username = username.split("?")[0]
    # Strip trailing slashes and user symbols, then take part after last slash.
    return username.strip(" /").split("/")[-1].strip("@$")


# Download CSV.
if "--download" in str(sys.argv):
    print("Downloading latest data from Google Sheets...")
    url = "https://docs.google.com/spreadsheets/d/1EPQ4uAyxqMYW8dEPVfduenf48ItutJkJxIXOsFdHXpE/gviz/tq?tqx=out:csv&sheet=Form+Responses+1"
    urllib.request.urlretrieve(url, "raw.csv")
else:
    print("Use the `--download` flag to download the latest data")


# Load the current data file.
path = os.path.join("site", "data", "data.json")
data = []
with open(path, "r", encoding="utf-8") as jfile:
    data = json.loads(jfile.read())


# Load the CSV form responses.
responses = []
if os.path.exists("raw.csv"):
    print("Churning through CSV of responses...")
    with open("raw.csv", "r", encoding="utf-8") as csvfile:
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
                "last4": ""
            }
            colnum = 0
            for col in row:
                colnum += 1
                # Skip first column with date
                if colnum == 1:
                    continue
                # Normalize people names.
                if colnum == 2:
                    record["name"] = col.strip().replace("  ", " ")
                # Normalize place names.
                if colnum == 3:
                    record["place"] = col.strip().title()\
                        .replace("'S", "\u2019s")\
                        .replace("\u2019S", "\u2019s")\
                        .replace("  ", " ")\
                        .replace(" and ", " & ")\
                        .replace(" + ", " & ")
                if colnum == 4:
                    record["paypal"] = parse_username(col)
                if colnum == 5:
                    record["venmo"] = parse_username(col)
                if colnum == 6:
                    record["last4"] = col.strip()
                if colnum == 7:
                    record["cashapp"] = parse_username(col)

            # Add parsed response to the list, if they contain valid data.
            if record["paypal"] or record["venmo"] or record["cashapp"]:
                responses.append(record)

# Next, cross reference existing data and only add new names.
for person in responses:
    person_exists = False
    # Loop through all existing workers.
    for place in data:
        for worker in place["workers"]:
            # prevent duplicate entries with same name or app username
            if (
                person["name"].lower() == worker["name"].lower()
                or (person["paypal"] and person["paypal"].lower() == worker["paypal"].lower())
                or (person["venmo"] and person["venmo"].lower() == worker["venmo"].lower())
                or (person["cashapp"] and person["cashapp"].lower() == worker["cashapp"].lower())
            ):
                person_exists = True
                break
        if person_exists:
            break

    # If person does not already exist, add them to the appropriate place.
    if not person_exists:
        place_exists = False
        pix = -1
        for place in data:
            pix += 1
            # Do a basic place comparison by stripping punctuation, prepositions, articles, etc.,
            # or evaluate aliases.
            place_comp = string_for_compare(place["name"])
            person_place_comp = string_for_compare(person["place"])
            aliases = [string_for_compare(x) for x in place.get("alias", [])]
            if person["place"] in aliases or place_comp == person_place_comp:
                place_exists = True
                # Add this worker.
                data[pix]["workers"].append({
                    "name": person["name"],
                    "paypal": person["paypal"],
                    "venmo": person["venmo"],
                    "cashapp": person["cashapp"],
                    "last4": person["last4"],
                })
                # Add a place alias.
                if place["name"].lower() != person["place"].lower():
                    if "alias" in data[pix].keys():
                        if person["place"] not in data[pix]["alias"]:
                            print(f"Adding alias to {place['name']}: '{person['place']}'")
                            data[pix]["alias"].append(person["place"])
                    else:
                        print(f"Adding alias to {place['name']}: '{person['place']}'")
                        data[pix]["alias"] = [person["place"]]
                break

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
                    "last4": person["last4"],
                }]
            })

# Alphabetize the places.
data = sorted(data, key=lambda x: x["name"])

# Alphabetize the workers in each place.
delete_places = []
for i in range(0, len(data)):

    # Merge duplicated restraunts using known aliases
    if "alias" in data[i].keys():
        known_as = [string_for_compare(x) for x in data[i].get("alias", [])]

        for ix in range(0, len(data)):
            if (
                data[i]["name"] != data[ix]["name"] and
                string_for_compare(data[ix]["name"]) in known_as
            ):
                print("Merging {} into {}".format(data[ix]["name"], data[i]["name"]))
                data[i]["workers"] += data[ix]["workers"]
                delete_places.append(data[ix]["name"])

    data[i]["workers"] = sorted(data[i]["workers"], key=lambda x: x["name"])

# Delete merged places.
new_data = []
for place in data:
    if place["name"] not in delete_places:
        new_data.append(place)
data = new_data

# Write the file back.
with open(path, "w") as jfile:
    jfile.write(json.dumps(data, indent=2))

print("")
print(f"Written to {path}")
