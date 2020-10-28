========
bitflags
========

Bit flags implementation using a C Union. This library removes the need to use ctypes and helps you quickly access what
bits are toggled.

This class is built off of the Bit Manipulation guide found at https://wiki.python.org/moin/BitManipulation under the
Bit fields section.

This library includes a class based approach to bit flags (BitFlags) and a one time dynamic bit flags object (bitflags).

The individual bits can always be accessed with 'flag.bit_0', 'flag.bit_1', 'flag.bit_2', ...


Example - BitFlags
==================
This is the class based approach.

.. code-block:: python

    from bitflags import BitFlags


    class MyFlags(BitFlags):
        options = {0: "flag1", 1: "flag2", 2: "flag3", 3: "flag4", 4: "Something Happened"}


    f = MyFlags(0)

    assert f.value == 0
    assert int(f) == 0

    f.value = 0b101  # 5 - bin(5) shows the bit values (0b101)
    assert f.value == 0b101

    # You can always access the bit value with 'bit_X'
    # Access all of the bits (The number of bits can be changed by setting the class attribute nbits or nbytes
    print(f.bit_7, f.bit_6, f.bit_5, f.bit_4, f.bit_3, f.bit_2, f.bit_1, f.bit_0)
    # 0 0 0 0 0 1 0 1

    # Access the custom flags as attributes
    assert f.flag1 == 1
    assert f.flag2 == 0
    assert f.flag3 == 1
    assert f.flag4 == 0
    assert f.something_happened == 0

    # Get a list of flag options
    assert f.get_flags() == ['flag1', 'flag3']

    # Convert to use the data types
    assert str(f) == 'flag1, flag3'
    assert int(f) == 5
    assert bytes(f) == b'\x05'


This class was made to be flexible if you want the attributes to be different from the display options.

.. code-block:: python

    from bitflags import BitFlags


    class MyFlags(BitFlags):
        options = {0: "Failure", 1: "Warning", 2: "System 2% Overloaded"}

    f = MyFlags(0b111)
    assert hasattr(f, 'failure')
    assert hasattr(f, 'warning')
    assert hasattr(f, 'system_2_overloaded')

    assert f.get_flags() == ['Failure', 'Warning', 'System 2% Overloaded']


    class SpecialFlags(BitFlags):
        options = {0: "2% System Failure",  # Note: variable name cannot start with a number!
                   1: "System Overloaded",
                   2: "System Safe"}
        fields = {'system_failure': 0, 'system_overload': 1, 'safe': 2}  # Custom variables to access the bits

    s = SpecialFlags(7)

    assert s.system_failure == 1
    assert s.system_overload == 1
    assert s.safe == 1

    assert s.get_flags() == ["2% System Failure", "System Overloaded", "System Safe"]


    s2 = SpecialFlags(1)
    assert s.get_flags() == ["2% System Failure"]


You can also make a pattern for options.

.. code-block:: python

    from bitflags import BitFlags


    class MyFlags(BitFlags):
        pattern = '%i'

    f = MyFlags()
    f.value = 0b101  # 5 - bin(5) shows the bit values (0b101)
    assert f.value == 0b101

    # Get a list of flag options
    assert f.get_flags() == ['0', '2']

    # Convert to use the data types
    assert str(f) == '0, 2'
    assert int(f) == 5
    assert bytes(f) == b'\x05'


Example - bitflags
==================

The one time object bit flags. This is basically the same thing as BitFlags only the instance constructor allows you
to set the options, fields, and number of bits/bytes.

.. code-block:: python

    from bitflags import bitflags

    f = bitflags(flag1=1, flag3=1, options={0: "flag1", 1: "flag2", 2: "flag3", 3: "flag4", 4: "Something Happened"})

    assert f.value == 0b101

    assert f.flag1 == 1
    assert f.flag2 == 0
    assert f.flag3 == 1
    assert f.flag4 == 0
    assert f.something_happened == 0

    # Change the fields that access the bits.
    f.set_fields({'a': 0, 'b': 1, 'c': 2, 'd': 3})

    assert f.a == f.bit_0
    assert f.b == f.bit_1
    assert f.c == f.bit_2
    assert f.d == f.bit_3


The bitflags constructor uses type to create a new BitFlags class. This class isn't really re-usable unless you access
that class from the object that was created.

.. code-block:: python

    from bitflags import bitflags

    f = bitflags(flag1=1, flag3=1, options={0: "flag1", 1: "flag2", 2: "flag3", 3: "flag4", 4: "Something Happened"})

    assert f.value == 0b101

    f2 = type(f)(0b1)
    assert f2.flag1 == 1
    assert f2.value == 1
    assert f.value == 0b101

    f3 = f.__class__(0b10)
    assert f3.flag1 == 0
    assert f3.flag2 == 1
    assert f3.value == 2
    assert f2.value == 1
    assert f.value == 0b101


If you want to use multiple bit flag objects that have the same fields then it is better to use BitFlags class 
inheritance.
