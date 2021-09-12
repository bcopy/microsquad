import unittest

from microsquad.mapper.line_protocol_parser import LineProtocolParser
class TestPoint(unittest.TestCase):

    def setUp(self) -> None:
        self.parser = LineProtocolParser()
        return super().setUp()

    def test_simple_line(self):
        msg = self.parser.parse('measurement,tag=value field=12345423 123')
        expected = ('measurement',dict(tag='value'),dict(field=12345423),123)
        self.assertEqual(msg, expected)

    def test_no_fields(self):
        msg = self.parser.parse('measurement,tag=value 123')
        expected = ('measurement',dict(tag='value'),dict(),123)
        self.assertEqual(msg, expected)

    def test_no_tags(self):
        msg = self.parser.parse('measurement 123')
        expected = ('measurement',dict(),dict(),123)
        self.assertEqual(msg, expected)


if __name__ == '__main__':
    unittest.main()
