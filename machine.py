#!/usr/bin/env python3

import sys
from sh import logisim
from pprint import pprint, pformat
from collections import namedtuple
import argparse as ap
import logging as log
import attr

from disasm import disasm

FLAGS_Z = 1
FLAGS_OV = 1 << 1

def format_flags(flags):
    f = []
    f.append(flags & FLAGS_Z and 'z' or ' ')
    f.append(flags & FLAGS_OV and 'ov' or '  ')
    return '[{:4}]'.format(' '.join(f))

@attr.s
class State:
    pc = attr.ib(factory=int)
    insn = attr.ib(factory=int)
    flags = attr.ib(factory=int)
    a = attr.ib(factory=int)
    b = attr.ib(factory=int)

    def __str__(self):
        return 'pc: 0x{0.pc:04x} i: 0x{0.insn:04x} I: {1:10} f: {2} a: 0x{0.a:02x} b: 0x{0.b:02x}'.format(
                self, disasm(self.insn), format_flags(self.flags))


def parse_pins(line):
    def parse_reg(s):
        bin = s.strip().replace(' ', '')
        return int(bin, 2)

    line = line.strip()
    toks = line.split('\t')

    flags, pc, ra, insn, rb = map(parse_reg, toks)
    return State(pc, insn, flags, ra, rb)

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
        state = parse_pins(line)
        print(state)

if __name__ == '__main__':
    sys.exit(main())
