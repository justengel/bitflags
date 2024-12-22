from bitflags import bitflags, BitFlags


def test_bitflags():
    f = bitflags(0, options={0: 'logout', 1: 'login', 2: 'profile', 3: 'Custom Action'})
    # Same As
    # class CustomFlags(BitFlags):
    #     options={0: 'logout', 1: 'login', 2: 'profile', 3: 'Custom Action'}

    assert f.nbytes == 1
    assert hasattr(f, 'bit_0')
    assert hasattr(f, 'bit_1')
    assert hasattr(f, 'bit_2')
    assert hasattr(f, 'bit_3')
    assert hasattr(f, 'bit_4')
    assert hasattr(f, 'bit_5')
    assert hasattr(f, 'bit_6')
    assert hasattr(f, 'bit_7')

    assert hasattr(f, 'logout')
    assert hasattr(f, 'login')
    assert hasattr(f, 'profile')
    assert hasattr(f, 'custom_action')

    f.value = 0b11

    assert f.value == 0b11
    assert f.bit_0 == 1
    assert f.bit_1 == 1
    assert f.bit_2 == 0
    assert f.bit_3 == 0
    assert f.logout == f.bit_0
    assert f.login == f.bit_1
    assert f.profile == f.bit_2
    assert f.custom_action == f.bit_3

    assert f.get_flags() == ['logout', 'login']

    # Test nbytes
    f = bitflags(0, options={0: 'logout', 1: 'login', 2: 'profile', 3: 'Custom Action'}, nbytes=2)
    # Same As
    # class CustomFlags(BitFlags):
    #     options = {0: 'logout', 1: 'login', 2: 'profile', 3: 'Custom Action'}
    #     nbytes = 2

    assert f.nbytes == 2
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


def test_kwargs():
    f = bitflags(flag1=1, flag2=0, flag3=3, options={0: 'flag1', 1: 'flag2', 2: 'flag3'})
    assert f.value == 0b101
    assert f['flag1'] == f.bit_0
    assert f['flag2'] == f.bit_1
    assert f['flag3'] == f.bit_2
    assert f.flag1 == f.bit_0
    assert f.flag2 == f.bit_1
    assert f.flag3 == f.bit_2
    assert f.flag1 == 1
    assert f.flag2 == 0
    assert f.flag3 == 1

    f = bitflags(flag_1=1, flag_2=0, flag_3=3, options={0: 'flag1', 1: 'flag2', 2: 'flag3'}, case_type="snake")
    assert f.value == 0b101
    assert f['flag1'] == f.bit_0
    assert f['flag2'] == f.bit_1
    assert f['flag3'] == f.bit_2
    assert f.flag_1 == f.bit_0
    assert f.flag_2 == f.bit_1
    assert f.flag_3 == f.bit_2
    assert f.flag_1 == 1
    assert f.flag_2 == 0
    assert f.flag_3 == 1


def test_set_fields():
    f = bitflags(0b11, options={0: 'logout', 1: 'login', 2: 'profile', 3: 'Custom Action'}, nbytes=2)
    f.set_fields({'a': 1, 'b': 2, 'c': 3, 'd': 4})

    assert f.a == f.bit_1
    assert f.b == f.bit_2
    assert f.c == f.bit_3
    assert f.d == f.bit_4


def test_bitflags_reuse():
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


if __name__ == '__main__':
    test_bitflags()
    test_kwargs()
    test_set_fields()
    test_bitflags_reuse()
    print("All tests finished successfully!")
