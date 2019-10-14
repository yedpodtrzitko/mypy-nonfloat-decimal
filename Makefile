test:
	pytest --mypy-ini-file=./tests/mypy.ini ./tests

black:
	black mypy_nonfloat_decimal


.PHONY: test black
