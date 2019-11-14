#!/usr/bin/env python3

import sys
from sh import logisim
from pprint import pprint, pformat
from collections import namedtuple
import argparse as ap
import logging as log

Regs = namedtuple('Regs', 'pc')

def parse_pins(line):
    bin = line.strip().replace(' ', '')
    pc = int(bin, 2)
    return Regs(pc)

def parse_args():
    p = ap.ArgumentParser()
    p.add_argument('--cpu-circut', type=str, default='cpu.circ', help='main CPU circut file')
    p.add_argument('--rom', type=str, default='rom.circ', help='ROM circut file')

    return p.parse_args()

def main():
    args = parse_args()
    log.debug('args: %s', pformat(args))

    out = logisim('-tty', 'table', args.cpu_circut, '-sub', 'rom.circ', args.rom)

    for line in out:
        regs = parse_pins(line)
        pprint(regs)

if __name__ == '__main__':
    sys.exit(main())
