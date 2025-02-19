import collections
import ctypes
from itertools import chain
from .utils import to_lower_var_name, to_snake_case, toCamelCase, to_keep_case, format_pattern, order_flag_options, order_flag_field, dynamicmethod
from .flag_bits import FlagBits8, FlagBits16, FlagBits32, FlagBits64, FLAG_BITS_SELECTOR


__all__ = ['BitFlagsMetaclass', 'BitFlags', 'bitflags']


class BitFlagsMetaclass(type(ctypes.Union)):
    """Metaclass to help create a ctypes.Union class with a ctypes.LittleEndianStructure sub class to make a c bit flag.

    Example:

        ..code-block :: python

            >>> import ctypes
            >>>
            >>> class Flags_bits(ctypes.LittleEndianStructure):
            >>>     _fields_ = [
            >>>                 ("bit_0", ctypes.c_uint8, 1),  # asByte & 1
            >>>                 ('bit_1', ctypes.c_uint8, 1),  # asByte & 2
            >>>                 ]

    Attributes:
        options (OrderedDict): Dictionary of bit (int) key and a display name (str) value mapping.
            This is used in get_flags.
        fields (OrderedDict): Dictionary of variable name (str) key and bit (int) value mapping.
            This gives attribute access to the bits you want to get or set.
        nbytes (int): Number of bytes for this value. This also indicates that you can access
            bit_0, bit_1, bit_2 to bit_(nbytes * 8).
        nbits (int): The users set number of bits or just the total number of bits that are accessible.
        pattern (str)[None]: Pattern to map options to. Example: 'Bit %i' will make 'Bit 0', 'Bit 1', 'Bit 2' as options
        byteorder (str)['big']: Argument when converting to bytes ('big' or 'little').
        signed (bool)[False]: Key word argument for when converting to bytes.
    """

    CASE_TYPES = {
        "lower": to_lower_var_name,  # snake like but will not separate numbers
        "snake": to_snake_case,
        "camel": toCamelCase,
        "keep": to_keep_case,
    }

    def __new__(mcls, name, bases, attrs):
        nbytes = 1
        nbits = 0

        # Variable name case conversion function
        case_func = attrs.get("case_func", 
            mcls.CASE_TYPES.get(
                attrs.get("case_type"), 
                to_lower_var_name
            )
        )

        # Format the options which are the bits mapped to display names
        options = {}
        if 'options' in attrs and attrs['options']:
            options = attrs.pop('options')
            if isinstance(options, dict):
                options = options.items()

            # Sort the options
            options = collections.OrderedDict(sorted((order_flag_options(key, value) for key, value in options),
                                                     key=lambda item: item[0]))
            nbits = max(chain(options.keys(), (0,))) + 1
            nbytes = int((nbits + 7) // 8)

        # Format the fields which are the variable names mapped to bits
        if 'fields' in attrs and attrs['fields']:
            fields = attrs.pop('fields')
            if isinstance(fields, dict):
                fields = fields.items()
            fields = collections.OrderedDict(sorted((order_flag_field(key, value, case_func) for key, value in fields),
                                                    key=lambda item: item[1]))
            nbits = max(chain(fields.values(), (0,))) + 1
            nbytes = int((nbits + 7) // 8)

            if not options:
                options = collections.OrderedDict(((value, key) for key, value in fields.items()))

        else:
            fields = collections.OrderedDict((order_flag_field(key, value, case_func) for key, value in options.items()))

        # Get the number of bytes
        try:
            nbits = int(attrs['nbits'])
        except (KeyError, ValueError, TypeError):
            pass
        try:
            nbytes = max(int(attrs['nbytes']), nbytes)
        except (KeyError, ValueError, TypeError):
            try:
                nbytes = max(int((nbits + 7) // 8), nbytes)
            except (KeyError, ValueError, TypeError):
                pass

        # Format the pattern argument into options and fields.
        pattern_func = attrs.get('pattern_func', format_pattern)
        if 'pattern' in attrs and attrs['pattern']:
            pattern = attrs['pattern']
            for i in range(nbytes*8):
                if i not in options:
                    bit_pat = pattern_func(i, pattern)
                    options[i] = bit_pat
                    var_name = case_func(bit_pat)
                    if var_name:
                        fields[var_name] = i

        # Create options to fields mapping
        options_to_fields = collections.OrderedDict()
        for var_name, bit in fields.items():
            name = options.get(bit)
            if name:
                options_to_fields[name] = var_name

        # ===== Create the Union =====
        # Get the FlagBits type and int type (c_uint8, c_uint16, ...)
        try:
            flag_bits, int_type = FLAG_BITS_SELECTOR[nbytes]
        except (IndexError, TypeError):
            flag_bits, int_type = FlagBits8, ctypes.c_uint8

        # Attributes that form the C Union
        if '_anonymous_' not in attrs:
            attrs['_anonymous_'] = ('bit',)
        elif 'bit' not in attrs['_anonymous_']:
            attrs['_anonymous_'] = ('bit',) + attrs['_anonymous_']
        attrs['_fields_'] = [('bit', flag_bits), ('value', int_type)]

        # Additional helper attributes
        attrs['options'] = options
        attrs['fields'] = fields
        attrs['options_to_fields'] = options_to_fields
        attrs['nbytes'] = nbytes
        if 'nbits' not in attrs:
            attrs['nbits'] = nbits or nbytes * 8

        # Variables to convert to bytes
        if 'byteorder' not in attrs:
            if 'endian' in attrs:
                attrs['byteorder'] = attrs['endian']
            else:
                attrs['byteorder'] = 'big'

        if 'signed' not in attrs:
            attrs['signed'] = False

        attrs["case_func"] = case_func
        attrs["pattern_func"] = pattern_func

        # Create the new class
        new_cls = super().__new__(mcls, name, bases, attrs)
        return new_cls
    
    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)

        # Set the fields as attributes
        for var_name, bit in cls.fields.items():
            try:
                # Cannot set the variable name if it starts with a number
                setattr(cls, var_name, getattr(cls, 'bit_'+str(bit)))
            except:
                pass


class BitFlags(ctypes.Union, metaclass=BitFlagsMetaclass):
    """BitFlags class that can be easily inherited to create custom bit mappings.

    Note:
        The total number of bytes is not changeable once the class is created. To specify a larger number of bit flags,
        specify the nbytes or nbits key word argument.

    Example:

        ..code-block:: python

            >>> class CustomFlags(BitFlags):
            >>>     options = {0: 'flag1', 1: 'flag2', 2: 'flag3'}
            >>>
            >>> f = CustomFlags(flag1=1, flag2=0, flag3=1)
            >>> assert f.value == 0b101
            >>> assert f.flag1 == f.bit_0
            >>> assert f.flag1 == 1
            >>> assert f.flag2 == 0
            >>> assert f.flag3 == 1
            >>> assert f.get_flags() == ['flag1', 'flag3']

    Attributes:
        options (OrderedDict): Dictionary of bit (int) key and a display name (str) value mapping.
            This is used in get_flags.
        fields (OrderedDict): Dictionary of variable name (str) key and bit (int) value mapping.
            This gives attribute access to the bits you want to get or set.
        nbytes (int): Number of bytes for this value. This also indicates that you can access
            bit_0, bit_1, bit_2 to bit_(nbytes * 8).
        nbits (int): The users set number of bits or just the total number of bits that are accessible.
        pattern (str)[None]: Pattern to map options to. Example: 'Bit %i' will make 'Bit 0', 'Bit 1', 'Bit 2' as options
        pattern_func (callable)[bitflags.utils.format_pattern]: Function that takes in the bit position and pattern returing the formatted bit name.
        case_type (str)["lower"]: "lower", "snake", "camel", or "keep" to change the type of variable name case.
        case_func (callable)[bitflags.utils.to_lower_var_name]: Function to convert the formatted pattern name to a variable name.
        byteorder (str)['big']: Argument when converting to bytes ('big' or 'little').
        signed (bool)[False]: Key word argument for when converting to bytes.
    """

    case_type = "lower"
    _anonymous_ = ("bit",)  # Matches _fields_ "bit"
    _fields_ = [
                ("bit", FlagBits8),
                ("value", ctypes.c_uint8)
                ]

    def __new__(cls, value=0, **kwargs):
        """Create an instance of the BitFlags.

        Args:
            value (int/str)[0]: Initial value.
            kwargs (**dict): Dictionary of Initial values for the fields. 'bit_0=1', 'bit_1=1', 'my_flag'=1, ...
        """
        new_cls = super().__new__(cls, value=value)
        return new_cls

    def __init__(self, value=0, **kwargs):
        """Create a new dynamic BitFlags class and instance.

        Args:
            value (int/str)[0]: Initial value.
            kwargs (**dict): Dictionary of Initial values for the fields. 'bit_0=1', 'bit_1=1', 'my_flag'=1, ...
        """
        super().__init__(value=value)

        # Set the values for the fields
        for var_name in kwargs:
            setattr(self, var_name, kwargs[var_name])

    def set_flags(self, value):
        """Set the bit flags.

        Args:
            value (bytes/int/str/list/tuple): Bytes value, integer value, or list of string options to set.
        """
        if isinstance(value, bytes):
            byteorder = getattr(self, 'byteorder', None)
            if byteorder is None:
                byteorder = getattr(self, 'endian', 'big')
            signed = getattr(self, 'signed', False)
            self.value = int.from_bytes(value, byteorder=byteorder, signed=signed)
            return

        elif isinstance(value, int):
            self.value = value
            return

        elif not isinstance(value, (list, tuple)):
            value = [value]

        # Reset the value to 0
        self.value = 0

        # Loop through and set the bits for the found option/field names
        for name in value:
            name = self.options_to_fields.get(name, name)
            bit = self.fields.get(name, name)
            setattr(self, f'bit_{bit}', 1)

    def get_flags(self):
        """Return a list of flag names that are set/True."""
        return [self.options[bit] for name, bit in self.fields.items()
                if getattr(self, str(name), False) and bit in self.options]

    @classmethod
    def set_fields(cls, fields):
        """Change the fields and make them accessible attributes.

        Args:
            fields (dict/list/tuple): Field (variable_name (str), bit (int)) pairs.
        """
        old = cls.fields.copy()

        if isinstance(fields, dict):
            fields = fields.items()
        fields = collections.OrderedDict(sorted((order_flag_field(key, value, cls.case_func) for key, value in fields),
                                                key=lambda item: item[1]))
        cls.fields.clear()
        cls.fields.update(fields)

        # Update the attributes
        cls._update_fields(old)

    @classmethod
    def update_fields(cls, fields=None):
        """Update the fields and possibly change class variable names to access the data.

        Args:
            fields (dict/list/tuple): Field (variable_name (str), bit (int)) pairs.
        """
        old = cls.fields.copy()

        if fields is not None:
            if isinstance(fields, dict):
                fields = fields.items()
            fields = collections.OrderedDict(sorted((order_flag_field(key, value, cls.case_func) for key, value in fields),
                                                    key=lambda item: item[1]))
            cls.fields.update(fields)

        # Update the attributes
        cls._update_fields(old)

    @classmethod
    def _update_fields(cls, old=None):
        """Remove the old field attributes and set the new field attributes."""
        if old:
            # Remove the old field variable names
            for key in old:
                try:
                    delattr(cls, key)
                except:
                    pass

        # Set the new field variable names
        error = None
        for key, bit in cls.fields.items():
            try:
                bit_attr = getattr(cls, 'bit_' + str(bit))
                setattr(cls, key, bit_attr)
            except Exception as err:
                error = err

            if error:
                raise ValueError('Cannot set field %s. The variable name or bit (%i) is invalid.' % (key, bit))

    # ===== Type Conversion =====
    def to_hex(self, fmt=None):
        """Convert the value to hex.

        Args:
            fmt (str)[None]: String format "0x{:02X}". If None nbits is used for hex size.

        Returns:
            hex (str): Integer value converted to hex.
        """
        if fmt is None:
            if self.nbytes <= 2:  # if self.nbits <= 16:
                fmt = '0x{:02X}'
            elif self.nbytes <= 4:  # elif self.nbits <= 32:
                fmt = '0x{:04X}'
            else:
                fmt = '0x{:08X}'
        return fmt.format(int(self))

    def to_bits(self):
        """Convert the value to a string of bits."""
        fmt = '{:0' + str(self.nbits) + 'b}'
        return fmt.format(int(self))

    def __int__(self):
        return self.value

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self.get_flags())

    def __str__(self):
        return ', '.join(self.get_flags())

    def __bytes__(self):
        byteorder = getattr(self, 'byteorder', None)
        if byteorder is None:
            byteorder = getattr(self, 'endian', 'big')
        signed = getattr(self, 'signed', False)
        return self.value.to_bytes(self.nbytes, byteorder, signed=signed)

    def __getitem__(self, flag):
        flag = self._flag_to_attr(flag)
        if not hasattr(self, flag):
            raise KeyError('Invalid flag "{}"!'.format(flag))
        return getattr(self, flag)

    def __setitem__(self, flag, value):
        flag = self._flag_to_attr(flag)
        if not hasattr(self, flag):
            raise KeyError('Invalid flag "{}"!'.format(flag))
        setattr(self, str(flag), value)

    def _flag_to_attr(self, flag):
        """Return the attribute name or the given flag."""
        if not isinstance(flag, str):
            try:
                flag = self.options[flag]
            except (KeyError, ValueError, TypeError, Exception):
                pass
        else:
            try:
                flag = self.options_to_fields[flag]
            except (KeyError, ValueError, TypeError, Exception):
                pass
        if isinstance(flag, int):
            flag = 'bit_{}'.format(flag)
        flag = str(flag)
        return flag

    def get(self, flag, *default):
        """Return the given flag's value.

        Args:
            flag (int/str): Bit position (starting at 0) or string flag name.
            *default (object)[MISSING]: If given return the default and do not raise an error.

        Returns:
            value (int)[None]: 0 or 1. None if the flag does not exist.
        """
        return getattr(self, self._flag_to_attr(flag), *default)

    def set(self, flag, value=1):
        """Change the given flag.

        Args:
            flag (int/str): Bit position (starting at 0) or string flag name.
            value (int)[1]: Change the flag to this value (0 or 1).
        """
        setattr(self, self._flag_to_attr(flag), value)

    # Use get for dict compatibility. Keep old methods.
    get_flag = get
    set_flag = set

    @dynamicmethod
    def from_flags(cls, value):
        """Create a new BitFlags object from a list of flags."""
        if isinstance(cls, BitFlags):
            bit_flags = type(cls)()
        else:
            bit_flags = cls()

        for option in value:
            if option in bit_flags.options:
                bit = bit_flags.options[option]
                setattr(bit_flags, 'bit_'+str(bit), 1)

        return bit_flags

    @dynamicmethod
    def from_str(cls, value, delimiter=','):
        """Create a new BitFlags object from a string containing multiple flags."""
        return cls.from_flags(value.split(delimiter))

    @dynamicmethod
    def from_int(cls, value):
        """Create a new BitFlags object from the given integer"""
        return cls(value)

    @dynamicmethod
    def from_bytes(cls, value, byteorder=None, *, signed=None):
        """Create a new BitFlags object from the given bytes.

        Note:
            If this is called from the class it will use the class byteorder and signed values to convert the bytes
            to an integer. If this is called from an object/instance then it will use that byteorder and signed values.
            An object/instance byteorder and signed values may be different from a classes values.

        Args:
            value (bytes): Bytes to use for the bit flags.
            byteorder (str)[None]: Optional byteorder 'big' or 'little' used when converting the bites to an integer and
                back to bytes again.
            signed (bool)[None]: Optional signed argument used when converting the bites to an integer and back to
                bytes again.

        Returns:
            bit_flags (BitFlags): New bit flags object with byteorder and signed set from how the bytes were converted.
        """
        # Check if someone passed in an integer by mistake by possibly iterating through bytes.
        if isinstance(value, int):
            return cls.from_int(value)

        if byteorder is None:
            byteorder = cls.byteorder
        if signed is None:
            signed = cls.signed

        if isinstance(cls, BitFlags):
            bit_flags = type(cls)()
        else:
            bit_flags = cls()

        bit_flags.value = int.from_bytes(value, byteorder, signed=signed)
        bit_flags.byteorder = byteorder
        bit_flags.signed = signed
        return bit_flags

    # ===== Iterator =====
    def __iter__(self):
        """Iterate through every bit's value."""
        self.__index__ = 0
        return self

    def __next__(self):
        """Return the value of the next bit."""
        idx = self.__index__
        self.__index__ += 1

        if idx >= self.nbytes * 8:
            self.__index__ = 0
            raise StopIteration

        try:
            return getattr(self, 'bit_'+str(idx))
        except AttributeError:
            self.__index__ = 0
            raise StopIteration

    def next(self):
        """Return the value of the next bit."""
        return self.__next__()


class bitflags(BitFlags):
    """Create a dynamic bit flags object.

    Note:
        The total number of bytes is not changeable once the object is created. To specify a larger number of bit flags,
        specify the nbytes or nbits key word argument.

    Example:

        ..code-block:: python

            >>> f = bitflags(flag1=1, flag2=0, flag3=3, options={0: 'flag1', 1: 'flag2', 2: 'flag3'})
            >>> assert f.value == 0b101
            >>> assert f.flag1 == f.bit_0
            >>> assert f.flag1 == 1
            >>> assert f.flag2 == 0
            >>> assert f.flag3 == 1

    Attributes:
        options (OrderedDict): Dictionary of bit (int) key and a display name (str) value mapping.
            This is used in get_flags.
        fields (OrderedDict): Dictionary of variable name (str) key and bit (int) value mapping.
            This gives attribute access to the bits you want to get or set.
        nbytes (int): Number of bytes for this value. This also indicates that you can access
            bit_0, bit_1, bit_2 to bit_(nbytes * 8).
        nbits (int): The users set number of bits or just the total number of bits that are accessible.
        pattern (str)[None]: Pattern to map options to. Example: 'Bit %i' will make 'Bit 0', 'Bit 1', 'Bit 2' as options.
        pattern_func (callable)[bitflags.utils.format_pattern]: Function that takes in the bit position and pattern returing the formatted bit name.
        case_type (str)["lower"]: "lower", "snake", "camel", or "keep" to change the type of variable name case.
        case_func (callable)[bitflags.utils.to_lower_var_name]: Function to convert the formatted pattern name to a variable name.
        byteorder (str)['big']: Argument when converting to bytes ('big' or 'little').
        signed (bool)[False]: Key word argument for when converting to bytes.
    """
    def __new__(cls, value=0, options=None, fields=None, nbytes=None, nbits=None, pattern=None, pattern_func=None, case_type="lower", case_func=None, **kwargs):
        """Create a new dynamic BitFlags class and instance.

        Args:
            value (int/str)[0]: Initial value.
            options (dict/list)[None]: Bit (int) and Display Name (str) pairs to map a bit with a display name.
            fields (dict/list)[None]: variable_name (str) and bit (int) pairs to map a variable name to a specific bit.
            nbytes (int)[None]: Number of bytes.
            nbits (int)[None]: Number of bits.
            pattern (str)[None]: Pattern to map options to. Example: 'Bit %i' will make 'Bit 0', 'Bit 1', 'Bit 2' as options.
            pattern_func (callable)[bitflags.utils.format_pattern]: Function that takes in the bit position and pattern returing the formatted bit name.
            case_type (str)["lower"]: "lower", "snake", "camel", or "keep" to change the type of variable name case.
            case_func (callable)[bitflags.utils.to_lower_var_name]: Function to convert the formatted pattern name to a variable name.
            kwargs (**dict): Dictionary of Initial values for the fields. 'bit_0=1', 'bit_1=1', 'my_flag'=1, ...
        """
        # Check to use the normal BitFlags __new__
        if options is None and fields is None and nbytes is None and nbits is None:
            obj = super().__new__(value, **kwargs)

        else:
            # class CustomBitFlags(bitflags):
            #     options = options
            #     fields = fields
            #     nbytes = nbytes
            #     nbits = nbits
            #     pattern = pattern
            #     __new__ = BitFlags.__new__
            attrs = {
                'options': options, 
                'fields': fields, 
                'nbytes': nbytes, 
                'nbits': nbits,
                'pattern': pattern,
                'case_type': case_type,
                '__new__': BitFlags.__new__
            }
            if pattern_func is not None:
                attrs['pattern_func'] = pattern_func
            if case_func is not None:
                attrs['case_func'] = case_func
            CustomBitFlags = type('CustomBitFlags', (bitflags,), attrs)

            obj = super().__new__(CustomBitFlags, value=value, **kwargs)

        # Set mutable options and fields
        obj.options = obj.__class__.options.copy()
        obj.fields = obj.__class__.fields.copy()
        obj.options_to_fields = obj.__class__.options_to_fields.copy()

        return obj

    def __init__(self, value=0, options=None, fields=None, nbytes=None, nbits=None, pattern=None, pattern_func=None, case_type="lower", case_func=None, **kwargs):
        """Create a new dynamic BitFlags class and instance.

        Args:
            value (int/str)[0]: Initial value.
            options (dict/list)[None]: Bit (int) and Display Name (str) pairs to map a bit with a display name.
            fields (dict/list)[None]: variable_name (str) and bit (int) pairs to map a variable name to a specific bit.
            nbytes (int)[None]: Number of bytes.
            nbits (int)[None]: Number of bits.
            pattern (str)[None]: Pattern to map options to. Example: 'Bit %i' will make 'Bit 0', 'Bit 1', 'Bit 2' as options.
            pattern_func (callable)[bitflags.utils.format_pattern]: Function that takes in the bit position and pattern returing the formatted bit name.
            case_type (str)["lower"]: "lower", "snake", "camel", or "keep" to change the type of variable name case.
            case_func (callable)[bitflags.utils.to_lower_var_name]: Function to convert the formatted pattern name to a variable name.
            kwargs (**dict): Dictionary of Initial values for the fields. 'bit_0=1', 'bit_1=1', 'my_flag'=1, ...
        """
        super().__init__(value=value, **kwargs)

    # ===== Mutable Fields =====
    def __getattr__(self, key):
        try:
            return getattr(self, 'bit_' + str(self.fields[key]))
        except (AttributeError, KeyError):
            pass
        raise AttributeError('BitFlags has no attribute ' + repr(key) + ' see the "fields" attribute')

    def __setattr__(self, key, value):
        try:
            return super().__setattr__(key, value)
        except AttributeError as err:
            error = err
        try:
            return setattr(self, 'bit_' + str(self.fields[key]), value)
        except (AttributeError, KeyError):
            pass
        raise error
