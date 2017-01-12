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
    args = arg_parser.parse_args()

    # Load databases
    db = FileBibDB(args.bib.name, mode='r')

    # Print entries
    for entry in db.values():
        rename_file(entry, args.pdf.name, args.bib.name)
        break

def rename_file(entry, pdf, bib):
    if entry['author']:
        authors = entry['author'].split(',')
        if len(authors) <= 3:
            author = ', '.join(authors[:-1])
        else:
            author = authors[0] + ' et al.'

        print (author)

    if author and 'year' in entry and 'title' in entry:
        newname = author + ' - ' + '{}'.format(entry['year']) + ' - ' + algo.tex_to_unicode(algo.title_case(entry['title'])).replace("/", " ") + '.pdf'

        if os.path.exists(pdf):
            shutil.copy2(pdf, os.getcwd() + '/' +  newname)
            shutil.move(pdf, os.path.expanduser("~") + '/.local/share/Trash/files/')
            shutil.move(bib, os.path.expanduser("~") + '/.local/share/Trash/files/')


if __name__ == '__main__':
    main()
