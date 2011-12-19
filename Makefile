ARGS=

test:
	@rm -rf tests/test-output.log
	@echo "\033[32mCheck tests/test-output.log for the spawned commands stdout/stderr\033[0m"
	PYTHONPATH=. py.test -vs tests/ ${ARGS}