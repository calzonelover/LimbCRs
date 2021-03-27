PACKAGE = cttex.c Makefile dictsort.c dict2c.pl tdict.txt README

all: cttex dictsort

cttex: cttex.c tdict.h
	gcc -O -o cttex cttex.c

dictsort: dictsort.c
	gcc -O -o dictsort dictsort.c

#tdict.h: tdict.txt
#	dict2c.pl tdict.txt > tdict.h

pack: $(PACKAGE)
	tar zcvfh cttex.tar.gz $(PACKAGE)

clean: 
	rm -f cttex dictsort *~ junk
#	rm -f tdict.h

