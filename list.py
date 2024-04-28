from typing import Optional, List, Callable, Any


class UnrolledNode:
    def __init__(
        self,
        values: Optional[List[Any]] = None,
        next_node=None,
        capacity: Optional[int] = 1,
    ) -> None:
        self.values: Optional[List[Any]] = values
        self.next: UnrolledNode = next_node
        if capacity:
            self.capacity: int = capacity
        else:
            self.capacity = 1

    def __eq__(self, other) -> bool:
        if self is None and other is None:
            return True
        elif self is not None and other is not None:
            if self.values != other.values:
                return False
            if self.capacity != other.capacity:
                return False
            return self.next == other.next
        else:
            return False

    def __str__(self) -> str:
        if self.values:
            return ":".join(str(value) for value in self.values)
        return "None"


class UnrolledLinkedList:
    def __init__(
        self, node_capacity: int = 1, head: Optional[UnrolledNode] = None
    ) -> None:
        self.node_capacity: int = node_capacity
        self.head: Optional[UnrolledNode] = head

    def __eq__(self, other) -> bool:
        if not isinstance(other, UnrolledLinkedList):
            return False
        return self.head == other.head

    def __str__(self) -> str:
        result: List[str] = []
        current_node: Optional[UnrolledNode] = self.head
        while current_node:
            if current_node.values:
                result.append("".join(map(str, current_node.values)))
            else:
                result.append("None")
            current_node = current_node.next
        return "".join(result)


def url_empty() -> UnrolledLinkedList:
    return UnrolledLinkedList()


def cons(
    values: Optional[List[Any]], next_node: Optional[UnrolledNode], capacity: Optional[Any] = 1
) -> UnrolledNode:
    return UnrolledNode(values, next_node, capacity)


def size(url: Optional[UnrolledLinkedList]) -> int:

    def _size_help(node: Optional[UnrolledNode]) -> int:
        if node is None:
            return 0
        if node.values:
            return len(node.values) + _size_help(node.next)
        else:
            return _size_help(node.next)

    if url is None:
        return 0
    return _size_help(url.head)


def add(url: UnrolledLinkedList, element: Any) -> UnrolledLinkedList:
    def _add_help(node: Optional[UnrolledNode]) -> Optional[UnrolledNode]:
        if node is None:
            return cons([element], None, url.node_capacity)
        if node.values is not None:
            if len(node.values) < node.capacity:
                return cons(node.values + [element], node.next, node.capacity)
            else:
                return cons(node.values, _add_help(node.next), node.capacity)
        else:
            return cons(None, _add_help(node.next), node.capacity)

    return UnrolledLinkedList(url.node_capacity, _add_help(url.head))


def add_to_end(url: UnrolledLinkedList, element: Any) -> UnrolledLinkedList:
    def _add_to_end_help(node: Optional[UnrolledNode]) -> Optional[UnrolledNode]:
        if node is None:
            return cons([element], None, url.node_capacity)
        if node.next is None:
            if node.values is None:
                return cons(None, None, node.capacity)
            else:
                if len(node.values) < node.capacity:
                    if element is not None:
                        return cons(node.values + [element], None, node.capacity)
                    else:
                        return cons(node.values, cons(None, None, node.capacity), node.capacity)
                else:
                    return cons(node.values, cons(None, None, node.capacity), node.capacity)
        return cons(node.values, _add_to_end_help(node.next), node.capacity)
    return UnrolledLinkedList(url.node_capacity, _add_to_end_help(url.head))


def find(
    url: Optional[UnrolledLinkedList], predicate: Callable[[Any], bool]
) -> Optional[Any]:
    if url is None:
        return None
    current_node: Optional[UnrolledNode] = url.head
    while current_node:
        if current_node.values is None:
            if predicate(None):
                return None
        else:
            for value in current_node.values:
                if predicate(value):
                    return value
        current_node = current_node.next
    return None


def member(url: Optional[UnrolledLinkedList], value: Optional[Any]) -> bool:
    if url is None:
        return False
    current_node: Optional[UnrolledNode] = url.head
    while current_node:
        if current_node.values:
            if value:
                if value in current_node.values:
                    return True
        else:
            if not value:
                return True
        current_node = current_node.next
    return False


def url_set(
    url: Optional[UnrolledLinkedList], index: int, value: Any
) -> UnrolledLinkedList:
    def _set_help(
        node: Optional[UnrolledNode], idx: int, val: Any
    ) -> Optional[UnrolledNode]:
        if node is None:
            raise IndexError("Index out of range")
        if node.values is None:
            if idx > 0:
                return cons(None, _set_help(node.next, idx - 1, val), node.capacity)
            else:
                return cons(val, node.next, node.capacity)
        if idx >= len(node.values):
            return cons(node.values, _set_help(node.next, idx - len(node.values), val), node.capacity)
        if node.values is None:
            return cons([val], node.next, node.capacity)
        else:
            if val is None and node.capacity == 1:
                return cons(None, node.next, node.capacity)
            else:
                new_values: List[Any] = node.values[:]
                new_values[idx] = val
                return cons(new_values, node.next, node.capacity)
    if url is None:
        return UnrolledLinkedList()
    return UnrolledLinkedList(url.node_capacity, _set_help(url.head, index, value))


def from_list(lst: List[Any], capacity: Optional[int] = 1) \
        -> Optional[UnrolledLinkedList]:
    if len(lst) == 0:
        return UnrolledLinkedList()

    def _from_list_help(lst2: List[Any], capacity2: Optional[int] = 1) \
            -> Optional[UnrolledNode]:
        if capacity2 is None:
            capacity2 = 1
        if len(lst2) == 0 or len(lst2) <= capacity2:
            if lst2[0] is None and capacity == 1:
                return cons(None, None, capacity2)
            return cons(lst2, None, capacity2)
        if lst2[0] is None:
            return cons(None, _from_list_help(lst2[capacity2:], capacity2), capacity2)

        return cons(lst2[:capacity2], _from_list_help(lst2[capacity2:], capacity2), capacity2)
    if capacity is None:
        capacity = 1
    return UnrolledLinkedList(capacity, _from_list_help(lst, capacity))


def to_list(url: Optional[UnrolledLinkedList]) -> List[Any]:
    if url is None:
        return []
    result: List[Any] = []

    def _to_list_help(current_node: Optional[UnrolledNode]) -> None:
        if current_node is None:
            return
        if current_node.values:
            result.extend(current_node.values)
        else:
            result.append(None)
        _to_list_help(current_node.next)

    _to_list_help(url.head)
    return result


def remove(
    url: Optional[UnrolledLinkedList], element: Any
) -> Optional[UnrolledLinkedList]:
    if url is None:
        return UnrolledLinkedList()
    if url.head is None:
        return url

    def _remove_help(node: UnrolledNode) -> Optional[UnrolledNode]:
        if node is None:
            return None
        if node.values:
            new_values: List[Any] = [value for value in node.values if value != element]
            if not new_values:
                return _remove_help(node.next)
            return cons(new_values, _remove_help(node.next), node.capacity)
        else:
            return cons(None, _remove_help(node.next), node.capacity)
    return UnrolledLinkedList(url.node_capacity, _remove_help(url.head))


def reverse(url: Optional[UnrolledLinkedList]) -> UnrolledLinkedList:

    def _reverse_help(
        node: UnrolledNode, prev: Optional[UnrolledNode] = None
    ) -> UnrolledNode:
        if node is None:
            return prev
        if node.values:
            return _reverse_help(node.next, UnrolledNode(node.values[::-1], prev, node.capacity))
        else:
            return _reverse_help(node.next, UnrolledNode(None, prev, node.capacity))

    if url is None:
        return UnrolledLinkedList()
    if url.head is None:
        return url
    return UnrolledLinkedList(url.node_capacity, _reverse_help(url.head))


def m_concat(
    url1: Optional[UnrolledLinkedList], url2: Optional[UnrolledLinkedList]
) -> Optional[UnrolledLinkedList]:

    def _reverse_node(
        node: Optional[UnrolledNode], prev: Optional[UnrolledNode] = None
    ) -> Optional[UnrolledNode]:
        if node is None:
            return prev
        new_node: UnrolledNode = UnrolledNode(node.values, prev, node.capacity)
        return _reverse_node(node.next, new_node)

    def _m_concat_help(
        node1: Optional[UnrolledNode], node2: Optional[UnrolledNode]
    ) -> Optional[UnrolledNode]:
        if node1 is None:
            return node2
        return _m_concat_help(node1.next,
                              cons(node1.values, node2, node1.capacity))

    if url1 is None:
        return url2
    if url2 is None:
        return url1
    capacity: int = max(url1.node_capacity, url2.node_capacity)
    return UnrolledLinkedList(
        capacity, _m_concat_help(_reverse_node(url1.head), url2.head)
    )


def iterator(lst: Optional[UnrolledLinkedList]):
    if lst is None:
        return
    current_node: Optional[UnrolledNode] = lst.head

    def _iterator_help():
        nonlocal current_node
        while current_node:
            if current_node.values is None:
                yield None
                current_node = current_node.next
            if current_node.values:
                current_value: Any = current_node.values[0]
                yield current_value
                current_node = cons(current_node.values[1:],
                                    current_node.next, current_node.capacity)
            else:
                current_node = current_node.next
    return _iterator_help()


def url_filter(
    url: Optional[UnrolledLinkedList], predicate: Callable[[Any], bool]
) -> UnrolledLinkedList:
    if url is None:
        return UnrolledLinkedList()

    def _filter_help(node: Optional[UnrolledNode]) -> Optional[UnrolledNode]:
        if node is None:
            return None
        if node.values is not None:
            filtered_values: List[Any] = [value for value in node.values if predicate(value)]
            if not filtered_values:
                return _filter_help(node.next)
            return cons(filtered_values, _filter_help(node.next), node.capacity)
        else:
            if predicate(None):
                return cons([], _filter_help(node.next), node.capacity)
            else:
                return cons(None, _filter_help(node.next), node.capacity)
    return UnrolledLinkedList(url.node_capacity, _filter_help(url.head))


def url_map(
    url: Optional[UnrolledLinkedList], func: Callable[[Any], Any]
) -> UnrolledLinkedList:
    if url is None:
        return UnrolledLinkedList()

    def _map_help(
        node: Optional[UnrolledNode], func2: Callable[[Any], Any]
    ) -> Optional[UnrolledNode]:
        if node is None:
            return None
        if node.values is None:
            return cons(func2(None), _map_help(node.next, func2), node.capacity)
        else:
            mapped_values: List[Any] = [func2(value) for value in node.values]
            return cons(mapped_values, _map_help(node.next, func2), node.capacity)
    return UnrolledLinkedList(url.node_capacity, _map_help(url.head, func))


def reduce(
    url: Optional[UnrolledLinkedList],
    func: Callable[[Any, Any], Any],
    init: Any
) -> Any:
    if url is None:
        return None
    if Any is None:
        raise TypeError("Expected an integer value")
    result: Any = init
    current_node: Optional[UnrolledNode] = url.head
    while current_node:
        if current_node.values is not None:
            for value in current_node.values:
                result = func(result, value)
        current_node = current_node.next
    return result
