# simple makefile to simplify repetitive build env management tasks under posix

PYTHON := $(shell which python)
RUNTESTS := $(shell which pytest)

all: clean install

clean-test:
	@rm -fr .pytest_cache

clean-pyc:
	@find . -name "*.pyc" -exec rm {} \;

clean: clean-test clean-pyc

install:
	@python setup.py install

# tests
pep8:
	@pep8 --exclude=.git alphatwirl_interface

flake8:
	@flake8 $(shell file -p bin/* |awk -F: '/python.*text/{print $$1}') alphatwirl_interface --ignore=F401 --max-line-length=120
	# using imported fixtures causes problems with flake8
	@flake8 $(shell file -p bin/* |awk -F: '/python.*text/{print $$1}') test --ignore=F401,F811 --max-line-length=120

test: test-code flake8

test-all: test-code-full flake8

test-code:
	@$(RUNTESTS)  test


changelog:
	@github_changelog_generator -u alphatwirl -p alphatwirl-interface
