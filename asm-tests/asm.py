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

CTL_JMP = 1 << 0
CTL_MWR = 1 << 1
CTL_WRA = 1 << 2
CTL_WRB = 1 << 3
CTL_LDMEM_LDIMM = 1 << 4
CTL_STA_STB = 1 << 5
CTL_LDALU = 1 << 6
CTL_JZ = 1 << 7

ALU_OP_ADD = 0
ALU_OP_SUB = 1

def encode(imm, ctl):
    return '{:02x}{:02x}'.format(imm, ctl)

def dbl_comp_8(x):
    return x if x >= 0 else 0x100 + x

def test_dbl_comp_8():
    assert dbl_comp_8(0) == 0
    assert dbl_comp_8(1) == 1
    assert dbl_comp_8(128) == 128
    assert dbl_comp_8(255) == 255
    assert dbl_comp_8(-1) == 255
    assert dbl_comp_8(-2) == 254

class AsmError(Exception): pass

def j(kind, line, out):
    assert kind in {'mp', 'z'}
    insn = 'j' + kind

    try:
        _, offt = line.split(' ', 1)
        offt = int(offt)

    except ValueError:
        raise AsmError('bad {} instruction `{}`'.format(insn, line))

    if offt < -128 or offt > 127:
        raise AsmError('bad {} offset `{}`'.format(insn, offt))

    offt = dbl_comp_8(offt)
    ctl = dict(mp=0, z=CTL_JZ)
    out.writeln(encode(imm=offt, ctl=ctl[kind]))

@insn
def jmp(line, out):
    return j('mp', line, out)

@insn
def jz(line, out):
    return j('z', line, out)

@insn
def hlt(line, out):
    out.writeln(encode(imm=0, ctl=CTL_JMP))

@insn
def nop(line, out):
    out.writeln(encode(imm=0, ctl=0))

def ldr(r, line, out):
    ''' template for lda, ldb instructions '''
    assert r in {'a', 'b'}
    insn = 'ld' + r

    try:
        _, addr = line.split(' ', 1)
        addr = int(addr)

    except ValueError:
        raise AsmError('bad {} instruction `{}`'.format(insn, line))

    if addr < 0 or addr > 0xff:
        raise AsmError('bad {} addr `{}`'.format(insn, addr))

    ctl = dict(a=CTL_WRA, b=CTL_WRB)
    out.writeln(encode(imm=addr, ctl=ctl[r]))

@insn
def lda(line, out):
    return ldr('a', line, out)

@insn
def ldb(line, out):
    return ldr('b', line, out)

def immr(r, line, out):
    ''' template for imma, immb instructions '''
    assert r in {'a', 'b'}
    insn = 'imm' + r

    try:
        _, imm = line.split(' ', 1)
        imm = int(imm)

    except ValueError:
        raise AsmError('bad {} instruction `{}`'.format(insn, line))

    if imm < -128 or imm > 255:
        raise AsmError('bad {} imm `{}`'.format(insn, imm))

    imm = dbl_comp_8(imm)

    ctl = dict(a=CTL_WRA, b=CTL_WRB)
    out.writeln(encode(imm=imm, ctl=CTL_LDMEM_LDIMM | ctl[r]))

@insn
def imma(line, out):
    return immr('a', line, out)

@insn
def immb(line, out):
    return immr('b', line, out)

def _str(r, line, out):
    ''' template for sta, stb instructions '''
    assert r in {'a', 'b'}
    insn = 'st' + r

    try:
        _, addr = line.split(' ', 1)
        addr = int(addr)

    except ValueError:
        raise AsmError('bad {} instruction `{}`'.format(insn, line))

    if addr < 0 or addr > 0xff:
        raise AsmError('bad {} addr `{}`'.format(insn, addr))

    ctl = dict(a=0, b=CTL_STA_STB)
    out.writeln(encode(imm=addr, ctl=CTL_MWR | ctl[r]))

@insn
def sta(line, out):
    return _str('a', line, out)

@insn
def stb(line, out):
    return _str('b', line, out)

@insn
def add(line, out):
    out.writeln(encode(imm=ALU_OP_ADD, ctl=CTL_WRA | CTL_LDALU))

@insn
def sub(line, out):
    out.writeln(encode(imm=ALU_OP_SUB, ctl=CTL_WRA | CTL_LDALU))


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
                    INSNS[insn](line, out)

                except KeyError:
                    print('{}:{}: warn: bad instruction `{}`'.format(args.fname, ln, line))
                    continue

                except AsmError as ex:
                    print('{}:{}: warn: {}'.format(args.fname, ln, ex))
                    continue

if __name__ == '__main__':
    sys.exit(main())
