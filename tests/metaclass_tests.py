import ctypes
from bitflags.flag_bits import FlagBits8, FlagBits16, FlagBits32, FlagBits64


class _BitFlags(ctypes.Union):
    _anonymous_ = ("bit",)
    _fields_ = [
                ("bit", FlagBits32),
                ("value", ctypes.c_uint32)
                ]

f = _BitFlags()
f.value = 0b11111111111111111111111111111111  # 2**32
for i in range(32):
    assert getattr(f, 'bit_'+str(i)) == 1, i


class BitFlagsMetaclass(type(ctypes.Union)):
    """Metaclass to help create a ctypes.Union class with a ctypes.LittleEndianStructure sub class to make a c bit flag.

    Example:

        ..code-block :: python

            >>> import ctypes
            >>>
            >>> class Flags_bits(ctypes.LittleEndianStructure):
            >>>     _fields_ = [
            >>>                 ("bit_0", ctypes.c_uint8, 1),  # asByte & 1
            >>>                 ('bit_1', ctypes.c_uint8, 1),  # asByte & 1
    """
    def __new__(mcls, name, bases, attrs):
        print(name, bases, attrs)
        return super().__new__(mcls, name, bases, attrs)


class BitFlags(_BitFlags, metaclass=BitFlagsMetaclass):
    pass


class CustomFlags(BitFlags):
    _fields_ = [
                ("bit", FlagBits8),
                ("value", ctypes.c_uint8)
                ]

