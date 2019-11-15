.SUFFIXES:
.PHONY: all clean

all:
	$(MAKE) -C asm-tests all

clean:
	$(MAKE) -C asm-tests clean
