from io import BytesIO


INT32_MAX = 2 ** 31 - 1
INT32_MIN = -2 ** 31


def from_int(v: int) -> bytes:
    if not INT32_MIN <= v <= INT32_MAX:
        raise Exception('Invalid value!')
    b = b''
    for i in range(5):
        if i == 4:
            b += (v & 0b0000_1111).to_bytes(1, byteorder='little')
            break
        t = v & 0b0111_1111
        v >>= 7
        if v == 0:
            b += t.to_bytes(1, byteorder='little')
            break
        b += (t | 0b1000_0000).to_bytes(1, byteorder='little')
    return b


def to_int(b: BytesIO) -> int:
    v = 0
    for i in range(5):
        t = b.read1(1)[0]
        if i == 4 and t & 0b1111_0000 > 0:
            raise Exception('Invalid value!')
        v += (t & 0b0111_1111) << 7 * i
        if t & 0b1000_0000 == 0:
            break
    return int.from_bytes(v.to_bytes(4, byteorder='little'), byteorder='little', signed=True)
