import unittest
from hypothesis import given
from typing import List, Optional
import hypothesis.strategies as st
from list import (
    cons,
    UnrolledNode,
    UnrolledLinkedList,
    from_list,
    size,
    add,
    add_to_end,
    find,
    remove,
    to_list,
    iterator,
    member,
    reduce,
    reverse,
    m_concat,
    url_filter,
    url_map,
    url_set,
    url_empty,
)


class Test(unittest.TestCase):

    def test_UnrolledNode_equality(self) -> None:
        self.assertEqual(cons([], None, 0), UnrolledNode([], None, 0))
        self.assertEqual(
            cons([], cons([], None, 0), 0),
            UnrolledNode([], UnrolledNode([], None, 0), 0),
        )

    @given(values=st.lists(st.integers()), capacity=st.integers(min_value=1))
    def test_UnrolledLinkedList_equality(self,
                                         values: List[int], capacity) -> None:
        lst1: Optional[UnrolledLinkedList] = from_list(values, capacity)
        lst2: Optional[UnrolledLinkedList] = from_list(values, capacity)
        self.assertEqual(lst1, lst2)

    @given(values=st.lists(st.integers()), capacity=st.integers(min_value=1))
    def test_size(self, values: List[int], capacity: int) -> None:
        self.assertEqual(size(UnrolledLinkedList()), 0)
        self.assertEqual(size(UnrolledLinkedList(0)), 0)
        self.assertEqual(size(from_list(values, capacity)), len(values))

    @given(values=st.lists(st.integers()), capacity=st.integers(min_value=1))
    def test_add(self, values: List[int], capacity: int) -> None:
        lst: UnrolledLinkedList = UnrolledLinkedList(capacity)
        for value in values:
            lst = add(lst, value)
        self.assertEqual(to_list(lst), values)

    @given(capacity=st.integers(min_value=1))
    def test_find(self, capacity: int) -> None:
        lst1: UnrolledLinkedList = UnrolledLinkedList()
        self.assertIsNone(find(lst1, lambda x: x % 2 == 0))

        lst2: Optional[UnrolledLinkedList] = (
            from_list([1, 2, 3, 4, 5], capacity))
        self.assertEqual(find(lst2, lambda x: x % 2 == 0), 2)

        lst3: Optional[UnrolledLinkedList] = (
            from_list([1, 3, 5, 7, 9], capacity))
        self.assertIsNone(find(lst3, lambda x: x % 2 == 0), None)

    @given(capacity=st.integers(min_value=1))
    def test_member(self, capacity: int) -> None:
        lst: Optional[UnrolledLinkedList] = from_list([1, 2, 3, 4], capacity)
        self.assertTrue(member(lst, 3))
        self.assertFalse(member(lst, 5))

    @given(values=st.lists(st.integers()), capacity=st.integers(min_value=1))
    def test_url_set(self, values: List[int], capacity: int) -> None:
        lst1: UnrolledLinkedList = UnrolledLinkedList(capacity)
        with self.assertRaises(IndexError):
            url_set(lst1, 0, 1)
        if values:
            lst2: Optional[UnrolledLinkedList] = from_list(values, capacity)
            new_value: int = capacity
            index: int = max(len(values) - 1, 0)
            lst2 = url_set(lst2, index, new_value)
            values[index] = new_value
            self.assertEqual(to_list(lst2), values)
            with self.assertRaises(IndexError):
                url_set(lst2, len(values), new_value)

    @given(values=st.lists(st.integers()), capacity=st.integers(min_value=1))
    def test_from_to_list(self, values: List[int], capacity: int) -> None:
        lst1: Optional[UnrolledLinkedList] = from_list([])
        self.assertEqual(to_list(lst1), [])
        self.assertEqual(to_list(from_list(values, capacity)), values)

    @given(values=st.lists(st.integers()), capacity=st.integers(min_value=1))
    def test_remove(self, values: List[int], capacity: int) -> None:
        lst: Optional[UnrolledLinkedList] = (
            from_list([2, 1, 1, 1, 1], capacity))
        lst = remove(lst, 3)
        self.assertEqual(to_list(lst), [2, 1, 1, 1, 1])
        lst = remove(lst, 2)
        self.assertEqual(to_list(lst), [1, 1, 1, 1])
        lst = remove(lst, 1)
        self.assertEqual(to_list(lst), [])
        lst = remove(lst, 0)
        self.assertEqual(to_list(lst), [])
        lst = from_list(values, capacity)
        for value in values:
            lst = remove(lst, value)
        self.assertEqual(to_list(lst), [])

    @given(values=st.lists(st.integers()), capacity=st.integers(min_value=1))
    def test_reverse(self, values: List[int], capacity: int) -> None:
        lst1: UnrolledLinkedList = UnrolledLinkedList(capacity)
        lst1 = reverse(lst1)
        self.assertEqual(to_list(lst1), [])
        lst2: Optional[UnrolledLinkedList] = from_list([1], capacity)
        lst2 = reverse(lst2)
        self.assertEqual(to_list(lst2), [1])
        lst3: Optional[UnrolledLinkedList] = from_list(values, capacity)
        lst3 = reverse(lst3)
        self.assertEqual(to_list(lst3), list(reversed(values)))

    @given(values=st.lists(st.integers()), capacity=st.integers(min_value=1))
    def test_m_concat(self, values: List[int], capacity: int) -> None:
        lst1: UnrolledLinkedList = UnrolledLinkedList()
        result: Optional[UnrolledLinkedList] = m_concat(lst1, None)
        self.assertEqual(to_list(result), [])
        lst2: UnrolledLinkedList = UnrolledLinkedList(capacity)
        result = m_concat(lst1, lst2)
        self.assertEqual(to_list(result), [])
        lst3: Optional[UnrolledLinkedList] = from_list(values, capacity)
        result = m_concat(lst1, lst3)
        self.assertEqual(to_list(result), values)

    @given(values=st.lists(st.integers()), capacity=st.integers(min_value=1))
    def test_monoid_identity(self, values: List[int], capacity: int) -> None:
        lst: Optional[UnrolledLinkedList] = from_list(values, capacity)
        self.assertEqual(m_concat(url_empty(), lst), lst)
        self.assertEqual(m_concat(lst, url_empty()), lst)

    @given(values=st.lists(st.integers()), capacity=st.integers(min_value=1))
    def test_iterator(self, values: List[int], capacity: int) -> None:
        lst: Optional[UnrolledLinkedList] = UnrolledLinkedList(capacity)
        result = iterator(lst)
        self.assertEqual(list(result), [])

        lst = from_list(values, capacity)
        temp: List[int] = []
        get_next = iterator(lst)
        try:
            while True:
                temp.append(next(get_next))
        except StopIteration:
            pass
        self.assertEqual(values, temp)
        self.assertEqual(to_list(lst), temp)

    @given(values=st.lists(st.integers()), capacity=st.integers(min_value=1))
    def test_url_filter(self, values: List[int], capacity: int) -> None:
        lst1: UnrolledLinkedList = UnrolledLinkedList()
        lst1 = url_filter(lst1, lambda x: x % 2 == 0)
        self.assertEqual(to_list(lst1), [])

        if values:
            lst2: Optional[UnrolledLinkedList] = from_list(values, capacity)
            lst2 = url_filter(lst2, lambda x: x % 2 == 0)
            filtered_values: List[int] = \
                [value for value in values if value % 2 == 0]
            self.assertEqual(to_list(lst2), filtered_values)

    @given(values=st.lists(st.integers()), capacity=st.integers(min_value=1))
    def test_map(self, values: List[int], capacity: int) -> None:
        lst1: UnrolledLinkedList = UnrolledLinkedList()
        lst1 = url_map(lst1, lambda x: x * 2)
        self.assertEqual(to_list(lst1), [])
        if values:
            lst2: Optional[UnrolledLinkedList] = from_list(values, capacity)
            lst2 = url_map(lst2, str)
            self.assertEqual(to_list(lst2), list(map(str, values)))
            lst3: Optional[UnrolledLinkedList] = from_list(values, capacity)
            lst3 = url_map(lst3, lambda x: x * 2)
            self.assertEqual(to_list(lst3), list(map(lambda x: x * 2, values)))

    @given(values=st.lists(st.integers()), capacity=st.integers(min_value=1))
    def test_reduce(self, values: List[int], capacity: int) -> None:
        lst1: UnrolledLinkedList = UnrolledLinkedList()
        self.assertEqual(None, reduce(lst1, lambda x, y: x + y, None))
        if values:
            lst2: Optional[UnrolledLinkedList] = from_list(values, capacity)
            self.assertEqual(reduce(lst2, lambda x, y: x + y, 0), sum(values))

    @given(values=st.lists(st.integers()), capacity=st.integers(min_value=1))
    def test_str(self, values: List[int], capacity: int) -> None:
        lst1: UnrolledLinkedList = UnrolledLinkedList()
        self.assertEqual(str(lst1), "")
        if values:
            lst2: Optional[UnrolledLinkedList] = from_list(values, capacity)
            self.assertEqual(str(lst2), "".join(map(str, values)))

    @given(st.integers(min_value=1))
    def test_api_with_None(self, capacity: int) -> None:
        empty: UnrolledLinkedList = url_empty()
        l1: UnrolledLinkedList = UnrolledLinkedList(1, cons(None, cons([1], None, 1), 1))
        l2: UnrolledLinkedList = UnrolledLinkedList(1, cons([1], cons(None, None, 1), 1))

        self.assertEqual(add_to_end(l1, None), from_list([None, 1, None], 1))

        self.assertEqual(str(empty), "")
        self.assertEqual(str(l1), "None1")
        self.assertEqual(str(l2), "1None")
        self.assertNotEqual(empty, l1)
        self.assertNotEqual(empty, l2)
        self.assertNotEqual(l1, l2)
        self.assertEqual(l1, UnrolledLinkedList(capacity, cons(None, cons([1], None, 1), 1)))

        self.assertEqual(size(empty), 0)
        self.assertEqual(size(l1), 1)
        self.assertEqual(size(l2), 1)

        self.assertEqual(str(remove(l1, 0)), "None1")
        self.assertEqual(str(remove(l1, 1)), "None")

        self.assertFalse(member(empty, None))
        self.assertTrue(member(l1, None))
        self.assertTrue(member(l1, 1))
        self.assertFalse(member(l1, 2))

        self.assertEqual(l1, reverse(l2))

        self.assertEqual(to_list(l1), [None, 1])
        self.assertNotEqual(l1, from_list([1], 1))

        self.assertEqual(m_concat(l1, l2), from_list([None, 1, 1, None], 1))

        buf = iterator(l1)
        self.assertEqual(list(buf), [None, 1])
        lst = to_list(l1) + to_list(l2)
        for e in to_list(l1):
            lst.remove(e)
        for e in to_list(l2):
            lst.remove(e)
        self.assertEqual(lst, [])

        self.assertEqual(find(l2, lambda x: x is None), None)

        self.assertEqual(to_list(url_set(l1, 1, None)), to_list(url_set(l2, 0, None)))

        self.assertEqual(url_set(l1, 1, None), url_set(l2, 0, None))

        with self.assertRaises(TypeError):
            reduce(l1, lambda x, y: x + y, None)

        self.assertEqual(to_list(url_filter(l1, lambda x: x is None)), [None])

        self.assertEqual(to_list(url_map(l1, lambda x: None)), [None, None])
