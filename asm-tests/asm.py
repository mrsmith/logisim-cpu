#!/usr/bin/env python3

import sys
import argparse as ap
import logging as log
from pprint import pprint, pformat

def parse_args():
    p = ap.ArgumentParser()
    p.add_argument('fname', type=str, help='assembler input')
    p.add_argument('-o', type=str, default='a.out', help='binary output')

    return p.parse_args()

class AOut():
    def __init__(self, fd):
        self.fd = fd
        self.writeln('v2.0 raw')

    def writeln(self, data):
        self.fd.write(data + '\n')

INSNS = dict()

def insn(foo):
    INSNS[foo.__name__] = foo
    return foo

CTL_JMP = 1

def encode(imm, ctl):
    return '{:02x}{:02x}'.format(imm, ctl)

def dbl_comp_8(x):
    return x if x > 0 else 0x100 + x

class AsmError(Exception): pass

@insn
def jmp(ln, line, out):
    try:
        _, offt = line.split(' ', 1)
        offt = int(offt)

    except ValueError:
        raise AsmError('bad jmp instruction `{}`'.format(line))

    if offt < -128 or offt > 127:
        raise AsmError('bad jmp offset `{}`'.format(offt))

    offt = dbl_comp_8(offt)
    out.writeln(encode(imm=offt, ctl=CTL_JMP))

@insn
def hlt(ln, line, out):
    out.writeln(encode(imm=0, ctl=CTL_JMP))

@insn
def nop(ln, line, out):
    out.writeln(encode(imm=0, ctl=0))

def main():
    args = parse_args()
    log.debug('args: %s', pformat(args))

    with open(args.fname) as infd:
        with open(args.o, 'w') as outfd:
            out = AOut(outfd)

            for ln, line in enumerate(infd, start=1):
                line = line.split('#', 1)[0]
                line = line.strip()

                if not line:
                    continue

                insn = line.split(' ', 1)[0]
                try:
                    INSNS[insn](ln, line, out)

                except KeyError:
                    print('{}:{}: warn: bad instruction `{}`'.format(args.fname, ln, line))
                    continue

                except AsmError as ex:
                    print('{}:{}: warn: {}'.format(args.fname, ln, ex))
                    continue

if __name__ == '__main__':
    sys.exit(main())
