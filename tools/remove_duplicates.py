from bibtexparser import BibTexParser
import os, textwrap

def format_bibtex_entry(entry):
    # field, format, wrap or not
    field_order = [(u'author', '{{{0}}},\n', True),
			(u'title', '{{{0}}},\n', True),
			(u'journal','"{0}",\n', True),
			(u'volume','{{{0}}},\n', True),
			(u'number', '{{{0}}},\n', True),
			(u'pages', '{{{0}}},\n', True),
			(u'year', '{0},\n', True),
			(u'doi','{{{0}}},\n', False),
			(u'url','{{\\url{{{0}}}}},\n', False),
			(u'link','{{\\url{{{0}}}}},\n', False)]

    keys = set(entry.keys())

    extra_fields = keys.difference([f[0] for f in field_order])
    # we do not want these in our entry
    extra_fields.remove('type')
    extra_fields.remove('id')

    # Now build up our entry string
    s = '@{type}{{{id},\n'.format(type=entry['type'].upper(),
                                  id=entry['id'])

    for field, fmt, wrap in field_order:
        if field in entry:
            s1 = '  {0} ='.format(field.upper())
            s2 = fmt.format(entry[field])
            s3 = '{0:17s}{1}'.format(s1, s2)
            if wrap:
                # fill seems to remove trailing '\n'
                s3 = textwrap.fill(s3, subsequent_indent=' '*18, width=70) + '\n'
            s += s3  

    for field in extra_fields:
        if field in entry:
            s1 = '  {0} ='.format(field.upper())
            s2 = entry[field]
            s3 = '{0:17s}{{{1}}}'.format(s1, s2)
            s3 = textwrap.fill(s3, subsequent_indent=' '*18, width=70) + '\n'
            s += s3  

    s += '}\n\n'
    return s

if os.path.exists('merged.bib'): os.unlink('merged.bib')    

with open(sys.argv[1], 'r') as bibfile:
    bp = BibTexParser(bibfile)
    entries1 = bp.get_entry_list()

for entry in entries1:
    with open('merged.bib', 'a') as f:
        f.write(format_bibtex_entry(entry))

# store keys to check for duplicates
entry1_keys = [entry['id'] for entry in entries1]

with open(sys.argv[2], 'r') as bibfile:
    bp = BibTexParser(bibfile)
    entries2 = bp.get_entry_list()

for entry in entries2:
    if not entry['id'] in entry1_keys:
        with open('merged.bib', 'a') as f:
            f.write(format_bibtex_entry(entry))
