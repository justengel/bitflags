import sys
import ctypes


def make_field(i):
    return ('bit_{}'.format(i), ctypes.c_uint8, 1)


class _FlagBits1(ctypes.LittleEndianStructure):
    _fields_ = [make_field(0)]

class UFlagBits1(ctypes.Union):
    _anonymous_ = ("bits",)
    _fields_ = [
        ('bits', _FlagBits1),
        ('value', ctypes.c_uint8)
        ]


class _FlagBits8(ctypes.LittleEndianStructure):
    _fields_ = [make_field(i) for i in range(8)]


class UFlagBits8(ctypes.Union):
    _anonymous_ = ("bits",)
    _fields_ = [
        ('bits', _FlagBits8),
        ('value', ctypes.c_uint8)
        ]


class _FlagBits9(ctypes.LittleEndianStructure):
    _fields_ = [make_field(i) for i in range(9)]


class UFlagBits9(ctypes.Union):
    _anonymous_ = ("bits",)
    _fields_ = [
        ('bits', _FlagBits9),
        ('value', ctypes.c_uint16)
        ]


class _FlagBits16(ctypes.LittleEndianStructure):
    _fields_ = [make_field(i) for i in range(16)]


class UFlagBits16(ctypes.Union):
    _anonymous_ = ("bits",)
    _fields_ = [
        ('bits', _FlagBits16),
        ('value', ctypes.c_uint16)
        ]


class _FlagBits24(ctypes.LittleEndianStructure):
    _fields_ = [make_field(i) for i in range(24)]


class UFlagBits24(ctypes.Union):
    _anonymous_ = ("bits",)
    _fields_ = [
        ('bits', _FlagBits24),
        ('value', ctypes.c_uint32)
        ]


class _FlagBits32(ctypes.LittleEndianStructure):
    _fields_ = [make_field(i) for i in range(32)]


class UFlagBits32(ctypes.Union):
    _anonymous_ = ("bits",)
    _fields_ = [
        ('bits', _FlagBits32),
        ('value', ctypes.c_uint32)
        ]


class _FlagBits64(ctypes.LittleEndianStructure):
    _fields_ = [make_field(i) for i in range(64)]


class UFlagBits64(ctypes.Union):
    _anonymous_ = ("bits",)
    _fields_ = [
        ('bits', _FlagBits64),
        ('value', ctypes.c_uint64)
        ]


class _FlagBits96(ctypes.LittleEndianStructure):
    _fields_ = [make_field(i) for i in range(96)]


class UFlagBits96(ctypes.Union):
    _anonymous_ = ("bits",)
    _fields_ = [
        ('bits', _FlagBits96),
        ('value', ctypes.c_uint64)
        ]


class _FlagBits128(ctypes.LittleEndianStructure):
    _fields_ = [make_field(i) for i in range(128)]


class UFlagBits128(ctypes.Union):
    _anonymous_ = ("bits",)
    _fields_ = [
        ('bits', _FlagBits128),
        ('value', ctypes.c_uint64)
        ]


class _FlagBits129(ctypes.LittleEndianStructure):
    _fields_ = [make_field(i) for i in range(129)]


class UFlagBits129(ctypes.Union):
    _anonymous_ = ("bits",)
    _fields_ = [
        ('bits', _FlagBits129),
        ('value', ctypes.c_uint64)
        ]


def check_sizes():
    # sizeof = sys.getsizeof
    sizeof = ctypes.sizeof

    print('Flag 1 Size:', sizeof(_FlagBits1), sizeof(_FlagBits1()))
    print('Flag 8 Size:', sizeof(_FlagBits8), sizeof(_FlagBits8()))
    print('Flag 9 Size:', sizeof(_FlagBits9), sizeof(_FlagBits9()))
    print('Flag 16 Size:', sizeof(_FlagBits16), sizeof(_FlagBits16()))
    print('Flag 24 Size:', sizeof(_FlagBits24), sizeof(_FlagBits24()))
    print('Flag 32 Size:', sizeof(_FlagBits32), sizeof(_FlagBits32()))
    print('Flag 64 Size:', sizeof(_FlagBits64), sizeof(_FlagBits64()))
    print('Flag 96 Size:', sizeof(_FlagBits96), sizeof(_FlagBits96()))
    print('Flag 128 Size:', sizeof(_FlagBits128), sizeof(_FlagBits128()))
    print('Flag 129 Size:', sizeof(_FlagBits129), sizeof(_FlagBits129()))


def check_union_size():
    # sizeof = sys.getsizeof
    sizeof = ctypes.sizeof
    print('Union Flag 1 Size:', sizeof(UFlagBits1), sizeof(UFlagBits1()))
    print('Union Flag 8 Size:', sizeof(UFlagBits8), sizeof(UFlagBits8()))
    print('Union Flag 9 Size:', sizeof(UFlagBits9), sizeof(UFlagBits9()))
    print('Union Flag 16 Size:', sizeof(UFlagBits16), sizeof(UFlagBits16()))
    print('Union Flag 24 Size:', sizeof(UFlagBits24), sizeof(UFlagBits24()))
    print('Union Flag 32 Size:', sizeof(UFlagBits32), sizeof(UFlagBits32()))
    print('Union Flag 64 Size:', sizeof(UFlagBits64), sizeof(UFlagBits64()))
    print('Union Flag 96 Size:', sizeof(UFlagBits96), sizeof(UFlagBits96()))
    print('Union Flag 128 Size:', sizeof(UFlagBits128), sizeof(UFlagBits128()))
    print('Union Flag 129 Size:', sizeof(UFlagBits129), sizeof(UFlagBits129()))


def check_field_override():
    f = _FlagBits8()
    f.bit_0 = 1
    f.bit_1 = 0
    f.bit_2 = 1
    print("Checking field override:")
    for i in range(8):
        print(i, getattr(f, 'bit_{}'.format(i)))
    print()

    print("Cannot override _fields_:")
    f._fields_ = [('field_{}'.format(i), ctypes.c_uint8, 1) for i in range(8)]
    for i in range(8):
        print(i, getattr(f, 'field_{}'.format(i), None))
    print()

    # Errors
    # _FlagBits8._fields_ = [('field_{}'.format(i), ctypes.c_uint8, 1) for i in range(8)]
    # for i in range(8):
    #     print(i, getattr(f, 'field_{}'.format(i), None))


def check_union_fields():
    f = UFlagBits8(value=0b10000111)
    assert f.value == 0b10000111
    assert f.bit_0 == 1
    assert f.bit_1 == 1
    assert f.bit_2 == 1
    assert f.bit_3 == 0
    assert f.bit_4 == 0
    assert f.bit_5 == 0
    assert f.bit_6 == 0
    assert f.bit_7 == 1
    assert not hasattr(f, 'bit_8')

    f = UFlagBits16(value=0b1000000010000111)
    assert f.value == 0b1000000010000111
    assert f.bit_0 == 1
    assert f.bit_1 == 1
    assert f.bit_2 == 1
    assert f.bit_3 == 0
    assert f.bit_4 == 0
    assert f.bit_5 == 0
    assert f.bit_6 == 0
    assert f.bit_7 == 1
    assert f.bit_8 == 0
    assert f.bit_15 == 1
    assert not hasattr(f, 'bit_16')

    f = UFlagBits24(value=0b100000001000000010000111)
    assert f.value == 0b100000001000000010000111
    assert f.bit_0 == 1
    assert f.bit_1 == 1
    assert f.bit_2 == 1
    assert f.bit_3 == 0
    assert f.bit_4 == 0
    assert f.bit_5 == 0
    assert f.bit_6 == 0
    assert f.bit_7 == 1
    assert f.bit_8 == 0
    assert f.bit_15 == 1
    assert f.bit_16 == 0
    assert f.bit_23 == 1
    assert not hasattr(f, 'bit_24')

    print('finished check_union_fields')


if __name__ == '__main__':
    check_sizes()
    check_union_size()

    check_field_override()
    check_union_fields()
