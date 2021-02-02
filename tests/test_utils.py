

def test_int_from_bits():
    from bitflags import int_from_bits

    value = int_from_bits(0, 2)  # 101
    assert value == 5

    value = int_from_bits(0, 1, 2)
    assert value == 7


if __name__ == '__main__':
    test_int_from_bits()

    print('All tests passed successfully!')
