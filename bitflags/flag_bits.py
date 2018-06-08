import ctypes


__all__ = ['FlagBits8', 'FlagBits16', 'FlagBits32', 'FlagBits64', 'FLAG_BITS_SELECTOR']


class FlagBits8(ctypes.LittleEndianStructure):
    _fields_ = [
                ("bit_0", ctypes.c_uint8, 1),
                ("bit_1", ctypes.c_uint8, 1),
                ("bit_2", ctypes.c_uint8, 1),
                ("bit_3", ctypes.c_uint8, 1),
                ("bit_4", ctypes.c_uint8, 1),
                ("bit_5", ctypes.c_uint8, 1),
                ("bit_6", ctypes.c_uint8, 1),
                ("bit_7", ctypes.c_uint8, 1),
                ]


class FlagBits16(ctypes.LittleEndianStructure):
    _fields_ = [
                ("bit_0", ctypes.c_uint8, 1),
                ("bit_1", ctypes.c_uint8, 1),
                ("bit_2", ctypes.c_uint8, 1),
                ("bit_3", ctypes.c_uint8, 1),
                ("bit_4", ctypes.c_uint8, 1),
                ("bit_5", ctypes.c_uint8, 1),
                ("bit_6", ctypes.c_uint8, 1),
                ("bit_7", ctypes.c_uint8, 1),

                ("bit_8", ctypes.c_uint8, 1),
                ("bit_9", ctypes.c_uint8, 1),
                ("bit_10", ctypes.c_uint8, 1),
                ("bit_11", ctypes.c_uint8, 1),
                ("bit_12", ctypes.c_uint8, 1),
                ("bit_13", ctypes.c_uint8, 1),
                ("bit_14", ctypes.c_uint8, 1),
                ("bit_15", ctypes.c_uint8, 1),
                ]


class FlagBits32(ctypes.LittleEndianStructure):
    _fields_ = [
                ("bit_0", ctypes.c_uint8, 1),
                ("bit_1", ctypes.c_uint8, 1),
                ("bit_2", ctypes.c_uint8, 1),
                ("bit_3", ctypes.c_uint8, 1),
                ("bit_4", ctypes.c_uint8, 1),
                ("bit_5", ctypes.c_uint8, 1),
                ("bit_6", ctypes.c_uint8, 1),
                ("bit_7", ctypes.c_uint8, 1),

                ("bit_8", ctypes.c_uint8, 1),
                ("bit_9", ctypes.c_uint8, 1),
                ("bit_10", ctypes.c_uint8, 1),
                ("bit_11", ctypes.c_uint8, 1),
                ("bit_12", ctypes.c_uint8, 1),
                ("bit_13", ctypes.c_uint8, 1),
                ("bit_14", ctypes.c_uint8, 1),
                ("bit_15", ctypes.c_uint8, 1),

                ("bit_16", ctypes.c_uint8, 1),
                ("bit_17", ctypes.c_uint8, 1),
                ("bit_18", ctypes.c_uint8, 1),
                ("bit_19", ctypes.c_uint8, 1),
                ("bit_20", ctypes.c_uint8, 1),
                ("bit_21", ctypes.c_uint8, 1),
                ("bit_22", ctypes.c_uint8, 1),
                ("bit_23", ctypes.c_uint8, 1),

                ("bit_24", ctypes.c_uint8, 1),
                ("bit_25", ctypes.c_uint8, 1),
                ("bit_26", ctypes.c_uint8, 1),
                ("bit_27", ctypes.c_uint8, 1),
                ("bit_28", ctypes.c_uint8, 1),
                ("bit_29", ctypes.c_uint8, 1),
                ("bit_30", ctypes.c_uint8, 1),
                ("bit_31", ctypes.c_uint8, 1),
                ]


class FlagBits64(ctypes.LittleEndianStructure):
    _fields_ = [
                ("bit_0", ctypes.c_uint8, 1),
                ("bit_1", ctypes.c_uint8, 1),
                ("bit_2", ctypes.c_uint8, 1),
                ("bit_3", ctypes.c_uint8, 1),
                ("bit_4", ctypes.c_uint8, 1),
                ("bit_5", ctypes.c_uint8, 1),
                ("bit_6", ctypes.c_uint8, 1),
                ("bit_7", ctypes.c_uint8, 1),

                ("bit_8", ctypes.c_uint8, 1),
                ("bit_9", ctypes.c_uint8, 1),
                ("bit_10", ctypes.c_uint8, 1),
                ("bit_11", ctypes.c_uint8, 1),
                ("bit_12", ctypes.c_uint8, 1),
                ("bit_13", ctypes.c_uint8, 1),
                ("bit_14", ctypes.c_uint8, 1),
                ("bit_15", ctypes.c_uint8, 1),

                ("bit_16", ctypes.c_uint8, 1),
                ("bit_17", ctypes.c_uint8, 1),
                ("bit_18", ctypes.c_uint8, 1),
                ("bit_19", ctypes.c_uint8, 1),
                ("bit_20", ctypes.c_uint8, 1),
                ("bit_21", ctypes.c_uint8, 1),
                ("bit_22", ctypes.c_uint8, 1),
                ("bit_23", ctypes.c_uint8, 1),

                ("bit_24", ctypes.c_uint8, 1),
                ("bit_25", ctypes.c_uint8, 1),
                ("bit_26", ctypes.c_uint8, 1),
                ("bit_27", ctypes.c_uint8, 1),
                ("bit_28", ctypes.c_uint8, 1),
                ("bit_29", ctypes.c_uint8, 1),
                ("bit_30", ctypes.c_uint8, 1),
                ("bit_31", ctypes.c_uint8, 1),

                ("bit_32", ctypes.c_uint8, 1),
                ("bit_33", ctypes.c_uint8, 1),
                ("bit_34", ctypes.c_uint8, 1),
                ("bit_35", ctypes.c_uint8, 1),
                ("bit_36", ctypes.c_uint8, 1),
                ("bit_37", ctypes.c_uint8, 1),
                ("bit_38", ctypes.c_uint8, 1),
                ("bit_39", ctypes.c_uint8, 1),

                ("bit_40", ctypes.c_uint8, 1),
                ("bit_41", ctypes.c_uint8, 1),
                ("bit_42", ctypes.c_uint8, 1),
                ("bit_43", ctypes.c_uint8, 1),
                ("bit_44", ctypes.c_uint8, 1),
                ("bit_45", ctypes.c_uint8, 1),
                ("bit_46", ctypes.c_uint8, 1),
                ("bit_47", ctypes.c_uint8, 1),

                ("bit_48", ctypes.c_uint8, 1),
                ("bit_49", ctypes.c_uint8, 1),
                ("bit_50", ctypes.c_uint8, 1),
                ("bit_51", ctypes.c_uint8, 1),
                ("bit_52", ctypes.c_uint8, 1),
                ("bit_53", ctypes.c_uint8, 1),
                ("bit_54", ctypes.c_uint8, 1),
                ("bit_55", ctypes.c_uint8, 1),

                ("bit_56", ctypes.c_uint8, 1),
                ("bit_57", ctypes.c_uint8, 1),
                ("bit_58", ctypes.c_uint8, 1),
                ("bit_59", ctypes.c_uint8, 1),
                ("bit_60", ctypes.c_uint8, 1),
                ("bit_61", ctypes.c_uint8, 1),
                ("bit_62", ctypes.c_uint8, 1),
                ("bit_63", ctypes.c_uint8, 1),
                ]


FLAG_BITS_SELECTOR = {0: (FlagBits8, ctypes.c_uint8), 1: (FlagBits8, ctypes.c_uint8),
                      2: (FlagBits16, ctypes.c_uint16),
                      3: (FlagBits32, ctypes.c_uint32), 4: (FlagBits32, ctypes.c_uint32),

                      5: (FlagBits64, ctypes.c_uint64), 6: (FlagBits64, ctypes.c_uint64),
                      7: (FlagBits64, ctypes.c_uint64), 8: (FlagBits64, ctypes.c_uint64)
                      }
