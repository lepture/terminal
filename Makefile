.PHONY: clean-pyc clean-build docs

test:
	@nosetests -s

coverage:
	@rm -f .coverage
	@nosetests --with-cov terminal tests/

clean: clean-build clean-pyc clean-docs


clean-build:
	@rm -fr build/
	@rm -fr dist/
	@rm -fr *.egg-info


clean-pyc:
	@find . -name '*.pyc' -exec rm -f {} +
	@find . -name '*.pyo' -exec rm -f {} +
	@find . -name '*~' -exec rm -f {} +
	@find . -name '__pycache__' -exec rm -fr {} +

clean-docs:
	@rm -fr  docs/_build

docs:
	@git submodule init
	@git submodule update
	@$(MAKE) -C docs html
