#!/usr/bin/env python

import sys

from os.path import abspath, join, split
from setuptools import setup

sys.path.insert(0, join(split(abspath(__file__))[0], 'lib'))
from cartas import __version__ as _cartas_version

setup(name='cartas',
      version=_cartas_version,
      description='Facilities to assist in plotting data per-country',
      author='N Lance Hepler',
      author_email='nlhepler@gmail.com',
      url='http://github.com/veg/cartas',
      license='GNU GPL version 3',
      packages=['cartas'],
      package_dir={'cartas': 'lib/cartas'},
      package_data={'cartas': ['data/*.json']},
      data_files=[('/usr/local/bin', [
            'bin/plotcartas'
      ])],
      requires=['countrymap', 'matplotlib', 'mpl_toolkits.basemap']
     )
