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

To use the data import script, install Python 3.6 or higher, and run:

```
python import.py
```

Then review the `data.json` file before committing.
