.POSIX:

PREFIX = /usr/local

output: dwmblocks.o
	gcc dwmblocks.o -lX11 -o dwmblocks
dwmblocks.o: dwmblocks.c config.h
	gcc -c -lX11 dwmblocks.c
clean:
	rm -f *.o *.gch dwmblocks
install: output
	mkdir -p $(DESTDIR)$(PREFIX)/bin
	cp -f dwmblocks $(DESTDIR)$(PREFIX)/bin
	chmod 755 $(DESTDIR)$(PREFIX)/bin/dwmblocks
uninstall:
	rm -f $(DESTDIR)$(PREFIX)/bin/dwmblocks

.PHONY: clean install uninstall
