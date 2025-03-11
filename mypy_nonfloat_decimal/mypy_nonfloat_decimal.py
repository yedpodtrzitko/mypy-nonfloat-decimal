"""Mypy plugin: non-float check for Decimal."""

from decimal import Decimal
from typing import Callable, Optional

from mypy.errorcodes import MISC, ErrorCode
from mypy.plugin import FunctionContext, Plugin
from mypy.types import AnyType, Instance, LiteralType, TupleType, Type, UnionType

VALID_DECIMAL_ARG = ErrorCode(
    "valid-decimal-arg",
    "Check valid argument provided when constructing a Decimal, e.g. non-float",
    "General",
    # Make a subcode of `misc` for backward compatibility.
    sub_code_of=MISC,
)


class InvalidType(ValueError):
    pass


def _get_type_name(type_name) -> str:
    """Mypy API of type name has changed from callable to property."""
    return type_name() if callable(type_name) else type_name


class DecimalNonFloatPlugin(Plugin):
    """Mypy plugin for checking only certain types to be passed to Decimal().

    `float` passed to Decimal() can cause imprecision, allow only string, int, Decimal.
    """

    def get_function_hook(
        self, fullname: str
    ) -> Optional[Callable[[FunctionContext], Type]]:
        """Register callback when a specific type is called, in this case Decimal.

        :param fullname: full name of the type to consider
        :return: callback for specific type call
        """
        if fullname in ("_decimal.Decimal", "decimal.Decimal"):
            return analyze_decimal_call
        return None


def analyze_decimal_call(ctx: FunctionContext) -> Type:
    """Callback for Decimal type calls.

    Consider if parameter passed to Decimal is legit.
    """
    try:
        param: Instance = ctx.arg_types[0][0]
    except IndexError:
        # no arguments passed
        pass
    else:
        try:
            consider_decimal_type(ctx, param)
        except InvalidType as e:
            ctx.api.fail(
                'Invalid type passed to Decimal (expected "Union[int, str, Decimal]"), got {} instead (offender: {})'.format(
                    param, str(e)
                ),
                ctx.context,
                code=VALID_DECIMAL_ARG,
            )

    return ctx.default_return_type


def consider_decimal_type(ctx, param) -> None:
    if isinstance(param, AnyType):
        pass  # dont do anything with `Any`
    elif isinstance(param, (UnionType, TupleType)):
        for item in param.items:
            consider_decimal_type(ctx, item)
    elif isinstance(param, (LiteralType,)):
        if not isinstance(param.value, (int, str, Decimal)):
            raise InvalidType(type(param.value))

    elif not hasattr(param, "type"):
        ctx.api.note(
            'Unexpected type passed to Decimal (expected "Union[int, str, Decimal]"), got {} instead'.format(
                param
            ),
            ctx.context,
        )
    elif _get_type_name(param.type.name) not in ("str", "int", "Decimal"):
        raise InvalidType(_get_type_name(param.type.name))
