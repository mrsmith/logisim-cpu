#!/usr/bin/env python3

import sys
from sh import logisim
from pprint import pprint, pformat
from collections import namedtuple
import argparse as ap
import logging as log

State = namedtuple('State', 'pc, a, insn, b')

def parse_pins(line):
    def parse_reg(s):
        bin = s.strip().replace(' ', '')
        return int(bin, 2)

    line = line.strip()
    toks = line.split('\t')

    pc, ra, insn, rb = map(parse_reg, toks)
    return State(pc, ra, insn, rb)

def parse_args():
    p = ap.ArgumentParser()
    p.add_argument('--cpu-circut', type=str, default='cpu.circ', help='main CPU circut file')
    p.add_argument('--rom', type=str, default='rom.circ', help='ROM circut file')

    p.add_argument('-d', action='count', default=0, help='debug, -dd more debug')

    return p.parse_args()

def configure_logging(args):
    level = log.INFO if args.d < 2 else log.DEBUG
    log.basicConfig(stream=sys.stderr, level=level)

    if args.d < 3:
        sh_logger = log.getLogger('sh')
        sh_logger.setLevel(log.WARN)

def main():
    args = parse_args()
    configure_logging(args)

    log.debug('args: %s', pformat(args))

    out = logisim('-tty', 'table', args.cpu_circut, '-sub', 'rom.circ', args.rom)

    for line in out:
        log.debug(pformat(line))
        regs = parse_pins(line)
        pprint(regs)

if __name__ == '__main__':
    sys.exit(main())
