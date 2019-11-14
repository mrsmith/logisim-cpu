.SUFFIXES:

ASM := $(wildcard *.asm) 
OUT := $(patsubst %.asm,%.out,$(ASM))
ROM := $(patsubst %.out,%.rom,$(OUT))

%.out: %.asm ./asm.py
	./asm.py $< -o $@

%.rom: %.out ../mkrom.py
	../mkrom.py $< -o $@

.PHONY: all
all: $(OUT) $(ROM) bad

.PHONY: bad
bad:
	$(MAKE) -C bad check

.PHONY: clean
clean:
	rm -f $(OUT) $(ROM)
	$(MAKE) -C bad clean
