

import ctypes


class LArray:

    def __init__(self, iterable=[]) -> None:
        """Initialize this LArray.

        If no iterable is provided, the new LArray is empty.
        Otherwise, initialize the LArray by appending the values
        provided by the iterable.

        >>> lst = LArray()
        >>> lst
        LArray([])
        >>> lst = LArray([1, 4, 3, 6])
        >>> lst
        LArray([1, 4, 3, 6])
        """
        self._num_items = 0
        self._elems = _new_array(1)

        for elem in iterable:
            self.append(elem)

    def __str__(self) -> str:
        """Return a string representation of this LArray.

        >>> lst = LArray()
        >>> str(lst)
        '[]'
        >>> lst = LArray([1, 4, 3, 6])
        >>> str(lst)
        '[1, 4, 3, 6]'
        """
        return "[{0}]".format(", ".join([repr(x) for x in self]))

    def __repr__(self) -> str:
        """Return the canonical string representation of this LArray.

        >>> lst = LArray()
        >>> repr(lst)
        'LArray([])'
        >>> lst = LArray([1, 4, 3, 6])
        >>> repr(lst)
        'LArray([1, 4, 3, 6])'
        """

        return "{0}({1})".format(self.__class__.__name__, str(self))

    def __len__(self) -> int:
        """Return the number of elements in this LArray.

        >>> lst = LArray()
        >>> len(lst)
        0
        >>> lst = LArray([1, 4, 3, 6])
        >>> len(lst)
        4
        """
        return self._num_items

    def __iter__(self):
        """Return an iterator for this LArray.

        >>> lst = LArray([1, 4, 3, 6])
        >>> for x in lst:
        ...     print(x)
        ...
        1
        4
        3
        6
        """
        for i in range(len(self)):
            yield self[i]

    def __getitem__(self, i: int) -> any:
        """Return the element at index i.

        Raises IndexError if the index is out of range
        (i < 0 or i >= len(self)).

        Note: Unlike Python's built-in list type, __getitem__() doesn't
        support negative indices.

        >>> lst = LArray([1, 4, 3, 6])
        >>> lst[0]
        1
        >>> lst[3]
        6
        """
        if 0 <= i < len(self):
            return self._elems[i]

        raise IndexError('LArray: index out of range')

    def __setitem__(self, i: int, x: any) -> None:
        """Replace the element at index i with x.

        Raises IndexError if the index is out of range
        (i < 0 or i >= len(self)).

        Note: Unlike Python's built-in list type, __setitem__() doesn't
        support negative indices.

        >>> lst = LArray([1, 4, 3, 6])
        >>> lst[0] = 10
        >>> lst
        LArray([10, 4, 3, 6])
        >>> lst[2] = 7
        >>> lst
        LArray([10, 4, 7, 6])
        """
        if 0 <= i < len(self):
            self._elems[i] = x
            return None

        raise IndexError('LArray: assignment index out of range')

    def __delitem__(self, i: int) -> None:
        """Remove the element at index i.

        Raises IndexError if the index is out of range
        (i < 0 or i >= len(self)).

        Note: Unlike Python's built-in list type, __delitem__() doesn't
        support negative indices.

        >>> lst = LArray([1, 4, 3, 6])
        >>> del lst[0]
        >>> lst
        LArray([4, 3, 6])
        >>> len(lst)
        3

        >>> del lst[2]
        >>> lst
        LArray([4, 3])
        >>> len(lst)
        2
        """
        if 0 <= i < len(self):

            self._elems[i:self._num_items - 1] = \
                self._elems[i + 1:self._num_items]
            self._num_items -= 1

            if len(self._elems) >= 3 * len(self):
                self._resize()

            return None

        raise IndexError('LArray: assignment index out of range')

    def __contains__(self, x: any) -> bool:
        """Return True if x is in this LArray; otherwise False.

        >>> lst = LArray([10, 20, 30, 20])
        >>> 10 in lst
        True
        >>> 40 in lst
        False
        """

        for i in range(len(self)):
            if self._elems[i] == x:
                return True
        return False

    def __add__(self, other: 'LArray') -> 'LArray':
        """Return a new LArray containing the concatenation of this LArray
        and other.

        Raises TypeError if other is not an LArray.

        >>> list1 = LArray([1, 3, 5])
        >>> list2 = LArray([2, 4, 6])
        >>> list3 = list1 + list2
        >>> list3
        LArray([1, 3, 5, 2, 4, 6])
        """
        if not isinstance(other, LArray):
            raise TypeError("can only concatenate LArray to LArray")

        newlist = LArray()
        n = len(self) + len(other)
        newlist._elems = _new_array(n)
        newlist._elems[0:len(self)] = self._elems[0:len(self)]
        newlist._elems[len(self):n] = other._elems[0:len(other)]
        newlist._num_items = n
        return newlist

    def __eq__(self, other: 'LArray') -> bool:
        """Return True if other equals this LArray.

        other and self are equal iff:
        (1) other is an LArray;
        (2) other and self contain the same number of items;
        (3) other[i] == self[i], for all i, 0 <= i < len(self)

        >>> lst1 = LArray([10, 20, 30])
        >>> lst2 = LArray([10, 20, 30])
        >>> lst1 == lst2
        True

        >>> tup = (10, 20, 30)  # compare to a tuple with the same elements
        >>> lst1 == tup
        False

        >>> lst2 = LArray([10, 20, 30, 20])
        >>> lst1 == lst2
        False
        """
        if not isinstance(other, LArray):
            return False

        if len(other) != len(self):
            return False

        for i in range(len(self)):
            if self._elems[i] != other._elems[i]:

                return False
        return True

    def append(self, x: any) -> None:
        """Append x to the end of this LArray.

        >>> lst = LArray([1, 4, 3, 6])
        >>> lst.append(2)
        >>> lst
        LArray([1, 4, 3, 6, 2])
        >>> len(lst)
        5
        """
        if len(self) == len(self._elems):

            self._resize()

        self._elems[self._num_items] = x
        self._num_items += 1

    def insert(self, i: int, x: any) -> None:
        """Insert x before index i in this LArray.
        If i >= len(self), append x to the list.

        Raises IndexError if the index is out of range (i < 0).

        Note: Unlike Python's built-in list type, insert() doesn't
        support negative indices.

        >>> lst = LArray([1, 4, 3, 6])
        >>> lst.insert(0, 10)
        >>> lst
        LArray([10, 1, 4, 3, 6])
        >>> len(lst)
        5

        >>> lst.insert(5, 7)  # append 7 to the list
        >>> lst
        LArray([10, 1, 4, 3, 6, 7])
        >>> len(lst)
        6
        """
        if self._num_items == len(self._elems):

            self._resize()

        if i < 0:
            raise IndexError('LArray: assignment index out of range')

        if i < len(self):

            self._elems[i + 1:self._num_items + 1] = \
                self._elems[i:self._num_items]
            self._elems[i] = x
            self._num_items += 1
        else:
            self.append(x)

    def extend(self, iterable) -> None:
        """Extend this LArray with the elements from the iterable.

        >>> list1 = LArray([1, 3, 5])
        >>> list2 = LArray([2, 4, 6])
        >>> list1.extend(list2)
        >>> list1
        LArray([1, 3, 5, 2, 4 6])

        >>> list1 = LArray([10, 20, 30])
        >>> tup = (60, 50, 40)
        >>> list1.extend(tup)
        >>> list1
        LArray([10, 20, 30, 60, 50, 40])
        """
        for i in iterable:
            self.append(i)

    def index(self, x: any) -> int:
        """Return the index of the first occurrence of x in this LArray.

        Raises ValueError if x is not in the list.

        >>> lst = LArray([10, 20, 30])
        >>> lst.index(10)
        0
        >>> lst.index(20)
        1
        """
        for i in range(len(self)):
            if self._elems[i] == x:
                return i
        raise ValueError("LArray.index(x): x is not in list")

    def pop(self, i: int = -1) -> any:
        """Remove and return the element at index i. By default, the last element is removed.

        Raises IndexError if the index is out of range.

        Note: Like Python's built-in list type, pop() supports negative indices.

        >>> lst = LArray([1, 4, 3, 6])
        >>> lst.pop()  # equivalent to lst.pop(-1)
        6
        >>> lst
        LArray([1, 4, 3])

        >>> lst = LArray([1, 4, 3, 6])
        >>> lst.pop(0)
        1
        >>> lst
        LArray([4, 3, 6])
        """
        if self._num_items == 0:
            raise IndexError("LArray: pop from empty list")
        elif i >= self._num_items or i < -len(self):
            raise IndexError("LArray: pop index out of range")

        value = self._elems[i]

        if -1 >= i >= -len(self):
            i += len(self)

        if 0 <= i < len(self):

            self._elems[i:self._num_items - 1] = \
                self._elems[i + 1:self._num_items]
            self._num_items -= 1

            if len(self._elems) >= 3 * len(self):
                self._resize()

        return value

    def __reversed__(self):
        """Return a reverse iterator for this LArray.

        >>> lst = LArray([1, 4, 3, 6])
        >>> for x in 
        :
        ...     print(x)
        ...
        6
        3
        4
        1
        """
        for i in range(len(self) - 1, -1, -1):
            yield self[i]

    def _resize(self) -> None:
        """Change this LArray's capacity to 2 * n, where n is the number of
        elements in the list. If the list is empty, change its capacity to 1.
        """

        arr = _new_array(max(1, 2 * self._num_items))

        arr[0:self._num_items] = self._elems[0:self._num_items]

        self._elems = arr


def _new_array(capacity: int) -> 'py_object_Array_<capacity>':
    """Return a new array with the specified capacity that stores
    references to Python objects. All elements are initialized to None.

    >>> arr = _new_array(10)
    >>> len(arr)
    10

    >>> for i in range(10):
    ...      a[i] = 2 * i
    ...

    >>> arr[0]
    0
    >>> arr[9]
    18

    >>> 4 in arr
    True
    >>> 3 in arr
    False
    """
    if capacity <= 0:
        raise ValueError('new_array: capacity must be > 0')

    PyCArrayType = ctypes.py_object * capacity
    a = PyCArrayType()
    for i in range(len(a)):
        a[i] = None

    return a
