import unittest

from artifact_py import name

class TestName(unittest.TestCase):
    def test_same(self):
        assert name.Name.from_str('REQ-foo') == name.Name.from_str('REQ-foo')

    def test_case(self):
        assert name.Name.from_str('req-foo') == name.Name.from_str('REQ-foo')

    def test_different_type(self):
        assert name.Name.from_str('SPC-foo') != name.Name.from_str('REQ-foo')

    def test_different_value(self):
        assert name.Name.from_str('REQ-bar') != name.Name.from_str('REQ-foo')
