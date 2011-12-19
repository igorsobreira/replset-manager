ARGS=

test:
	@rm -rf tests/test-output.log
	PYTHONPATH=. py.test -vs tests/ ${ARGS}