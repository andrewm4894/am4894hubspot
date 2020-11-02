SRC = $(wildcard ./*.ipynb)

all: am4894hubspot docs

build: $(SRC)
	nbdev_build_docs
	nbdev_test_nbs
	nbdev_build_lib

am4894hubspot: $(SRC)
	nbdev_build_lib
	touch am4894hubspot

docs_serve: docs
	cd docs && bundle exec jekyll serve

docs: $(SRC)
	nbdev_build_docs
	touch docs

test:
	nbdev_test_nbs

release: pypi
	nbdev_bump_version

pypi: dist
	twine upload --repository pypi dist/*

dist: clean
	python setup.py sdist bdist_wheel

clean:
	rm -rf dist