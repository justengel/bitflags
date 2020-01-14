import sys
import ctypes


class _FlagBits(ctypes.LittleEndianStructure):
    _pack_ = 1
    #  This results in 6 bytes
    _fields_ = [('bit_1', ctypes.c_uint8, 1),
                ('value', ctypes.c_uint8, 2),
                ('v', ctypes.c_float),  # Float must be in continuous bytes
                ('bit_2', ctypes.c_uint8, 1),
                ('v2', ctypes.c_uint8, 4),
                ]
    #  This results in 5 bytes
    # _fields_ = [('bit_1', ctypes.c_uint8, 1),
    #             ('value', ctypes.c_uint8, 2),
    #             ('bit_2', ctypes.c_uint8, 1),
    #             ('v2', ctypes.c_uint8, 4),
    #             ('v', ctypes.c_float),  # Float must be in continuous bytes
    #             ]


f = _FlagBits(v=4.0)
print(sys.getsizeof(f), sys.getsizeof(_FlagBits))

print('bit_1', f.bit_1)
print('value', f.value)
print('v', f.v)
print('bit_2', f.bit_2)
print('v2', f.v2)

print('from_buffer')
f2 = _FlagBits.from_buffer_copy(bytes([0b00000111, 0b00111111, 0b00000000, 0b00000000, 0b00010000]))
print('bit_1', f2.bit_1)
print('value', f2.value)
print('v', f2.v)
print('bit_2', f2.bit_2)
print('v2', f2.v2)

#
# class UFlagBits(ctypes.Union):
#     _anonymous_ = ("bits",)
#     _fields_ = [
#         ('bits', _FlagBits),
#         ('value', ctypes.c_void_p)
#         ]
#
# u = UFlagBits(value=b'\x01\x02\x03')
# print(f.bit_1)
# print(f.value)
# print(f.v)
# print(f.bit_2)
