#!/usr/bin/env python3

import os.path

from biblib import FileBibDB

import algo

import argparse
import shutil
import sys
import re

def main():
    arg_parser = argparse.ArgumentParser(
        description='Rename a .pdf based on the content of a .bib first entry')
    arg_parser.add_argument('--bib', required=True, help='.bib file(s) to process',
                            type=open)
    arg_parser.add_argument('--pdf', required=True, help='.pdf file to rename',
                            type=open)
    arg_parser.add_argument('--last', help='use last key', action="store_true", default=False)
    arg_parser.add_argument('--key', help='cite key to use', action="store", dest="key")
    arg_parser.add_argument('--dry-run', help='do not remove any files', action="store_true", default=False)
    args = arg_parser.parse_args()
    print (args)

    # Load databases
    db = FileBibDB(args.bib.name, mode='r')

    # Print entries
    # TODO: get entry based on the method (last, key etc)
    for entry in db.values():
        rename_file(entry, args.pdf.name, args.bib.name, args.dry_run)
        break

def rename_file(entry, pdf, bib, dry_run):
    if entry['author']:
        authors = entry['author'].split(',')
        if len(authors) <= 3:
            author = ', '.join(authors[:-1])
        else:
            author = authors[0] + ' et al.'

    if author and 'year' in entry and 'title' in entry:
        newname = author + ' - ' + '{}'.format(entry['year']) + ' - ' + algo.tex_to_unicode(algo.title_case(entry['title'])).replace("/", " ") + '.pdf'

        if os.path.exists(pdf):
            shutil.copy2(pdf, os.getcwd() + '/' +  newname)

            if not dry_run:
                shutil.move(pdf, os.path.expanduser("~") + '/.local/share/Trash/files/')
                shutil.move(bib, os.path.expanduser("~") + '/.local/share/Trash/files/')
                print ("Files moved")


if __name__ == '__main__':
    main()
