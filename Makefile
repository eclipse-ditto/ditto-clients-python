DESTDIR?=/

.PHONY : all clean clean-build clean-py install test upload

all:
	python ./setup.py build

install: all
	python ./setup.py install --root=${DESTDIR}

build-whl:
	 python3 -m build

clean: clean-build clean-py

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-py: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

test: install
	python setup.py test

upload: test
	python ./setup.py sdist upload
