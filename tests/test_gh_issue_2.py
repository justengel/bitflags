from bitflags import BitFlags
import sys

class MyFlags(BitFlags):
    options = {
        0:  'b00',
        1:  'b01',
        2:  'b02',
        3:  'b03',
        4:  'b04',
        5:  'b05',
        6:  'b06',
        7:  'b07',
        8:  'b08',
        9:  'b09',
        10: 'b10',
        11: 'b11',
        12: 'b12',
        13: 'b13',
        14: 'b14',
        15: 'b15'
    }
f = MyFlags(65535)

print(sys.version)
assert f.get_flags() == ['b00', 'b01', 'b02', 'b03', 'b04', 'b05', 'b06', 'b07', 'b08', 'b09', 'b10', 'b11', 'b12', 'b13', 'b14', 'b15']
assert hasattr(f, 'b08')
