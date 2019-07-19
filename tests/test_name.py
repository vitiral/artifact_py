import unittest
import networkx as nx

from artifact_py.name import Name


class TestName(unittest.TestCase):
    def test_same(self):
        assert Name.from_str('REQ-foo') == Name.from_str('REQ-foo')

    def test_case(self):
        assert Name.from_str('req-foo') == Name.from_str('REQ-foo')

    def test_different_type(self):
        assert Name.from_str('SPC-foo') != Name.from_str('REQ-foo')

    def test_different_value(self):
        assert Name.from_str('REQ-bar') != Name.from_str('REQ-foo')


class TestGraph(unittest.TestCase):
    def setUp(self):
        self.g = nx.DiGraph()

    def test_add(self):
        n1 = Name.from_str("REQ-foo")
        self.g.add_node(n1)
        n2 = Name.from_str("REQ-foo")
        assert n1 in self.g
        assert n2 in self.g
        assert self.g[n1] == self.g[n2]

    def test_edge(self):
        n1 = Name.from_str("REQ-foo")
        n2 = Name.from_str("REQ-bar")

        n1_ = Name.from_str("REQ-foo")
        n2_ = Name.from_str("REQ-bar")

        self.g.add_edge(n1, n2)
        assert n1 in self.g
        assert n2 in self.g
        assert self.g.has_edge(n1, n2)
        assert self.g.has_edge(n1_, n2_)
