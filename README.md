Cleveland Virtual Tip Jar
=========================

Code for website at https://clevelandtips.com/


Contributing
------------

Code is in a static HTML page in `site/` directory, rendered client-side with
Vue.js.

Data is located in `site/data/data.json`. Data is imported and cleaned via
`import.py` script. If you'd like to contribute data, make a pull request
or submit your info from the form link on https://clevelandtips.com/.

Data pull requests will be accepted providing that the data is in
**alphabetical** order.

To use the data import script, install Python, then:

1. Download a CSV from Google Forms/Sheets and place it in this directory named
   `raw.csv`.

2. Run the data import script:
   ```
   python import.py
   ```
   This script will also alphabetize all entries.

3. Review the `data.json` file diff before committing. Update any necessary
   data points such as website, and clean up misspellings, duplicates,
   proper capitalization, etc. It is helpful to view this file in a visual diff
   tool, such as VS Code. This is the most labor intensive part and where we
   need the most help.

4. Run the site locally using a web server, such as:
   ```
   python -m http.server -d site 8000
   ```
   Then go to http://localhost:8000/ and make sure it loads correctly with your
   updated data. If it does not load, there is most likely a syntax error in the
   JSON file.

5. Commit the changes and make a pull request.
