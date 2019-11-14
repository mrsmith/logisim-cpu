.SUFFIXES:

ASM := $(wildcard *.asm) 
OUT := $(patsubst %.asm,%.out,$(ASM))

%.out: %.asm ./asm.py
	./asm.py $< -o $@

.PHONY: all
all: $(OUT) bad

.PHONY: bad
bad:
	$(MAKE) -C bad check

.PHONY: clean
clean:
	rm -f $(OUT)
	$(MAKE) -C bad clean
