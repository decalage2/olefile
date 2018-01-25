#!/usr/bin/env python

import pypandoc


PKG_ROOT = 'olefile'

EXTRA_ARGS = ['--standalone']
HTML = 'html'

def convert_md(src, dest, fmt):
    print('CONVERTING %s to %s' % (src, dest))
    md = open(src).read()
    # remove lines with ":::python" or ":::text":
    lines = []
    for line in md.splitlines():
        if not(":::python" in line) and not (":::text" in line):
            lines.append(line)
    md = '\n'.join(lines)
    out = pypandoc.convert(md, format='markdown-smart', to=fmt, outputfile=dest,
        extra_args=EXTRA_ARGS)
    assert out==''
    # print out
    # f = open(dest, 'w')
    # f.write(out)
    # f.close()

# README md => rst, html
src = 'README.md'
dest = 'README.rst' # os.path.join(PKG_ROOT, 'README.rst')
convert_md(src, dest, 'rst-smart')

dest = 'README.html' # os.path.join(PKG_ROOT, 'README.html')
convert_md(src, dest, HTML)

