#!/usr/bin/env python

"""
Look for trailing whitespace-only lines that the translator didn't add to the
msgstr in a PO file.

Warning: this is destructive, so make sure your PO is versioned or you
have a backup. Also, it's by no means complete and correct, always do
manual double checking.

Usage: ./fix_po_whitespace.py path/to/file.po
"""

import sys
import re

whitespace = re.compile(r'^\s*$')
trailing = re.compile(r'^" +"$')
translation_string = re.compile(r'"\S+"')


def add_po_whitespace(fh):
    buffer = []

    look_for_whitespace = False
    current_trailing = None
    look_for_translation = False
    has_translation = False
    added_whitespace = 0

    for line in fh:
        if line.startswith('msgid "'):
            look_for_whitespace = True
            look_for_translation = False
            has_translation = False
        elif trailing.match(line) and look_for_whitespace:
            current_trailing = line
            look_for_whitespace = False
        elif line.startswith('msgstr'):
            look_for_translation = True
        elif current_trailing and whitespace.match(line) and has_translation:
            buffer.append(current_trailing)
            added_whitespace += 1
            current_trailing = None

        if look_for_translation and translation_string.search(line):
            has_translation = True

        buffer.append(line)

    print 'added %s whitespace lines' % added_whitespace

    return ''.join(buffer)


if __name__ == '__main__':
    fh = open(sys.argv[1])
    new_content = add_po_whitespace(fh)
    fh.close()

    with open(sys.argv[1], 'w') as fh:
        fh.write(new_content)
