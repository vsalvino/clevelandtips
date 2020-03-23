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

1. Download a CSV from Google Forms/Sheets.

2. Run the data import script:
   ```
   python import.py
   ```

3. Review the `data.json` file diff before committing. Update any necessary
   data points such as website, and clean up misspellings, duplicates, etc.
