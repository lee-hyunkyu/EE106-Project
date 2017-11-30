from PriorityQueue import *
from Graph import *
import unittest
import string
import random
 
class TestPriorityQueue(unittest.TestCase):

    def test_priority_queue_with_number(self):
        q = PriorityQueue()
        a = list(range(100))
        random.shuffle(a)
        for i in a:
            q.add(i)

        self.assertTrue(len(q) == 100)
        for i in range(100):
            popped_value = q.pop()
            self.assertTrue(i == popped_value, popped_value)
            self.assertTrue(len(q) == 100 - i - 1)
    
    def test_priority_queue_with_nodes(self):
        nodes = [Node(i) for i in range(100)]
        random.shuffle(nodes)
        for i in range(100):
            nodes[i]._distance = i
        random.shuffle(nodes)

        q = PriorityQueue()
        for n in nodes:
            q.add(n)

        for i in range(100):
            self.assertTrue(q.pop().distance == i)

    def test_priority_queue(self):
        nodes = [Node(i) for i in range(100)]
        random.shuffle(nodes)
        for i in range(100):
            nodes[i]._distance = i
        random.shuffle(nodes)

        q = PriorityQueue()
        for n in nodes:
            q.add(n)

        for n in nodes:
            if random.random() > 0.5:
                n._distance = n._distance * 3
                q.heapify()

        prev = q.pop().distance
        for i in range(99):
            curr = q.pop().distance
            self.assertTrue(prev <= curr)
            prev = curr

if __name__ == '__main__':
    unittest.main()