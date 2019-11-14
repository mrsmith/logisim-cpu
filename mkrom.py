#!/usr/bin/env python3

import sys
import argparse as ap
import logging as log
from pprint import pprint, pformat
from os.path import dirname, splitext, join as pjoin

def parse_args():
    p = ap.ArgumentParser()
    p.add_argument('--rom-template', type=str, default=None, help='template for the ROM file')

    p.add_argument('fname', type=str, help='a.out machine code for ROM image')
    p.add_argument('-o', type=str, default=None, help='ROM output')

    return p.parse_args()

def read(fname):
    with open(fname) as fd:
        return fd.read()

def read_a_out(fname):
    with open(fname) as fd:
        hdr = fd.readline()
        assert hdr.strip() == 'v2.0 raw'

        for line in fd:
            yield line.strip()

def main():
    args = parse_args()
    log.debug('args: %s', pformat(args))
    
    templatef = args.rom_template
    if args.rom_template is None:
        templatef = pjoin(dirname(__file__), 'rom.template')

    template = read(templatef)

    mcode = read_a_out(args.fname)
    data = '\n'.join(mcode)
    
    outf = args.o
    if args.o is None:
        outf = splitext(args.fname) + '.rom'

    with open(outf, 'w') as fd:
        fd.write(template.format(data=data))

if __name__ == '__main__':
    sys.exit(main())
