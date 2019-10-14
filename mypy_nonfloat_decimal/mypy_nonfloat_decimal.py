"""Mypy plugin: non-float check for Decimal."""

from typing import Callable, Optional

from mypy.plugin import FunctionContext, Plugin
from mypy.types import AnyType, Instance, Type


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
        if fullname == "decimal.Decimal":
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
        if isinstance(param, AnyType):
            # dont do anything with `Any`
            pass
        elif not hasattr(param, "type"):
            ctx.api.note(
                'Unexpected type passed to Decimal (expected "Union[int, str, Decimal]"), got {} instead'.format(
                    param
                ),
                ctx.context,
            )
        elif param.type.name() not in ("str", "int", "Decimal"):
            ctx.api.fail(
                'Invalid type passed to Decimal (expected "Union[int, str, Decimal]"), got {} instead'.format(
                    param.type.name()
                ),
                ctx.context,
            )
    return ctx.default_return_type
