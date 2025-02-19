import collections
import ctypes
import time

from bitflags import BitFlags


def test_constructor():
    class CustomFlags(BitFlags):
        options = {0: 'logout', 1: 'login', 2: 'profile', 3: 'Custom Action'}

    assert ctypes.sizeof(CustomFlags) == 1
    assert CustomFlags.nbytes == 1, CustomFlags.nbytes
    assert hasattr(CustomFlags, 'bit_0')
    assert hasattr(CustomFlags, 'bit_1')
    assert hasattr(CustomFlags, 'bit_2')
    assert hasattr(CustomFlags, 'bit_3')
    assert hasattr(CustomFlags, 'bit_4')
    assert hasattr(CustomFlags, 'bit_5')
    assert hasattr(CustomFlags, 'bit_6')
    assert hasattr(CustomFlags, 'bit_7')
    assert not hasattr(CustomFlags, 'bit_8')

    f = CustomFlags()
    assert f.nbytes == 1
    assert f.value == 0
    assert f.logout == 0
    assert f.login == 0
    assert f.profile == 0
    assert f.custom_action == 0

    assert hasattr(f, 'bit_0')
    assert hasattr(f, 'bit_1')
    assert hasattr(f, 'bit_2')
    assert hasattr(f, 'bit_3')
    assert hasattr(f, 'bit_4')
    assert hasattr(f, 'bit_5')
    assert hasattr(f, 'bit_6')
    assert hasattr(f, 'bit_7')
    assert not hasattr(f, 'bit_8')

    assert f.logout == f.bit_0
    assert f.login == f.bit_1
    assert f.profile == f.bit_2
    assert f.custom_action == f.bit_3

    # Test initialization
    f = CustomFlags(0)
    assert f.nbytes == 1
    assert f.value == 0
    assert f.logout == 0
    assert f.login == 0
    assert f.profile == 0
    assert f.custom_action == 0

    assert hasattr(f, 'bit_0')
    assert hasattr(f, 'bit_1')
    assert hasattr(f, 'bit_2')
    assert hasattr(f, 'bit_3')
    assert hasattr(f, 'bit_4')
    assert hasattr(f, 'bit_5')
    assert hasattr(f, 'bit_6')
    assert hasattr(f, 'bit_7')
    assert not hasattr(f, 'bit_8')

    assert f.logout == f.bit_0
    assert f.login == f.bit_1
    assert f.profile == f.bit_2
    assert f.custom_action == f.bit_3

    # Test initialization
    f = CustomFlags(0b11)
    assert f.nbytes == 1
    assert f.value == 0b11
    assert f.value == 3
    assert f.bit_0 == 1
    assert f.bit_1 == 1
    assert not hasattr(f, 'bit_8')

    assert f.logout == f.bit_0
    assert f.login == f.bit_1
    assert f.profile == f.bit_2
    assert f.custom_action == f.bit_3

    # Test Large Initialization
    f = CustomFlags(0xFFFF)
    assert f.nbytes == 1
    assert f.value == 0xFF
    assert f.value == 255
    assert f.bit_0 == 1
    assert f.bit_1 == 1
    assert f.bit_2 == 1
    assert f.bit_3 == 1
    assert f.bit_4 == 1
    assert f.bit_5 == 1
    assert f.bit_6 == 1
    assert f.bit_7 == 1
    assert not hasattr(f, 'bit_8')

    assert f.logout == f.bit_0
    assert f.login == f.bit_1
    assert f.profile == f.bit_2
    assert f.custom_action == f.bit_3


def test_nbytes():
    class CustomFlags(BitFlags):
        nbytes = 2
        options = {0: 'logout', 1: 'login', 2: 'profile', 3: 'Custom Action'}

    assert ctypes.sizeof(CustomFlags) == 2
    assert CustomFlags.nbytes == 2
    assert hasattr(CustomFlags, 'bit_0')
    assert hasattr(CustomFlags, 'bit_1')
    assert hasattr(CustomFlags, 'bit_2')
    assert hasattr(CustomFlags, 'bit_3')
    assert hasattr(CustomFlags, 'bit_4')
    assert hasattr(CustomFlags, 'bit_5')
    assert hasattr(CustomFlags, 'bit_6')
    assert hasattr(CustomFlags, 'bit_7')

    assert hasattr(CustomFlags, 'bit_8')
    assert hasattr(CustomFlags, 'bit_9')
    assert hasattr(CustomFlags, 'bit_10')
    assert hasattr(CustomFlags, 'bit_11')
    assert hasattr(CustomFlags, 'bit_12')
    assert hasattr(CustomFlags, 'bit_13')
    assert hasattr(CustomFlags, 'bit_14')
    assert hasattr(CustomFlags, 'bit_15')
    assert not hasattr(CustomFlags, 'bit_16')

    f = CustomFlags()
    assert f.nbytes == 2
    assert f.value == 0
    assert f.logout == 0
    assert f.login == 0
    assert f.profile == 0
    assert f.custom_action == 0

    assert hasattr(f, 'bit_0')
    assert hasattr(f, 'bit_1')
    assert hasattr(f, 'bit_2')
    assert hasattr(f, 'bit_3')
    assert hasattr(f, 'bit_4')
    assert hasattr(f, 'bit_5')
    assert hasattr(f, 'bit_6')
    assert hasattr(f, 'bit_7')

    assert hasattr(f, 'bit_8')
    assert hasattr(f, 'bit_9')
    assert hasattr(f, 'bit_10')
    assert hasattr(f, 'bit_11')
    assert hasattr(f, 'bit_12')
    assert hasattr(f, 'bit_13')
    assert hasattr(f, 'bit_14')
    assert hasattr(f, 'bit_15')
    assert not hasattr(f, 'bit_16')

    assert f.logout == f.bit_0
    assert f.login == f.bit_1
    assert f.profile == f.bit_2
    assert f.custom_action == f.bit_3

    # Test large initialization
    f = CustomFlags(0xFFFF)
    assert f.value == 0xFFFF
    assert f.bit_0 == 1
    assert f.bit_1 == 1
    assert f.bit_2 == 1
    assert f.bit_15 == 1
    assert f.bit_14 == 1
    assert f.bit_13 == 1


def test_nbits():
    class CustomFlags(BitFlags):
        nbits = 10  # Still 2 bytes
        options = {0: 'logout', 1: 'login', 2: 'profile', 3: 'Custom Action'}

    assert CustomFlags.nbits == 10
    assert ctypes.sizeof(CustomFlags) == 2
    assert CustomFlags.nbytes == 2
    assert hasattr(CustomFlags, 'bit_0')
    assert hasattr(CustomFlags, 'bit_1')
    assert hasattr(CustomFlags, 'bit_2')
    assert hasattr(CustomFlags, 'bit_3')
    assert hasattr(CustomFlags, 'bit_4')
    assert hasattr(CustomFlags, 'bit_5')
    assert hasattr(CustomFlags, 'bit_6')
    assert hasattr(CustomFlags, 'bit_7')

    assert hasattr(CustomFlags, 'bit_8')
    assert hasattr(CustomFlags, 'bit_9')
    assert hasattr(CustomFlags, 'bit_10')
    assert hasattr(CustomFlags, 'bit_11')
    assert hasattr(CustomFlags, 'bit_12')
    assert hasattr(CustomFlags, 'bit_13')
    assert hasattr(CustomFlags, 'bit_14')
    assert hasattr(CustomFlags, 'bit_15')
    assert not hasattr(CustomFlags, 'bit_16')

    f = CustomFlags()
    assert f.nbytes == 2
    assert f.value == 0
    assert f.logout == 0
    assert f.login == 0
    assert f.profile == 0
    assert f.custom_action == 0

    assert hasattr(f, 'bit_0')
    assert hasattr(f, 'bit_1')
    assert hasattr(f, 'bit_2')
    assert hasattr(f, 'bit_3')
    assert hasattr(f, 'bit_4')
    assert hasattr(f, 'bit_5')
    assert hasattr(f, 'bit_6')
    assert hasattr(f, 'bit_7')

    assert hasattr(f, 'bit_8')
    assert hasattr(f, 'bit_9')
    assert hasattr(f, 'bit_10')
    assert hasattr(f, 'bit_11')
    assert hasattr(f, 'bit_12')
    assert hasattr(f, 'bit_13')
    assert hasattr(f, 'bit_14')
    assert hasattr(f, 'bit_15')
    assert not hasattr(f, 'bit_16')

    assert f.logout == f.bit_0
    assert f.login == f.bit_1
    assert f.profile == f.bit_2
    assert f.custom_action == f.bit_3

    # Test large initialization
    f = CustomFlags(0xFFFF)
    assert f.value == 0xFFFF
    assert f.bit_0 == 1
    assert f.bit_1 == 1
    assert f.bit_2 == 1
    assert f.bit_13 == 1
    assert f.bit_14 == 1
    assert f.bit_15 == 1


def test_field_options():
    # ===== Test Options: Setting the 'options' for display names and variable names (list/dict)  =====
    class CustomFlags(BitFlags):
        options = {0: 'logout', 1: 'login', 2: 'profile', 3: 'Custom Action'}

    # Options - bit, display name mappings
    assert isinstance(CustomFlags.options, collections.OrderedDict)
    assert list(range(4)) == list(CustomFlags.options.keys())
    assert CustomFlags.options == {0: 'logout', 1: 'login', 2: 'profile', 3: 'Custom Action'}

    # Fields - variable name, bit mappings
    assert isinstance(CustomFlags.fields, collections.OrderedDict)
    assert list(range(4)) == list(CustomFlags.fields.values())
    assert CustomFlags.fields == {'logout': 0, 'login': 1, 'profile': 2, 'custom_action': 3}

    # ===== Test Options: Test Odd Display name values =====
    class CustomFlags(BitFlags):
        options = {0: 'logout', 1: 'login', 2: 'profile', 3: 'Custom Action', 4: ' A 12345 Display *^&* Name  %m'}

    # Options - bit, display name mappings
    assert isinstance(CustomFlags.options, collections.OrderedDict)
    assert list(range(5)) == list(CustomFlags.options.keys())
    assert CustomFlags.options == {0: 'logout', 1: 'login', 2: 'profile', 3: 'Custom Action',
                                   4: ' A 12345 Display *^&* Name  %m'}

    # Fields - variable name, bit mappings
    assert isinstance(CustomFlags.fields, collections.OrderedDict)
    assert list(range(5)) == list(CustomFlags.fields.values())
    assert CustomFlags.fields == {'logout': 0, 'login': 1, 'profile': 2, 'custom_action': 3, '_a_12345_display_name_m': 4}

    # ===== Test Fields: Setting the 'fields' for variable names and display names (list/dict) =====
    class CustomFlags(BitFlags):
        fields = [('logout', 0), ('login', 1), ('profile', 2), ('custom_action', 3)]

    # Fields - variable name, bit mappings
    assert isinstance(CustomFlags.fields, collections.OrderedDict)
    assert list(range(4)) == list(CustomFlags.fields.values())
    assert CustomFlags.fields == {'logout': 0, 'login': 1, 'profile': 2, 'custom_action': 3}

    # Options - bit, display name mappings
    assert isinstance(CustomFlags.options, collections.OrderedDict)
    assert list(range(4)) == list(CustomFlags.options.keys())
    assert CustomFlags.options == {0: 'logout', 1: 'login', 2: 'profile', 3: 'custom_action'}

    # ===== Test Fields: Test Odd Display name values =====
    class CustomFlags(BitFlags):
        fields = {'logout': 0, 'login': 1, 'profile': 2, 'Custom Action': 3, ' A 12345 Display *^&* Name  %m': 4}

    # Fields - variable name, bit mappings
    assert isinstance(CustomFlags.fields, collections.OrderedDict)
    assert list(range(5)) == list(CustomFlags.fields.values())
    assert CustomFlags.fields == {'logout': 0, 'login': 1, 'profile': 2, 'custom_action': 3,
                                  '_a_12345_display_name_m': 4}

    # Options - bit, display name mappings
    assert isinstance(CustomFlags.options, collections.OrderedDict)
    assert list(range(5)) == list(CustomFlags.options.keys())
    assert CustomFlags.options == collections.OrderedDict([(0, 'logout'), (1, 'login'), (2, 'profile'),
                                                           (3, 'custom_action'), (4, '_a_12345_display_name_m')])

    # ===== Test Options and Fields: When both are set =====
    class CustomFlags(BitFlags):
        options = {0: 'logout', 1: 'login', 2: 'profile', 3: 'Custom Action', 4: ' A 12345 Display *^&* Name  %m'}
        fields = {'logout': 0, 'login': 1, 'my_account': 2, 'custom_action': 3, 'reasonable_name': 4}

    # Options - bit, display name mappings
    assert isinstance(CustomFlags.options, collections.OrderedDict)
    assert list(range(5)) == list(CustomFlags.options.keys())
    assert CustomFlags.options == {0: 'logout', 1: 'login', 2: 'profile', 3: 'Custom Action',
                                   4: ' A 12345 Display *^&* Name  %m'}

    # Fields - variable name, bit mappings
    assert isinstance(CustomFlags.fields, collections.OrderedDict)
    assert list(range(5)) == list(CustomFlags.fields.values())
    assert CustomFlags.fields == {'logout': 0, 'login': 1, 'my_account': 2, 'custom_action': 3, 'reasonable_name': 4}

    # Test the variable names
    f = CustomFlags(0b10101)
    assert hasattr(f, 'logout')
    assert f.logout == f.bit_0
    assert f.logout == 1
    assert hasattr(f, 'login')
    assert f.login == f.bit_1
    assert f.login == 0
    assert hasattr(f, 'my_account')
    assert f.my_account == f.bit_2
    assert f.my_account == 1
    assert hasattr(f, 'custom_action')
    assert f.custom_action == f.bit_3
    assert f.custom_action == 0
    assert hasattr(f, 'reasonable_name')
    assert f.reasonable_name == f.bit_4
    assert f.reasonable_name == 1


def test_update_fields():
    """The ctypes library does not allow for these dynamic updates immediately. This works when debugging line by line,
    but it does not work when you just run the code.
    """
    return # DO NOT RUN THESE TESTS

    class CustomFlags(BitFlags):
        options = {0: 'logout', 1: 'login', 2: 'profile', 3: 'Custom Action'}

    assert hasattr(CustomFlags, 'logout')
    assert hasattr(CustomFlags, 'login')
    assert hasattr(CustomFlags, 'profile')
    assert hasattr(CustomFlags, 'custom_action')

    CustomFlags.set_fields({'one': 0, 'two': 1, 'three': 2, 'four': 3})

    assert not hasattr(CustomFlags, 'logout')
    assert not hasattr(CustomFlags, 'login')
    assert not hasattr(CustomFlags, 'profile')
    assert not hasattr(CustomFlags, 'custom_action')

    f = CustomFlags(0b10101)
    assert f.logout == f.bit_0
    assert f.login == f.bit_1
    assert f.profile == f.bit_2
    assert f.custom_action == f.bit_3

    assert not hasattr(CustomFlags, 'logout')
    assert hasattr(f, 'one')
    assert f.one == f.bit_0
    assert not hasattr(f, 'login')
    assert hasattr(f, 'two')
    assert f.two == f.bit_1
    assert not hasattr(f, 'profile')
    assert hasattr(f, 'three')
    assert f.three == f.bit_2
    assert not hasattr(f, 'custom_action')
    assert hasattr(f, 'four')
    assert f.four == f.bit_3


def check_all_bits(flag):
    # Loop through all values in range
    for bit in range(flag.nbytes * 8):
        # Set the value to the bit
        flag.value = bit
        check_bit_value(flag, bit)


def check_bit_value(flag, value):
    # Make sure every bit is correctly set
    for i, on_off in enumerate(bin(value)[2:].zfill(flag.nbytes*8)[::-1]):  # Reverse iterate through bin for all bits
        on_off = int(on_off)
        bit_set = getattr(flag, 'bit_'+str(i))
        msg = 'Value %i (%s), Checking Bit %i, The bit value should be %i' % (value, bin(value), i, ~bit_set)
        assert bit_set == on_off, msg


def test_value_and_bits():
    class CustomFlags(BitFlags):
        options = {0: 'logout', 1: 'login', 2: 'profile', 3: 'Custom Action'}

    f = CustomFlags()
    assert f.value == 0
    check_all_bits(f)

    class CustomFlags(BitFlags):
        nbytes = 2
        options = {0: 'logout', 1: 'login', 2: 'profile', 3: 'Custom Action'}

    f = CustomFlags(0xFF)
    assert f.value == 0xFF
    check_all_bits(f)

    f = CustomFlags(0xFF)
    assert f.value == 0xFF
    check_bit_value(f, 0xFF)

    f = CustomFlags(0xFFFF)
    assert f.value == 0xFFFF
    check_bit_value(f, 0xFFFF)

    f.value = 6534
    assert f.value == 6534
    check_bit_value(f, 6534)


def test_pattern():
    class CustomFlags(BitFlags):
        pattern = '%i'

    assert ctypes.sizeof(CustomFlags) == 1

    f = CustomFlags(0xff)
    assert ctypes.sizeof(f) == 1
    assert f.value == 0xff
    assert f.get_flags() == ['0', '1', '2', '3', '4', '5', '6', '7']

    # Test string format with .format
    class CustomFlags(BitFlags):
        pattern = '{:}'

    f = CustomFlags(0xff)
    assert f.value == 0xff
    assert f.get_flags() == ['0', '1', '2', '3', '4', '5', '6', '7']

    # Test multiple bytes
    class CustomFlags(BitFlags):
        pattern = 'B%i'
        nbytes = 2

    assert ctypes.sizeof(CustomFlags) == 2

    f = CustomFlags(0xff)
    assert ctypes.sizeof(f) == 2
    assert f.value == 0xff
    assert f.get_flags() == ['B0', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7']  # Only flags that are True
    assert hasattr(f, 'b0')
    assert hasattr(f, 'b1')
    assert hasattr(f, 'b2')
    assert hasattr(f, 'b3')
    assert hasattr(f, 'b4')
    assert hasattr(f, 'b5')
    assert hasattr(f, 'b6')
    assert hasattr(f, 'b7')
    assert hasattr(f, 'b8')
    assert hasattr(f, 'b9')
    assert hasattr(f, 'b10')
    assert hasattr(f, 'b11')
    assert hasattr(f, 'b12')
    assert hasattr(f, 'b13')
    assert hasattr(f, 'b14')
    assert hasattr(f, 'b15')


def test_pattern_variable_case():
    class CustomFlags(BitFlags):
        pattern = 'My BIT%i'
        nbytes = 2
        case_type = "lower"  # Default

    assert ctypes.sizeof(CustomFlags) == 2

    f = CustomFlags(0xff)
    assert ctypes.sizeof(f) == 2
    assert f.value == 0xff
    assert f["My BIT0"] == 1
    assert f.get_flags() == ['My BIT0', 'My BIT1', 'My BIT2', 'My BIT3', 'My BIT4', 'My BIT5', 'My BIT6',
                             'My BIT7']  # Only flags that are True
    assert hasattr(f, 'my_bit0')
    assert hasattr(f, 'my_bit1')
    assert hasattr(f, 'my_bit2')
    assert hasattr(f, 'my_bit3')
    assert hasattr(f, 'my_bit4')
    assert hasattr(f, 'my_bit5')
    assert hasattr(f, 'my_bit6')
    assert hasattr(f, 'my_bit7')
    assert hasattr(f, 'my_bit8')
    assert hasattr(f, 'my_bit9')
    assert hasattr(f, 'my_bit10')
    assert hasattr(f, 'my_bit11')
    assert hasattr(f, 'my_bit12')
    assert hasattr(f, 'my_bit13')
    assert hasattr(f, 'my_bit14')
    assert hasattr(f, 'my_bit15')


    class CustomFlags(BitFlags):
        pattern = 'My BIT%i'
        nbytes = 2
        case_type = "snake"

    assert ctypes.sizeof(CustomFlags) == 2

    f = CustomFlags(0xff)
    assert ctypes.sizeof(f) == 2
    assert f.value == 0xff
    assert f["My BIT0"] == 1
    assert f.get_flags() == ['My BIT0', 'My BIT1', 'My BIT2', 'My BIT3', 'My BIT4', 'My BIT5', 'My BIT6',
                             'My BIT7']  # Only flags that are True
    assert hasattr(f, 'my_bit_0')
    assert hasattr(f, 'my_bit_1')
    assert hasattr(f, 'my_bit_2')
    assert hasattr(f, 'my_bit_3')
    assert hasattr(f, 'my_bit_4')
    assert hasattr(f, 'my_bit_5')
    assert hasattr(f, 'my_bit_6')
    assert hasattr(f, 'my_bit_7')
    assert hasattr(f, 'my_bit_8')
    assert hasattr(f, 'my_bit_9')
    assert hasattr(f, 'my_bit_10')
    assert hasattr(f, 'my_bit_11')
    assert hasattr(f, 'my_bit_12')
    assert hasattr(f, 'my_bit_13')
    assert hasattr(f, 'my_bit_14')
    assert hasattr(f, 'my_bit_15')


    class CustomFlags(BitFlags):
        pattern = 'My BIT%i'
        nbytes = 2
        case_type = "camel"

    assert ctypes.sizeof(CustomFlags) == 2

    f = CustomFlags(0xff)
    assert ctypes.sizeof(f) == 2
    assert f.value == 0xff
    assert f["My BIT0"] == 1
    assert f.get_flags() == ['My BIT0', 'My BIT1', 'My BIT2', 'My BIT3', 'My BIT4', 'My BIT5', 'My BIT6',
                             'My BIT7']  # Only flags that are True
    assert hasattr(f, 'myBit0')
    assert hasattr(f, 'myBit1')
    assert hasattr(f, 'myBit2')
    assert hasattr(f, 'myBit3')
    assert hasattr(f, 'myBit4')
    assert hasattr(f, 'myBit5')
    assert hasattr(f, 'myBit6')
    assert hasattr(f, 'myBit7')
    assert hasattr(f, 'myBit8')
    assert hasattr(f, 'myBit9')
    assert hasattr(f, 'myBit10')
    assert hasattr(f, 'myBit11')
    assert hasattr(f, 'myBit12')
    assert hasattr(f, 'myBit13')
    assert hasattr(f, 'myBit14')
    assert hasattr(f, 'myBit15')


    class CustomFlags(BitFlags):
        pattern = 'My BIT{}'
        nbytes = 2
        case_type = "keep"

    assert ctypes.sizeof(CustomFlags) == 2

    f = CustomFlags(0xff)
    assert ctypes.sizeof(f) == 2
    assert f.value == 0xff
    assert f["My BIT0"] == 1
    assert f.get_flags() == ['My BIT0', 'My BIT1', 'My BIT2', 'My BIT3', 'My BIT4', 'My BIT5', 'My BIT6',
                             'My BIT7']  # Only flags that are True
    assert hasattr(f, 'My_BIT0')
    assert hasattr(f, 'My_BIT1')
    assert hasattr(f, 'My_BIT2')
    assert hasattr(f, 'My_BIT3')
    assert hasattr(f, 'My_BIT4')
    assert hasattr(f, 'My_BIT5')
    assert hasattr(f, 'My_BIT6')
    assert hasattr(f, 'My_BIT7')
    assert hasattr(f, 'My_BIT8')
    assert hasattr(f, 'My_BIT9')
    assert hasattr(f, 'My_BIT10')
    assert hasattr(f, 'My_BIT11')
    assert hasattr(f, 'My_BIT12')
    assert hasattr(f, 'My_BIT13')
    assert hasattr(f, 'My_BIT14')
    assert hasattr(f, 'My_BIT15')


    class CustomFlags(BitFlags):
        pattern = 'My BIT {}'
        pattern_func = lambda i, p: p.format(i + 1).upper().replace(" ", '-')
        nbytes = 2
        case_type = "keep"

    assert ctypes.sizeof(CustomFlags) == 2

    f = CustomFlags(0xff)
    assert ctypes.sizeof(f) == 2
    assert f.value == 0xff
    assert f["MY-BIT-1"] == 1
    assert f.get_flags() == ['MY-BIT-1', 'MY-BIT-2', 'MY-BIT-3', 'MY-BIT-4', 'MY-BIT-5', 'MY-BIT-6', 'MY-BIT-7',
                             'MY-BIT-8']  # Only flags that are True
    assert not hasattr(f, 'MY_BIT_0')
    assert hasattr(f, 'MY_BIT_1')
    assert hasattr(f, 'MY_BIT_2')
    assert hasattr(f, 'MY_BIT_3')
    assert hasattr(f, 'MY_BIT_4')
    assert hasattr(f, 'MY_BIT_5')
    assert hasattr(f, 'MY_BIT_6')
    assert hasattr(f, 'MY_BIT_7')
    assert hasattr(f, 'MY_BIT_8')
    assert hasattr(f, 'MY_BIT_9')
    assert hasattr(f, 'MY_BIT_10')
    assert hasattr(f, 'MY_BIT_11')
    assert hasattr(f, 'MY_BIT_12')
    assert hasattr(f, 'MY_BIT_13')
    assert hasattr(f, 'MY_BIT_14')
    assert hasattr(f, 'MY_BIT_15')
    assert hasattr(f, 'MY_BIT_16')


def test_iterator():
    class CustomFlags(BitFlags):
        nbytes = 2


    f = CustomFlags(0b101)

    # Iterate through the bit values.
    for i, val in enumerate(f):
        if i == 0 or i == 2:
            assert val == 1
        else:
            assert val == 0


def test_get_set_flags():
    class CustomFlags(BitFlags):
        options = {0: 'logout', 1: 'login', 2: 'profile', 3: 'Custom Action'}
        byteorder = 'big'

    f = CustomFlags(0b11)
    assert f.get_flags() == ['logout', 'login']

    f.set_flags(['profile', 'Custom Action'])
    assert f.get_flags() == ['profile', 'Custom Action']

    f.set_flags(1)
    assert f.get_flags() == ['logout']

    f.set_flags(b'\x00\x03')  # 0b11
    assert f.get_flags() == ['logout', 'login']

    f.value = 0
    f.byteorder = 'little'
    f.set_flags(b'\x03\x00')  # 0b11
    assert f.get_flags() == ['logout', 'login']

    # ===== Check set_flag/get_flag =====
    # Check str
    assert f.get_flags() == ['logout', 'login']
    f.set('login', 0)
    assert f.get('login') == 0
    assert f.get_flags() == ['logout']
    f.set('profile', 1)
    assert f.get('profile') == 1
    assert f.get_flags() == ['logout', 'profile']
    f.set_flag('bit_2', 0)
    assert f.get_flag('bit_2') == 0
    assert f.get_flags() == ['logout']
    f.set('login', 1)
    assert f.get('login') == 1
    assert f.get_flags() == ['logout', 'login']

    # Check int
    assert f.get_flags() == ['logout', 'login']
    f.set_flag(1, 0)
    assert f.get_flag(1) == 0
    assert f.get_flags() == ['logout']
    f.set(2, 1)
    assert f.get(2) == 1
    assert f.get_flags() == ['logout', 'profile']
    f[2] = 0
    assert f[2] == 0
    assert f.get_flags() == ['logout']

    # Check get default value
    try:
        f.get('nonexisting flag')
        raise AssertionError('get does not raise error for non existing')
    except AttributeError:
        pass  # Should hit here
    assert f.get('nonexisting flag', None) is None


def test_data_types():
    class CustomFlags(BitFlags):
        options = {0: 'logout', 1: 'login', 2: 'profile', 3: 'Custom Action'}

    f = CustomFlags(0b11)

    assert int(f) == 0b11
    assert str(f) == ', '.join(['logout', 'login'])
    assert bytes(f) == bytes([0b11])

    # Test multiple bytes
    class CustomFlags(BitFlags):
        options = {0: 'logout', 1: 'login', 2: 'profile', 3: 'Custom Action'}
        nbytes = 2

    f = CustomFlags(0xFF)
    assert int(f) == 0xFF
    assert str(f) == ', '.join(['logout', 'login', 'profile', 'Custom Action'])
    assert bytes(f) == b'\x00\xff', bytes(f)

    f.byteorder = 'little'
    assert bytes(f) == b'\xff\x00', bytes(f)


def test_from_bytes():
    """This really only matters if from_bytes is being used with bytes having more than 8 bits."""
    class CustomFlags(BitFlags):
        options = {0: 'logout', 1: 'login', 2: 'profile', 3: 'Custom Action'}
        nbytes = 2
        byteorder = 'big'
        signed = False

    bf = CustomFlags.from_bytes(b'\x00\x03')
    assert bf.value == 0b11

    f = CustomFlags()
    f.byteorder = 'little'

    # Conversion from bytes works from the class
    bf = f.from_bytes(b'\x00\x03')
    assert bf.value == 0b0000001100000000


def test_to_hex_bits():
    class CustomFlags(BitFlags):
        options = {0: 'logout', 1: 'login', 2: 'profile', 3: 'Custom Action'}
        nbytes = 4  # Used in to_hex
        byteorder = 'big'
        signed = False

    f = CustomFlags(0b101)
    assert int(f) == 5, '{} != {}'.format(int(f), 5)
    assert f.to_hex() == '0x0005', '{} != {}'.format(f.to_hex(), '0x0005')
    assert f.to_bits() == '0101', '{} != {}'.format(f.to_bits(), '0101')


if __name__ == '__main__':
    test_constructor()
    test_nbytes()
    test_nbits()
    test_field_options()
    test_update_fields()
    test_value_and_bits()
    test_pattern()
    test_pattern_variable_case()
    test_get_set_flags()
    test_data_types()
    test_from_bytes()
    test_to_hex_bits()
    print("All tests finished successfully!")
