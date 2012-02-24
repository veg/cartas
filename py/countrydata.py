#!/usr/bin/env python3.2

import json, sys

from os.path import basename, join
from glob import glob


assert len(sys.argv) == 2, "usage: countrydata.py PATH_TO_PREDICTION_FILES"

path = sys.argv[1].rstrip('/')

files = glob(join(path, "*.pred"))

ab_files = [(basename(f).split('.')[0], f) for f in files]

ab_data = {}
for ab, f in ab_files:
    with open(f) as fh:
        ab_data[ab] = json.load(fh)

with open('iso2_to_text.json') as fh:
    iso2_to_text = json.load(fh)

countrydata = {}
for ab, data in ab_data.items():
    country_vals = {}
    for name, val in data["predictions"].items():
        # country = name.split('.')[1]
        country = iso2_to_text[name.split('.')[1]]
        if country not in countrydata:
            countrydata[country] = {}
        if ab not in countrydata[country]:
            countrydata[country][ab] = []
        countrydata[country][ab].append(val)

for country, data in countrydata.items():
    oldnum = None
    for ab, vals in data.items():
        num = len(vals)
        if oldnum is not None:
            assert(num == oldnum)
        oldnum = num
        avg = round( 100 * sum(vals) / num )
        countrydata[country][ab] = avg
    countrydata[country]['#'] = oldnum

print('var countrydata = ', end='')
json.dump(countrydata, sys.stdout)
print(';', end='')
