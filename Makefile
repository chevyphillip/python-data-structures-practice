# Makefile for building markdown site from notebooks
.PHONY: convert clean

convert:
	mkdir -p site/notebooks
	jupyter nbconvert --to markdown --output-dir="site/notebooks" *.ipynb notebooks/*.ipynb
	mkdir -p site/solutions
	cp -r solutions/*.md site/solutions || true

clean:
	rm -rf site