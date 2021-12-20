from io import BytesIO
from unittest import TestCase

from slp.varint import from_int, to_int


class TestVarint(TestCase):
    def test_from_int(self):
        self.assertEqual(b'\x00', from_int(0))
        self.assertEqual(b'\x01', from_int(1))
        self.assertEqual(b'\x02', from_int(2))
        self.assertEqual(b'\x7f', from_int(127))
        self.assertEqual(b'\x80\x01', from_int(128))
        self.assertEqual(b'\xff\x01', from_int(255))
        self.assertEqual(b'\xdd\xc7\x01', from_int(25565))
        self.assertEqual(b'\xff\xff\x7f', from_int(2097151))
        self.assertEqual(b'\xff\xff\xff\xff\x07', from_int(2147483647))
        self.assertEqual(b'\xff\xff\xff\xff\x0f', from_int(-1))
        self.assertEqual(b'\x80\x80\x80\x80\x08', from_int(-2147483648))

    def test_from_int_with_error(self):
        from_int(2 ** 31 - 1)
        with self.assertRaisesRegex(Exception, '^Invalid value!$') as e:
            from_int(2 ** 31)
        from_int(-2 ** 31)
        with self.assertRaisesRegex(Exception, '^Invalid value!$') as e:
            from_int(-2 ** 31 - 1)

    def test_to_int(self):
        self.assertEqual(0, to_int(BytesIO(b'\x00')))
        self.assertEqual(1, to_int(BytesIO(b'\x01')))
        self.assertEqual(2, to_int(BytesIO(b'\x02')))
        self.assertEqual(127, to_int(BytesIO(b'\x7f')))
        self.assertEqual(128, to_int(BytesIO(b'\x80\x01')))
        self.assertEqual(255, to_int(BytesIO(b'\xff\x01')))
        self.assertEqual(25565, to_int(BytesIO(b'\xdd\xc7\x01')))
        self.assertEqual(2097151, to_int(BytesIO(b'\xff\xff\x7f')))
        self.assertEqual(2147483647, to_int(BytesIO(b'\xff\xff\xff\xff\x07')))
        self.assertEqual(-1, to_int(BytesIO(b'\xff\xff\xff\xff\x0f')))
        self.assertEqual(-2147483648, to_int(BytesIO(b'\x80\x80\x80\x80\x08')))

    def test_to_int_with_error(self):
        to_int(BytesIO(b'\xff\xff\xff\xff\x0f'))
        with self.assertRaisesRegex(Exception, '^Invalid value!$'):
            to_int(BytesIO(b'\xff\xff\xff\xff\x1f'))
