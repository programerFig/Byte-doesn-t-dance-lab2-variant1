from typing import Optional, List, Callable, Any


class UnrolledNode:
    def __init__(
        self,
        values: Optional[List[int]] = None,
        next_node=None,
        capacity: int = 1,
    ) -> None:
        if values is None:
            values = []
        self.values: List[int] = values
        self.next: UnrolledNode = next_node
        self.capacity: int = capacity

    def __eq__(self, other) -> bool:
        if other is None:
            return False
        if self.values != other.values:
            return False
        if self.capacity != other.capacity:
            return False
        return self.next == other.next


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
            result.append(":".join(map(str, current_node.values)))
            current_node = current_node.next
        return ":".join(result)


def url_empty() -> UnrolledLinkedList:
    return UnrolledLinkedList()


def cons(
    values: List[int], next_node: Optional[UnrolledNode], capacity: int
) -> UnrolledNode:
    return UnrolledNode(values, next_node, capacity)


def size(url: Optional[UnrolledLinkedList]) -> int:

    def _size_help(node: Optional[UnrolledNode]) -> int:
        if node is None:
            return 0
        return len(node.values) + _size_help(node.next)

    if url is None:
        return 0
    return _size_help(url.head)


def add(url: UnrolledLinkedList, element: int) -> UnrolledLinkedList:
    def _add_help(node: Optional[UnrolledNode]) -> Optional[UnrolledNode]:
        if node is None:
            return cons([element], None, url.node_capacity)
        if len(node.values) < node.capacity:
            return cons(node.values + [element], node.next, node.capacity)
        else:
            return cons(node.values, _add_help(node.next), node.capacity)

    return UnrolledLinkedList(url.node_capacity, _add_help(url.head))


def find(
    url: Optional[UnrolledLinkedList], predicate: Callable[[int], bool]
) -> Optional[int]:
    if url is None:
        return None
    current_node: Optional[UnrolledNode] = url.head
    while current_node:
        for value in current_node.values:
            if predicate(value):
                return value
        current_node = current_node.next
    return None


def member(url: Optional[UnrolledLinkedList], value: int) -> bool:
    if url is None:
        return False
    current_node: Optional[UnrolledNode] = url.head
    while current_node:
        if value in current_node.values:
            return True
        current_node = current_node.next
    return False


def url_set(
    url: Optional[UnrolledLinkedList], index: int, value: int
) -> UnrolledLinkedList:
    def _set_help(
        node: Optional[UnrolledNode], idx: int, val: int
    ) -> Optional[UnrolledNode]:
        if node is None:
            raise IndexError("Index out of range")
        if idx >= len(node.values):
            return cons(
                node.values,
                _set_help(node.next, idx - len(node.values), val),
                node.capacity,
            )
        new_values: List[int] = node.values[:]
        new_values[idx] = val
        return cons(new_values, node.next, node.capacity)

    if url is None:
        return UnrolledLinkedList()
    return UnrolledLinkedList(url.node_capacity,
                              _set_help(url.head, index, value))


def from_list(lst: List[int], capacity: int = 1) \
        -> Optional[UnrolledLinkedList]:
    if len(lst) == 0:
        return UnrolledLinkedList()

    def _from_list_help(lst2: List[int], capacity2: int) \
            -> Optional[UnrolledNode]:
        if len(lst2) == 0 or len(lst2) <= capacity2:
            return cons(lst2, None, capacity2)
        return cons(
            lst2[:capacity2],
            _from_list_help(lst2[capacity2:], capacity2), capacity2
        )

    return UnrolledLinkedList(capacity, _from_list_help(lst, capacity))


def to_list(url: Optional[UnrolledLinkedList]) -> List[int]:
    if url is None:
        return []
    result: List[int] = []

    def _to_list_help(current_node: Optional[UnrolledNode]) -> None:
        if current_node is None:
            return
        result.extend(current_node.values)
        _to_list_help(current_node.next)

    _to_list_help(url.head)
    return result


def remove(
    url: Optional[UnrolledLinkedList], element: int
) -> Optional[UnrolledLinkedList]:
    if url is None:
        return UnrolledLinkedList()
    if url.head is None:
        return url

    def _remove_help(node: UnrolledNode) -> Optional[UnrolledNode]:
        if node is None:
            return None
        new_values: List[int] = \
            [value for value in node.values if value != element]
        if not new_values:
            return _remove_help(node.next)
        return cons(new_values, _remove_help(node.next), node.capacity)

    return UnrolledLinkedList(url.node_capacity, _remove_help(url.head))


def reverse(url: Optional[UnrolledLinkedList]) -> UnrolledLinkedList:

    def _reverse_help(
        node: UnrolledNode, prev: Optional[UnrolledNode] = None
    ) -> UnrolledNode:
        if node is None:
            return prev
        new_node: UnrolledNode = (
            UnrolledNode(node.values[::-1], prev, node.capacity))
        return _reverse_help(node.next, new_node)

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
            if current_node.values:
                current_value: int = current_node.values[0]
                yield current_value
                current_node = cons(current_node.values[1:],
                                    current_node.next, current_node.capacity)
            else:
                current_node = current_node.next

    return _iterator_help()


def url_filter(
    url: Optional[UnrolledLinkedList], predicate: Callable[[int], bool]
) -> UnrolledLinkedList:
    if url is None:
        return UnrolledLinkedList()

    def _filter_help(node: Optional[UnrolledNode]) -> Optional[UnrolledNode]:
        if node is None:
            return None
        filtered_values: List[int] = [
            value for value in node.values if predicate(value)
        ]
        if not filtered_values:
            return _filter_help(node.next)
        return cons(filtered_values, _filter_help(node.next), node.capacity)

    return UnrolledLinkedList(url.node_capacity, _filter_help(url.head))


def url_map(
    url: Optional[UnrolledLinkedList], func: Callable[[int], Any]
) -> UnrolledLinkedList:
    if url is None:
        return UnrolledLinkedList()

    def _map_help(
        node: Optional[UnrolledNode], func2: Callable[[int], Any]
    ) -> Optional[UnrolledNode]:
        if node is None:
            return None
        mapped_values: List[int] = [func2(value) for value in node.values]
        return cons(mapped_values, _map_help(node.next, func2), node.capacity)

    return UnrolledLinkedList(url.node_capacity, _map_help(url.head, func))


def reduce(
    url: Optional[UnrolledLinkedList],
    func: Callable[[Any, int], Any],
    init: Any
) -> Any:
    if url is None:
        return None
    result: Any = init
    current_node: Optional[UnrolledNode] = url.head
    while current_node:
        for value in current_node.values:
            result = func(result, value)
        current_node = current_node.next
    return result
