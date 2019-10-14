from .mypy_nonfloat_decimal import DecimalNonFloatPlugin


def plugin(version):
    """Plugin entry point Mypy is looking for."""
    return DecimalNonFloatPlugin
