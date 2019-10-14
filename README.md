# Mypy non-float Decimal plugin

Restricts passing float numbers to Decimal

## Why?

[The implementation of floating point numbers](https://docs.python.org/3/tutorial/floatingpoint.html) 
can cause imprecisions in results. To avoid this problem you can use `Decimal` type, 
however you still need to avoid passing `float` as its parameter:

```
>>> Decimal(1.02)
Decimal("1.020000000000000017763568394002504646778106689453125")
>>> Decimal("1.02")
Decimal("1.02")
```

This plugin is meant to spot occurrences where `float` is passed to `Decimal` in your code.

## Usage

- install plugin

```
pip install mypy-nonfloat-decimal
```

- add it into list of mypy plugins in your mypy config (`mypy.ini`)

```
[mypy]
plugins=mypy_nonfloat_decimal
```

- upon running mypy will detect `float` passed to `Decimal` and report it as an error (`example.py`):


```
from decimal import Decimal
Decimal(1.02)
```

```
$ mypy --config-file ./mypy.ini ./example.py

example.py:2: error: Invalid type passed to Decimal (expected "Union[int, str, Decimal]"), got float instead
```
