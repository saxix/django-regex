BUILDDIR='~build'


.mkbuilddir:
	mkdir -p ${BUILDDIR}

develop:
	@pip install -U pip setuptools pip-tools
	@pip install -e .[dev]

compile-requirements:
	@pip-compile src/requirements/install.in \
		--upgrade \
		--rebuild \
		--no-header \
		--no-emit-trusted-host \
		--no-index -o src/requirements/install.pip
	@pip-compile src/requirements/testing.in \
		src/requirements/install.pip \
		--upgrade \
		--rebuild \
		--no-header \
		--no-emit-trusted-host \
		--no-index -o src/requirements/testing.pip
	@pip-compile src/requirements/develop.in \
		src/requirements/install.pip \
		src/requirements/testing.pip \
		--upgrade \
		--rebuild \
		--no-header \
		--no-emit-trusted-host \
		--no-index -o src/requirements/develop.pip

sync-requirements:
	pip-sync src/requirements/develop.pip
	pip install -e .[dev]


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
