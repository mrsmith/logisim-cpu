# fibornacci numbers
#
# a, b = 1, 2
# a, b = b, a + b
#

imma 10
sta 2   # @2: count

imma 1  # @0: a
sta 0

imma 2  # @1: b
sta 1

# loop
lda 0
ldb 1
add
sta 1   # b = a + b
stb 0   # a = b
lda 2
immb 1
sub     # count -= 1
sta 2
jz 2    # break
jmp -10 # goto loop

# end
hlt
