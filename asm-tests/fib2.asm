# fibornacci numbers
#
# a, b = 1, 2
# a, b = b, a + b
#

# cycle counter, do for 3 iterations

imma 10
sta 2   # @2: count

imma 1  # @0: a
sta 0

imma 2  # @1: b
sta 1

# loop
lda 0
nop
ldb 1
nop
add
sta 1   # b = a + b
stb 0   # a = b
nop
nop
nop
nop
nop
lda 2
immb 1
sub     # count -= 1
sta 2
jz 2    # break
jmp -17 # goto loop

# end
hlt
