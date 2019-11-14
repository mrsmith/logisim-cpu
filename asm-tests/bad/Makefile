.SUFFIXES:

ASM := $(wildcard *.asm)
STDOUT := $(patsubst %.asm,%.stdout,$(ASM))

CHECK := $(patsubst %.asm,check-%,$(ASM))

%.stdout: %.asm ../asm.py
	rm -f $@ && ../asm.py $< -o /dev/null > $@.tmp && mv $@.tmp $@

check-%: %.stdout
	diff -u $*.expected $<

.PHONY: check
check: $(CHECK)

.PHONY: clean
clean:
	rm -f $(STDOUT) $(patsubst %,%.tmp,$(STDOUT))
