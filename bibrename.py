#!/usr/bin/env python3

import os.path

from biblib import FileBibDB, Entry

# FIXME: this is ugly, algo.py and messages.py should be removed
import algo

import argparse
import shutil
import sys
import re

papers_path = '/Documents/papers/'

def main():
    # We want to use the file tag
    Entry.processedTags.append('file')
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
    db = FileBibDB(args.bib.name, method = 'force', mode = 'r')

    entry = list(db.values())[-1]
    if rename_file(entry, args.pdf.name, args.bib.name, args.dry_run):
        for key, value in entry.items():
            print (str(key) + ">" + str(value))
        print (db.ckeys)
        #db.add_entry(entry, entry.ckey, method = 'force')

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
            shutil.copy2(pdf, os.path.expanduser("~") + papers_path +  newname)
            entry.set_tag('file', ':' + pdf + ':PDF' )

            if not dry_run:
                shutil.move(pdf, os.path.expanduser("~") + '/.local/share/Trash/files/')
                return True
    return False

if __name__ == '__main__':
    main()
