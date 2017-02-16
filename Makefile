CC=gcc
CFLAGS = -ansi -Wall -g

all: post addauthor view

post: post.cc libstream.a
	mkdir messages
	$(CC) $(CFLAGS) converter.c -o converter
	./converter post.cc
	rm converter
	$(CC) $(CFLAGS) post.c -o post.o -c
	$(CC) $(CFLAGS) post.c -o post -L. -lstream
	rm post.c
	rm *.o

addauthor: addauthor.c libstream.a
	$(CC) $(CFLAGS) addauthor.c -o addauthor.o -c
	$(CC) $(CFLAGS) addauthor.c -o addauthor -L. -lstream
	rm *.o

libstream.a: stream.c stream.h
	$(CC) -c stream.c -o stream.o
	ar cr libstream.a stream.o
	rm *.o

view: view.py
	chmod +x view.py
