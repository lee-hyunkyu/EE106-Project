from Graph import *
import unittest
import string
 
class TestGraph(unittest.TestCase):

    def setup(self):
        self.graph = Graph()
        for s in string.ascii_letters:
            self.graph.add_node(s)

        count = 0
        for i in range(len(self.graph.V)):
            for j in range(i+1, len(self.graph.V)):
                self.graph.add_edge(self.graph.V[i], self.graph.V[j], count + 1)
                count += 1

    def test_node_initialization(self):
        for n, i in zip(list(string.ascii_letters), range(len(string.ascii_letters))):
            node = Node(n, i)
            self.assertTrue(node.name  == n)
            self.assertTrue(node.index == i)

    def test_graph_initialization(self):
        G = Graph()
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
        self.assertTrue(len(self.graph.E) == count)
        for edge in self.graph.E:
            self.assertTrue(edge.node1.index < edge.node2.index)

        count = 0
        for edge in self.graph.E:
            self.assertTrue(edge.length == count)
            count += 1

    def test_get_neighbors(self):
        for vertex in self.graph.V:
            neighbors = self.graph.get_neighbors(vertex)
            self.assertTrue(neighbors == len(self.graph.V) - 1)
            for neighbor in neighbors:
                self.assertTrue(neighbors != vertex)

    def test_get_edge(self):
        for vertex in self.graph.V:
            neighbors = self.graph.get_neighbors(vertex)
            for neighbor in neighbors:
                edge1 = self.graph.get_edge(vertex, neighbor)
                edge2 = self.graph.get_edge(neighbor, vertex)
                self.assertTrue(edge1 == edge2)
                self.assertTrue(vertex in [edge1.node1, edge1.node2])
                self.assertTrue(vertex in [edge2.node1, edge2.node2])
                self.assertTrue(neighbor in [edge1.node1, edge1.node2])
                self.assertTrue(neighbor in [edge2.node1, edge2.node2])

    def test_breadth_first_search(self):
        pass

    def test_dijkstras(self):
        pass

    def test_find_min_path(self):
        pass

if __name__ == '__main__':
    unittest.main()