#!/usr/bin/python

import StringIO
import settings
import os
import optparse
import re

def update_version():
    input = open('app.yaml','rb')
    out = StringIO.StringIO()
    repl = re.compile('[^a-z\d\-]')
    for line in input:
        if line.startswith('version'):
            out.write('version: %s\n' % repl.sub('', settings.VERSION))
        else:
            out.write(line)
    input.close()
    fileout = open('app.yaml','wb')
    fileout.write(out.getvalue())
    fileout.close()
    out.close()

def main():
    update_version()
    if settings.APP_ID:
        os.system('appcfg.py update . -A %s ' % settings.APP_ID)
    else:
        os.system('appcfg.py update .')
    
if __name__ == '__main__':
    main()
