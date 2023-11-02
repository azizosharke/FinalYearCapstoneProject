ROOTNAME = main
PDFFILE = $(ROOTNAME).pdf
TEXFILE = $(ROOTNAME).tex
LATEX = pdflatex

all: base 

base:
	$(LATEX) $(ROOTNAME)
	bibtex $(ROOTNAME)
	$(LATEX) $(ROOTNAME)
	$(LATEX) $(ROOTNAME)

clean:
	rm -f *.dvi *.ps *.aux *.bbl *.blg *.log *.out *.toc *.lot *.lof
