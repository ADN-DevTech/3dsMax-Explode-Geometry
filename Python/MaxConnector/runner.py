import sys
import os
from optparse import OptionParser

packagesdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'packages')
sys.path.append(packagesdir)

import maxconnect

parser = OptionParser()
parser.add_option('-f', dest='filename', help='Maxscript FILENAME')

(options, args) = parser.parse_args()

if __name__ == '__main__':
    if options.filename:
        filename, extension = os.path.splitext(options.filename)
        if extension == '.py':
            cmd = r'python.ExecuteFile @"%s";' % options.filename
        elif extension == '.ms' or extension == '.mcr':
            cmd = r'fileIn @"%s";' % options.filename
        else:
            cmd = r'print "Invalid filetype";'
        maxconnect.pycharm.run(cmd)