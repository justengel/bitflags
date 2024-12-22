from bitflags import BitFlags


class MyFlags(BitFlags):
    case_type = "keep"
    
    options = {
        0:  'flag0',
        1:  'FLAG1'
    }

f = MyFlags(3)

assert f.get_flags() == ['flag0', 'FLAG1']
assert hasattr(f, 'FLAG1')
assert not hasattr(f, "flag1"), "Lowercase flag created"
assert hasattr(f, 'flag0')
