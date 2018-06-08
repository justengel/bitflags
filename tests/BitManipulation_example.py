# Found at: https://wiki.python.org/moin/BitManipulation
import ctypes


class Flags_bits(ctypes.LittleEndianStructure):
    _fields_ = [
                ("logout",     ctypes.c_uint8, 1),  # asByte & 1
                ("userswitch", ctypes.c_uint8, 1),  # asByte & 2
                ("suspend",    ctypes.c_uint8, 1),  # asByte & 4
                ("idle",       ctypes.c_uint8, 1),  # asByte & 8
                ]


class Flags(ctypes.Union):
    _anonymous_ = ("bit",)
    _fields_ = [
                ("bit", Flags_bits),
                ("value", ctypes.c_uint8)
                ]


flags = Flags()
print(flags.value)
flags.value = 0x2
print( "logout: %i" % flags.bit.logout)
# `bit` is defined as anonymous field, so its fields can also be accessed directly:
print( "logout: %i" % flags.logout)
print( "userswitch:  %i" % flags.userswitch)
print( "suspend   :  %i" % flags.suspend)
print( "idle  : %i" % flags.idle)

# logout: 0
# logout: 0
# userswitch:  1
# suspend   :  0
# idle  : 0


# # DOES NOT WORK PROPERLY
# class AltFlags(ctypes.Union):
#     _fields_ = [
#         ("logout",     ctypes.c_uint8, 1),  # asByte & 1
#         ("userswitch", ctypes.c_uint8, 1),  # asByte & 2
#         ("suspend",    ctypes.c_uint8, 1),  # asByte & 4
#         ("idle",       ctypes.c_uint8, 1),  # asByte & 8
#         ("value", ctypes.c_uint8)
#         ]
#
#
# af = AltFlags()
# af.value = 0x3
#
# print('Alternate Flags logout', af.logout)
# print('Alternate Flags userswitch', af.userswitch)
# print('Alternate Flags suspend', af.suspend)
# print('Alternate Flags idle', af.idle)
# print('Alternate Flags value', af.value, bin(af.value))


# ===== Inheritance =====
class NewFlags_bits(ctypes.LittleEndianStructure):
    _fields_ = [
                ("a",     ctypes.c_uint8, 1),  # asByte & 1
                ("b", ctypes.c_uint8, 1),  # asByte & 2
                ("c",    ctypes.c_uint8, 1),  # asByte & 4
                ("d",       ctypes.c_uint8, 1),  # asByte & 8
                ]


class NewFlags(Flags):
    _fields_ = [
                ("bit", NewFlags_bits),
                ("value", ctypes.c_uint8)
                ]


flags = NewFlags()
print(flags.value)
flags.value = 0x2
print( "a: %i" % flags.bit.a)
# `bit` is defined as anonymous field, so its fields can also be accessed directly:
print( "a: %i" % flags.a)
print( "b:  %i" % flags.b)
print( "c   :  %i" % flags.c)
print( "d  : %i" % flags.d)
