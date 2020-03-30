# Cleveland Virtual Tip Jar

Code for website at https://clevelandtips.com/

## Volunteers - Developers

**We need help processing submissions and cleaning data!** To volunteer, please
make a pull request updating this README to sign up for a shift importing and
reviewing data. Then at the designated time, follow the steps below and make a
pull request when complete. Each shift normally takes about 30 minutes.

Please do a fresh pull or make a fresh fork before each shift, as the import
script and README tend to change frequently as improvements are made.

| Shift              | GitHub User     |
| ------------------ | ------------    |
| Monday mornings    | @roxcoldiron    |
| Monday evenings    |                 |
| Tuesday mornings   | @vsalvino       |
| Tuesday evenings   | @nathanbardwell |
| Wednesday mornings | @roxcoldiron    |
| Wednesday evenings | @shawninman     |
| Thursday mornings  | @vsalvino       |
| Thursday evenings  | @nathanbardwell |
| Friday mornings    | @shawninman     |
| Friday evenings    | @samsawan       |
| Saturday mornings  | @vsalvino       |
| Saturday evenings  |                 |
| Sunday mornings    | @samsawan       |
| Sunday evenings    | @shawninman     |

Code is in a static HTML page in `site/` directory, rendered client-side with
Vue.js.

Data is located in `site/data/data.json`. Data is imported and cleaned via
`import.py` script which does most of the heavy lifting. If you'd like to
contribute data, make a pull request or submit your info from the form link on
https://clevelandtips.com/.

Data pull requests will be accepted providing that the data is in
**alphabetical** order.

## Steps for Importing and Reviewing Submissions

Install Python 3.6 or higher, then:

(Optional) Download a CSV from our [Google Sheet](https://docs.google.com/spreadsheets/d/1EPQ4uAyxqMYW8dEPVfduenf48ItutJkJxIXOsFdHXpE/edit?usp=sharing)
(read only, it is populated by the signup form) and place it in this
directory named `raw.csv`.

1. Run the data import script:

   ```
   python import.py --download
   ```

   This script will download the latest data from the Google Sheet and
   alphabetize all entries.

2. Review the `data.json` file diff before committing. Update any necessary
   data points such as website, and clean up misspellings, duplicates,
   proper capitalization, etc.

   Add common misspellings or alternate place names in the `alias` key in a list
   and rerun the scrip to automatically merge places.

   If a place or a person needs to be removed from the list, add a `hide: true`
   key to the place or person entry.

   It is helpful to view this file in a visual diff tool, such as VS Code. This
   is the most labor intensive part and where we need the most help.

3. Run the site locally using a web server, such as:

   ```
   python -m http.server -d site 8000
   ```

   Then go to http://localhost:8000/ and make sure it loads correctly with your
   updated data. If it does not load, there is most likely a syntax error in the
   JSON file.

4. Commit the changes and make a pull request.
