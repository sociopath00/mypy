"""Primitive tuple ops for *variable-length* tuples.

Note: Varying-length tuples are represented as boxed Python tuple
objects, i.e. tuple_rprimitive (RPrimitive), not RTuple.
"""

from mypyc.ir.ops import ERR_MAGIC
from mypyc.ir.rtypes import tuple_rprimitive, int_rprimitive, list_rprimitive, object_rprimitive
from mypyc.primitives.registry import (
    c_method_op, custom_op, simple_emit, c_function_op
)


# tuple[index] (for an int index)
tuple_get_item_op = c_method_op(
    name='__getitem__',
    arg_types=[tuple_rprimitive, int_rprimitive],
    return_type=object_rprimitive,
    c_function_name='CPySequenceTuple_GetItem',
    error_kind=ERR_MAGIC)

# Construct a boxed tuple from items: (item1, item2, ...)
new_tuple_op = custom_op(
    arg_types=[object_rprimitive],
    result_type=tuple_rprimitive,
    is_var_arg=True,
    error_kind=ERR_MAGIC,
    steals=False,
    format_str='{dest} = ({comma_args}) :: tuple',
    emit=simple_emit('{dest} = PyTuple_Pack({num_args}{comma_if_args}{comma_args});'))

# Construct tuple from a list.
list_tuple_op = c_function_op(
    name='builtins.tuple',
    arg_types=[list_rprimitive],
    return_type=tuple_rprimitive,
    c_function_name='PyList_AsTuple',
    error_kind=ERR_MAGIC,
    priority=2)

# Construct tuple from an arbitrary (iterable) object.
c_function_op(
    name='builtins.tuple',
    arg_types=[object_rprimitive],
    return_type=tuple_rprimitive,
    c_function_name='PySequence_Tuple',
    error_kind=ERR_MAGIC)
