from Graph import *
import unittest
import string
 
class TestGraph(unittest.TestCase):

    def setup(self):
        self.graph = Graph()
        for s in string.ascii_letters:
            self.graph.add_node(s)

    def test_node_initialization(self):
        for n, i in zip(list(string.ascii_letters), range(len(string.ascii_letters))):
            node = Node(n, i)
            self.assertTrue(node.name  == n)
            self.assertTrue(node.index == i)

    def test_graph_initialization(self):
        G = Graph({}, {}, 0)
        self.assertTrue(len(G.V)     == 0)
        self.assertTrue(len(G.E)     == 0)
        self.assertTrue(G.nextIndex  == 0)

    def test_add_node(self):
        G = Graph()
        for s in string.ascii_letters:
            G.add_node(s)

        self.assertTrue(len(G.V) == len(string.ascii_letters))
        for v, s, i in zip(G.V.values(), string.ascii_letters, range(len(G.V))):
            self.assertTrue(v.name is s)
            self.assertTrue(v.index is i)
        self.assertTrue(G.nextIndex is len(G.V))

    def test_add_edge(self):
        pass

    def test_get_neighbors(self):
        pass

    def test_get_edge(self):
        pass

    def test_breadth_first_search(self):
        pass

    def test_dijkstras(self):
        pass

    def test_find_min_path(self):
        pass

if __name__ == '__main__':
    unittest.main()