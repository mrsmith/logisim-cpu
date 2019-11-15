# fibornacci numbers
#
# a, b = 1, 2
# a, b = b, a + b
#

# init
imma 1
immb 2

# iter 0
add

# a := a + b, b := b
# swap a and b
sta 0
stb 1
lda 1
ldb 0

# unfortunately iteration will not halt
# so unrolling for now

# iter 1
add

# a := a + b, b := b
# swap a and b
sta 0
stb 1
lda 1
ldb 0

# iter 2
add

# a := a + b, b := b
# swap a and b
sta 0
stb 1
lda 1
ldb 0

# iter 3
add

# a := a + b, b := b
# swap a and b
sta 0
stb 1
lda 1
ldb 0

hlt
