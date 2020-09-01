
all:
	cython mcpil.pyx --embed
	gcc -pthread -g -fwrapv -fPIC -Wall -g -fstack-protector-strong -Wformat -Werror=format-security -Wdate-time -I/usr/include/python3.7m mcpil.c -o mcpil.elf
	chmod a+x mcpil.elf
