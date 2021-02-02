import re
import ctypes


__all__ = ['int_from_bits', 'str_to_var_name', 'format_pattern',
           'order_flag_options', 'order_flag_field', 'order_flag_c_field',
           'dynamicmethod']


VARIABLE_NAME_SUB_PATTERN = re.compile('\W')


def int_from_bits(*bit_pos):
    """Combine the given bit positions as an integer where the given bit positions are set to 1.

    Bit positions start at 0.

    Args:
         *bit_pos (tuple/int): Tuple of integer bit positions where the bit positions start at 0.

    Returns:
        bits (int): Integer with the bits set.
    """
    bits = 0
    for bit in bit_pos:
        bits |= (1 << bit)
    return bits


def str_to_var_name(name):
    """Convert a string to a proper variable name.

    Example:

        'Abc Def 456 *%$#' -> 'abc_def_456'
        ' Abc *%$# 456 Def' -> '_abc_456_def'

    Args:
        name (str): Name to convert to a variable name

    Returns:
        var_name (str): Snake case variable name (lower case names separated by _).
    """
    # Convert to lower case and replace spaces with underscores
    var_name = name.lower().replace(' ', '_')

    # Remove invalid characters
    var_name = VARIABLE_NAME_SUB_PATTERN.sub('', var_name)

    # Remove ending underscores
    var_name = var_name.rstrip('_')

    # Remove multiple underscores/spaces from invalid characters
    var_name = var_name.replace('__', '_')

    return var_name


def format_pattern(bit, pattern):
    """Return a string that is formatted with the given bit using either % or .format on the given pattern."""
    try:
        if "%" in pattern:
            return pattern % bit
    except:
        pass
    try:
        return pattern.format(bit)
    except:
        return pattern


def order_flag_options(key, value):
    """Return the options key value pairs in the correct order (bit (int), name (str)).

    Args:
        key (int/str): Bit int or name.
        value (str/int): Name or bit int.

    Returns:
        option (tuple): (bit (int), name (str))
    """
    if isinstance(key, int):
        bit = key
        name = str(value)
    else:
        bit = int(value)
        name = str(key)
    return bit, name


def order_flag_field(key, value):
    """Return the fields key value pairs in the correct order (name (str), bit (int)).

    Args:
        key (int/str): Bit int or name.
        value (str/int): Name or bit int.

    Returns:
        field (tuple): (name (str), bit (int))
    """
    bit, name = order_flag_options(key, value)
    var_name = str_to_var_name(name)
    return var_name, bit


def order_flag_c_field(bit_pos, options=None):
    """Return the little endian field.

    Note:
        By default the variable name is the found option name in snake case ('Hello World' becomes 'hello_world')
        or 'bit_0', 'bit_1', 'bit_2' ...

    Args:
        bit_pos (int): Index of the bit field. This starts at 0.
        options (dict)[None]: Dictionary of bit flags (bit, name) value pairs.

    Returns:
        field (tuple): (Variable name, ctypes.c_uint8, 1) This needs to be in order
    """
    if options is None:
        var_name = 'bit_' + str(bit_pos)
    else:
        name = options.get(bit_pos, '')
        var_name = str_to_var_name(name) or 'bit_' + str(bit_pos)
    return var_name, ctypes.c_uint8, 1


class dynamicmethod(object):
    """Decorator to create a class method that will also be an instance method.

    I wrote a python library named dynamicmethod, but I don't want any dependencies just for this small class.
    """
    def __init__(self, func):
        self.__func__ = func

    def __get__(self, inst, cls):
        if inst is not None:
            # Instance method
            bound_method = self.__func__.__get__(inst, cls)
            return bound_method
        else:
            # Class method
            return self.__func__.__get__(cls, cls)
