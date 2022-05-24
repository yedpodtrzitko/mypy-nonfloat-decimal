test:
	pytest --mypy-ini-file=./tests/mypy.ini ./tests

black:
	black ./mypy_nonfloat_decimal ./tests

project:
	mypy --config-file=./tests/mypy.ini ./tests/manual_run.py


.PHONY: test black
