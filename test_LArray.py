
import unittest

from LArray import LArray


class IterTestCase(unittest.TestCase):
    """Test __iter__."""

    def test_iter1(self):
        """Test iteration over an empty list."""
        lst = LArray()
        elems = []
        for elem in lst:
            elems.append(elem)
        self.assertEqual(elems, [])

    def test_iter2(self):
        """Test iteration over a list containing some duplicate elements."""
        lst = LArray([1, 4, 4, 1, 9, 4, 6, 6])
        elems = []
        for elem in lst:
            elems.append(elem)
        self.assertEqual(sorted(elems), [1, 1, 4, 4, 4, 6, 6, 9])


class ExtendTestCase(unittest.TestCase):
    """Test extend (Exercise 1)."""

    def test_extend1(self):
        """test extending an LArray with another"""
        list1 = LArray([1, 3, 5])
        list2 = LArray([2, 4, 6])
        list1.extend(list2)
        self.assertEqual(list1, LArray([1, 3, 5, 2, 4, 6]))

    def test_extend2(self):
        """test adding a tuple to LArray"""
        list1 = LArray([10, 20, 30])
        tup = (60, 50, 40)
        list1.extend(tup)
        self.assertEqual(list1, LArray([10, 20, 30, 60, 50, 40]))


class IndexTestCase(unittest.TestCase):
    """Test index (Exercise 2)."""

    def test_index1(self):
        """Test an empty list."""
        lst = LArray()
        with self.assertRaises(ValueError):
            lst.index(10)

    def test_index2(self):
        """Test finding the index of an item that isn't in the list."""
        lst = LArray([1, 3, 4, 4, 7, 2, 3])
        with self.assertRaises(ValueError):
            lst.index(10)

    def test_index3(self):
        """Test index at beginning of array"""
        lst = LArray([10, 20, 30])
        self.assertEqual(lst.index(10), 0)

    def test_index4(self):
        """Test indexing in the middle of array"""
        lst = LArray([10, 20, 30])
        self.assertEqual(lst.index(20), 1)

    def test_index5(self):
        """Test indexing at end of array"""
        lst = LArray([10, 20, 30])
        self.assertEqual(lst.index(30), 2)


class PopTestCase(unittest.TestCase):
    """Test pop (Exercise 3)."""

    def test_pop1(self):
        """Test popping an item from an empty list."""
        lst = LArray()
        with self.assertRaises(IndexError):
            lst.pop(0)

    def test_pop2(self):
        """Test popping from a location with an invalid index."""
        lst = LArray([1, 3, 4, 4, 7, 2, 3])
        with self.assertRaises(IndexError):
            lst.pop(len(lst))
        with self.assertRaises(IndexError):
            lst.pop(-len(lst) - 1)

    def test_pop3(self):
        """test popping from the beginning of LArray"""
        lst = LArray([1, 4, 3, 6])
        self.assertEqual(lst.pop(0), 1)

    def test_pop4(self):
        """test popping from the end of LArray"""
        lst = LArray([1, 4, 3, 6])
        self.assertEqual(lst.pop(), 6)

    def test_pop5(self):
        """Test poppung from negative index"""
        lst = LArray([1, 4, 3, 6])
        self.assertEqual(lst.pop(-3), 4)


class ReversedTestCase(unittest.TestCase):
    """Test __reversed__ (Exercise 4)."""

    def test_reversed1(self):
        """Test iteration over an empty list."""
        lst = LArray()
        elems = []
        for elem in lst.__reversed__():
            elems.append(elem)
        self.assertEqual(elems, [])

    def test_reversed2(self):
        """Test iteration over a list containing some duplicate elements."""
        lst = LArray([1, 1, 4, 4, 4, 6, 6, 9])
        elems = []
        for elem in lst.__reversed__():
            elems.append(elem)
        self.assertEqual(elems, [9, 6, 6, 4, 4, 4, 1, 1])


if __name__ == '__main__':
    unittest.main(verbosity=2)
