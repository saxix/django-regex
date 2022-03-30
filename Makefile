BUILDDIR='~build'


.mkbuilddir:
	mkdir -p ${BUILDDIR}

develop:
	@pip install -U pip setuptools pip-tools
	@pip install -e .[dev]


test:
	py.test -v --create-db

qa:
	flake8 src/ tests/
	isort -rc src/ --check-only
	check-manifest


clean:
	rm -fr ${BUILDDIR} dist src/*.egg-info .coverage coverage.xml .eggs
	find src -name __pycache__ -o -name "*.py?" -o -name "*.orig" -prune | xargs rm -rf
	find tests -name __pycache__ -o -name "*.py?" -o -name "*.orig" -prune | xargs rm -rf

fullclean:
	rm -fr .tox .cache
	$(MAKE) clean


docs: .mkbuilddir
	mkdir -p ${BUILDDIR}/docs
	sphinx-build -aE docs/ ${BUILDDIR}/docs
ifdef BROWSE
	firefox ${BUILDDIR}/docs/index.html
endif
