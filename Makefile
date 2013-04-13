.PHONY: clean-pyc clean-build docs

test:
	@nosetests -s

coverage:
	@rm -f .coverage
	@nosetests --with-cov terminal tests/

clean: clean-build clean-pyc


clean-build:
	@rm -fr deploy/
	@rm -fr build/
	@rm -fr dist/
	@rm -fr test/build/
	@rm -fr *.egg-info


clean-pyc:
	@find . -name '*.pyc' -exec rm -f {} +
	@find . -name '*.pyo' -exec rm -f {} +
	@find . -name '*~' -exec rm -f {} +
	@find . -name '__pycache__' -exec rm -fr {} +

docs:
	@git submodule init
	@git submodule update
	@$(MAKE) -C docs html
