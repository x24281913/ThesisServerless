from __future__ import absolute_import
import optparse
import sys
import re
import os
from .diff import htmldiff
description = ''
parser = optparse.OptionParser(usage='%prog [OPTIONS] FILE1 FILE2\n%prog --annotate [OPTIONS] INFO1 FILE1 INFO2 FILE2 ...', description=description)
parser.add_option('-o', '--output', metavar='FILE', dest='output', default='-', help='File to write the difference to')
parser.add_option('-a', '--annotation', action='store_true', dest='annotation', help='Do an annotation')

def main(args=None):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('lxml.html._diffcommand.main', 'main(args=None)', {'sys': sys, 'parser': parser, 'annotate': annotate, 'read_file': read_file, 'split_body': split_body, 'htmldiff': htmldiff, 'args': args}, 1)

def read_file(filename):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('lxml.html._diffcommand.read_file', 'read_file(filename)', {'sys': sys, 'os': os, 'filename': filename}, 1)
body_start_re = re.compile('<body.*?>', re.I | re.S)
body_end_re = re.compile('</body.*?>', re.I | re.S)

def split_body(html):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('lxml.html._diffcommand.split_body', 'split_body(html)', {'body_start_re': body_start_re, 'body_end_re': body_end_re, 'html': html}, 3)

def annotate(options, args):
    print('Not yet implemented')
    sys.exit(1)

