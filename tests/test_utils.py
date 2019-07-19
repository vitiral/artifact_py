import os
import unittest

from artifact_py import utils


class TestPaths(unittest.TestCase):
    """Test assumptions about paths."""
    def setUp(self):
        self.cwd = os.getcwd()
        self.cwd_parent = os.path.dirname(self.cwd)

    def test_cwd(self):
        assert self.cwd == utils.abspath("./")
        assert self.cwd_parent == utils.abspath("./..")

    def test_join(self):
        assert '/root' == os.path.join('/any/long/path', '/root')
        assert '/a/b/' == os.path.join('/a/b/', '')

    def test_home(self):
        try:
            utils.abspath('~')
            assert False
        except ValueError:
            pass

    def test_dot(self):
        assert '/foo/bar/baz' == utils.abspath('/foo/./bar///baz')

    def test_dots(self):
        assert '/foo/bar/baz' == utils.abspath('/foo/bar/bob/../baz')

    def test_dots_cwd(self):
        assert os.path.join(self.cwd_parent,
                            'foo/bar') == utils.abspath('../foo/bar')
