CTL_JMP = 1 << 0
CTL_MWR = 1 << 1
CTL_WRA = 1 << 2
CTL_WRB = 1 << 3
CTL_LDMEM_LDIMM = 1 << 4
CTL_STA_STB = 1 << 5
CTL_LDALU = 1 << 6

def dbl_comp_to_int(x):
    return x if x < 128 else x - 256

def test_dbl_comp_to_int():
    assert dbl_comp_to_int(0) == 0
    assert dbl_comp_to_int(1) == 1
    assert dbl_comp_to_int(127) == 127
    assert dbl_comp_to_int(255) == -1
    assert dbl_comp_to_int(254) == -2

def disasm(code):
    ctl, imm = code & 0xff, (code >> 8) & 0xff

    if code == 0x0001:
        return 'hlt'
    elif code == 0x0000:
        return 'nop'
    elif ctl == CTL_JMP:
        return 'jmp 0x{:02x}'.format(dbl_comp_to_int(imm))
    elif ctl == CTL_WRA:
        return 'lda 0x{:02x}'.format(imm)
    elif ctl == CTL_WRB:
        return 'ldb 0x{:02x}'.format(imm)
    elif ctl == CTL_WRA | CTL_LDMEM_LDIMM:
        return 'imma 0x{:02x}'.format(imm)
    elif ctl == CTL_WRB | CTL_LDMEM_LDIMM:
        return 'immb 0x{:02x}'.format(imm)
    elif ctl == CTL_MWR:
        return 'sta 0x{:02x}'.format(imm)
    elif ctl == CTL_MWR | CTL_STA_STB:
        return 'stb 0x{:02x}'.format(imm)
    elif ctl == CTL_WRA | CTL_LDALU:
        return 'add'
    else:
        return '0x{:02x}.{:02x}'.format(imm, ctl)
