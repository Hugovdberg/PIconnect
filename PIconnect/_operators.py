"""helpers to define numeric operators in batch on classes"""
from collections import namedtuple

import wrapt


def operate(operator, operand):
    """Create a decorator to apply an operator to the function and a given operand.

    Operand can be either a constant or a function which accepts the same arguments
    as the base function to which the decorator is applied. Operator must be a
    function of two arguments.
    """

    @wrapt.decorator
    def operate_(func, instance, args, kwargs):  # pylint: disable=unused-argument
        """Decorate function to apply an operator to the function and a given operand."""
        if hasattr(operand, func.__name__):
            func2 = getattr(operand, func.__name__)
            return operator(func(*args, **kwargs), func2(*args, **kwargs))
        return operator(func(*args, **kwargs), operand)

    return operate_


def decorate(decorator, base, *args, **kwargs):
    """Return function decorated with the operate decorator.

    Inline replacement for @*decorator(*args, **kwargs)*
    """
    return decorator(*args, **kwargs)(base)


def add_operators(operators, members, newclassname, attributes):
    """Return a class decorator to add operators which patch each of a list of members.

    Keyword arguments:
    operators -- a list of tuples containing the function name to be added to the class,
              a definition of the operator (as a function of two arguments), and a
              docstring for the new function.
    members -- a list of strings with the names of the class members that must be
               decorated.
    newclassname -- the name of the new class that will be returned by the patched
                    versions of *members*.
    attributes -- a list of attributes that are extracted from the original object and
                  passed as arguments to <newclassname>.__init__.
    """

    def build_operator_method(method, operator, docstring, cls):
        """Return a method definition for a numerical operator.

        Keyword arguments:
        method -- name of the operator method of a subclass of *cls*, will used for
                  <operator>.__name__ for clean output in the class documentation.
        operator -- function of two arguments that is applied to the original function
                    result and a given operand.
        docstring -- docstring for the new operator method.
        cls -- class of which the new dynamic class will be subclassed.
        """

        def patch_members(self, other):
            """Return new object of class *newclassname* with patched members.

            Creates a new virtual class with the members in *members* patched to apply
            the given *operator* to the original function definition.
            """
            newmembers = {
                member: decorate(
                    decorator=operate,
                    base=getattr(self, member),
                    operator=operator,
                    operand=other,
                )
                for member in members
            }
            newclass = type(str(newclassname), (cls,), newmembers)
            return newclass(*[getattr(self, attr) for attr in attributes])

        patch_members.__name__ = str(method)
        patch_members.__doc__ = docstring
        return patch_members

    def add_numops_(cls):
        """Decorate a class to add a function for each operator in a list of operators."""
        for operator in operators:
            setattr(
                cls,
                operator.method,
                build_operator_method(
                    method=operator.method,
                    operator=operator.operator,
                    docstring=operator.docstring,
                    cls=cls,
                ),
            )
        return cls

    return add_numops_


Operator = namedtuple("Operator", ["method", "operator", "docstring"])
OPERATORS = [
    Operator("__add__", lambda x, y: x + y, """Add value(s) to PIPoint"""),
    Operator(
        "__radd__", lambda x, y: y + x, """Add PIPoint to value(s) (reverse order)"""
    ),
    Operator("__sub__", lambda x, y: x - y, """Subtract value(s) from PIPoint"""),
    Operator(
        "__rsub__",
        lambda x, y: y - x,
        """Subtract PIPoint from value(s) (reverse order)""",
    ),
    Operator("__mul__", lambda x, y: x * y, """Multiply PIPoint by value(s)"""),
    Operator(
        "__rmul__",
        lambda x, y: y * x,
        """Multiply value(s) by PIPoint (reverse order)""",
    ),
    Operator("__matmul__", lambda x, y: x @ y, """Matrix multiply"""),
    Operator("__rmatmul__", lambda x, y: y @ x, """Matrix multiply (reverse order)"""),
    Operator("__div__", lambda x, y: x / y, """Divide PIPoint by value(s)"""),
    Operator(
        "__rdiv__", lambda x, y: y / x, """Divide value(s) by PIPoint (reverse order)"""
    ),
    Operator("__truediv__", lambda x, y: x / y, """Divide PIPoint by value(s)"""),
    Operator(
        "__rtruediv__",
        lambda x, y: y / x,
        """Divide value(s) by PIPoint (reverse order)""",
    ),
    Operator(
        "__floordiv__", lambda x, y: x // y, """Floordivide PIPoint by value(s)"""
    ),
    Operator(
        "__rfloordiv__",
        lambda x, y: y // x,
        """Floordivide value(s) by PIPoint (reverse order)""",
    ),
    Operator("__mod__", lambda x, y: x % y, """Modulo PIPoint by value(s)"""),
    Operator(
        "__rmod__", lambda x, y: y % x, """Modulo value(s) by PIPoint (reverse order)"""
    ),
    Operator(
        "__divmod__",
        divmod,  # This is already a function of x and y
        """Return divmod of PIPoint by value(s).

             divmod(a, b) returns a tuple of the floordivision of a and b, a // b, and the
             modulo of a and b, a % b. For integers this is faster than when the operations
             are performed separately.
             """,
    ),
    Operator(
        "__rdivmod__",
        lambda x, y: divmod(y, x),
        """Return divmod of value(s) by PIPoint (reverse order).

             divmod(a, b) returns a tuple of the floordivision of a and b, a // b, and the
             modulo of a and b, a % b. For integers this is faster than when the operations
             are performed separately.
             """,
    ),
]
