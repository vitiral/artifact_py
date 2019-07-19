import unittest
import networkx as nx

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


class TestGraph(unittest.TestCase):
    def setUp(self):
        self.g = nx.DiGraph()

    def test_add(self):
        n1 = name.new("REQ-foo")
        self.g.add_node(n1)
        n2 = name.new("REQ-foo")
        assert n1 in self.g
        assert n2 in self.g
        assert self.g[n1] == self.g[n2]

    def test_edge(self):
        n1 = name.new("REQ-foo")
        n2 = name.new("REQ-bar")

        n1_ = name.new("REQ-foo")
        n2_ = name.new("REQ-bar")

        self.g.add_edge(n1, n2)
        assert n1 in self.g
        assert n2 in self.g
        assert self.g.has_edge(n1, n2)
        assert self.g.has_edge(n1_, n2_)
