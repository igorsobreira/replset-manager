ARGS=
test:
	PYTHONPATH=. py.test -vs tests/ ${ARGS}