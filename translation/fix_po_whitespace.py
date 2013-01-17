#!/usr/bin/env python

"""
Look for trailing whitespace-only lines that the translator didn't add to the
msgstr in a PO file.

Warning: this is destructive, so make sure your PO is versioned or you
have a backup.

Usage: ./fix_po_whitespace.py path/to/file.po
"""

import sys
import re

whitespace = re.compile(r'^\s*$')
trailing = re.compile(r'^" +"$')


def add_po_whitespace(fh):
    buffer = []

    look_for_whitespace = False
    current_trailing = None

    for line in fh:
        if line.startswith('msgid "'):
            look_for_whitespace = True
        elif trailing.match(line) and look_for_whitespace:
            current_trailing = line
            look_for_whitespace = False
        elif current_trailing and whitespace.match(line):
            buffer.append(current_trailing)
            current_trailing = None

        buffer.append(line)

    return ''.join(buffer)


if __name__ == '__main__':
    fh = open(sys.argv[1])
    new_content = add_po_whitespace(fh)
    fh.close()

    with open(sys.argv[1], 'w') as fh:
        fh.write(new_content)
