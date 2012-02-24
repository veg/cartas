#!/usr/bin/env python3.2

import re, sys

assert len(sys.argv) == 2, "usage: minify.py HTMLFILE"

with open(sys.argv[1]) as fh:
    print(re.sub(r'([>;]) ([<a-z])', r'\1\2', re.sub(r'[ \t\n]+', ' ', fh.read())).strip())
