"""Storage containers for PI data."""
import datetime

from pandas import Series
import pytz
import wrapt


class PISeries(Series):
    """Extension to pandas.Series with PI metadata."""
    version = '0.1.0'

    def __init__(self, tag, timestamp, value, uom=None, *args, **kwargs):
        Series.__init__(self,
                        data=value,
                        index=timestamp,
                        name=tag,
                        *args, **kwargs)
        self.tag = tag
        self.uom = uom

    @staticmethod
    def timestamp_to_index(timestamp):
        """Convert AFTime object to datetime.datetime in local timezone.

           TODO: Allow to define timezone, default to UTC?
        """
        local_tz = pytz.timezone('Europe/Amsterdam')
        return datetime.datetime(
            timestamp.Year,
            timestamp.Month,
            timestamp.Day,
            timestamp.Hour,
            timestamp.Minute,
            timestamp.Second,
            timestamp.Millisecond * 1000
        ).replace(tzinfo=pytz.utc).astimezone(local_tz)


def operate(base, operator, operand):
    """Apply a decorator to a function to apply an operator to the function and a given operand.

       Operand can be either a constant or a function which accepts the same arguments
       as the base function to which the decorator is applied. Operator must be a
       function of two arguments.
    """
    @wrapt.decorator
    def operate_(func, instance, args, kwargs):
        """Decorate function to apply an operator to the function and a give operand"""
        if hasattr(operand, base.__name__):
            # If operand has a function with the same name as the base function it is
            # assumed to have the same signature.
            func2 = getattr(operand, base.__name__)
            return operator(func(*args, **kwargs), func2(*args, **kwargs))
        else:
            # If operand does not have a function with the same name as the base
            # function it is assumed to be a constant.
            return operator(func(*args, **kwargs), operand)
    return operate_(base)


def add_numops(numops, members, newclassname, attributes):
    """Return a class decorator to add operators which patch each of a list of members.

    Keyword arguments:
    numops -- a list of tuples containing the function name to be added to the class,
              a definition of the operator (as a function of two arguments), and a
              docstring for the new function.
    members -- a list of strings with the names of the class members that must be
               decorated.
    newclassname -- the name of the new class that will be returned by the patched
                    versions of *members*.
    attributes -- a list of attributes that are extracted from the original object and
                  passed as arguments to <newclassname>.__init__.
    """

    def add_numop(op_name, op, op_doc, cls):
        """Return a method definition for a numerical operator.

        Keyword arguments:
        op_name -- name of the operator method of a subclass of *cls*, will used for
                   <operator>.__name__ for clean output in the class documentation.
        op -- function of two arguments that is applied to the original function result
              and a given operand.
        op_doc -- docstring for the new operator method.
        cls -- class of which the new dynamic class will be subclassed.
        """

        def operator_(self, other):
            """Return new object of with patched members.

               Creates a new virtual class with the members in *members* patched to apply
               the given operator *op* to the original function definition.
            """
            newclass = type(newclassname,
                            (cls,),
                            {member: operate(base=getattr(self, member),
                                             operator=op,
                                             operand=other) for member in members})
            new = newclass(*[getattr(self, attr) for attr in attributes])
            return new
        operator_.__name__ = op_name
        operator_.__doc__ = op_doc
        return operator_

    def add_numops_(cls):
        """Decorate a class to add a function for each operator in a list of operators."""
        for op_name, op, op_doc in numops:
            setattr(cls, op_name, add_numop(op_name, op, op_doc, cls))
        return cls
    return add_numops_


operators = [
    ('__add__', lambda x, y: x + y, 'Add value(s) to PIPoint'),
    ('__radd__', lambda x, y: y + x, 'Add PIPoint to value(s) (reverse order)'),
    ('__sub__', lambda x, y: x - y, 'Subtract value(s) from PIPoint'),
    ('__rsub__', lambda x, y: y - x, 'Subtract PIPoint from value(s) (reverse order)'),
    ('__mul__', lambda x, y: x * y, 'Multiply PIPoint by value(s)'),
    ('__rmul__', lambda x, y: y * x, 'Multiply value(s) by PIPoint (reverse order)'),
    # # '__matmul__': lambda x, y: x @ y,  # Removed for now, Python 3 only
    # # '__rmatmul__': lambda x, y: y @ x,  # Removed for now, Python 3 only
    ('__div__', lambda x, y: x / y, 'Divide PIPoint by value(s)'),
    ('__rdiv__', lambda x, y: y / x, 'Divide value(s) by PIPoint (reverse order)'),
    ('__truediv__', lambda x, y: x / y, 'Divide PIPoint by value(s)'),
    ('__rtruediv__', lambda x, y: y / x, 'Divide value(s) by PIPoint (reverse order)'),
    ('__floordiv__', lambda x, y: x // y, 'Floordivide PIPoint by value(s)'),
    ('__rfloordiv__', lambda x, y: y // x, 'Floordivide value(s) by PIPoint (reverse order)')
]
