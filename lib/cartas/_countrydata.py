#!/usr/bin/env python3.2

import json, sys

from os.path import abspath, basename, dirname, join
from glob import glob


__all__ = ['collate_countrydata']


def collate_countrydata(path, iso2=False):

    path = path.rstrip('/')

    files = glob(join(path, "*.pred"))

    ab_files = [(basename(f).split('.')[0], f) for f in files]

    ab_data = {}
    for ab, f in ab_files:
        with open(f) as fh:
            ab_data[ab] = json.load(fh)

    if not iso2:
        with open(join(dirname(abspath(__file__)), 'data', 'iso2_to_text.json')) as fh:
            iso2_to_text = json.load(fh)

    countrydata = {}
    for ab, data in ab_data.items():
        country_vals = {}
        for country, val in data["predictions"].items():
            country = country.split('.')[1]
            if country == '-':
                pass
            try:
                if not iso2:
                    country = iso2_to_text[country]
                if country not in countrydata:
                    countrydata[country] = {}
                if ab not in countrydata[country]:
                    countrydata[country][ab] = []
                countrydata[country][ab].append(val)
            except KeyError:
                pass

    for country, data in countrydata.items():
        oldnum = None
        for ab, vals in data.items():
            num = len(vals)
            if oldnum is not None:
                assert(num == oldnum)
            oldnum = num
#             avg = round( 100 * sum(vals) / num )
#             countrydata[country][ab] = avg
        countrydata[country]['#'] = oldnum

    return countrydata


if __name__ == '__main__':
    assert len(sys.argv) == 2, "usage: countrydata.py PATH_TO_PREDICTION_FILES"
    countrydata = collate_countrydata(sys.argv[1])
    print('var countrydata = ', end='')
    json.dump(countrydata, sys.stdout)
    print(';', end='')
    sys.exit(0)
