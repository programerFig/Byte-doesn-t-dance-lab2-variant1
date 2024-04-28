# Byte Doesn't Dance - lab 2 - variant 1

## Unrolled Linked List

- The Unrolled Linked List is a variant of the traditional linked list
  data structure. Unlike the singly linked list, the unrolled linked
  list stores multiple elements in each node, which helps reduce memory
  overhead and improve cache performance.

### Mutable vs Immutable

- The Unrolled Linked List implementation includes both mutable and
  immutable variants. This project focuses on the immutable variant.
- Mutable: You can modify the contents of nodes directly, allowing
  for in-place updates. This flexibility can be useful for scenarios
  where frequent modifications are required.
- Immutable: The immutable variant ensures that once a node is
  created, its contents cannot be changed. Instead, operations like
  adding, removing, or modifying elements result in the creation of
  new nodes. The cons function plays a crucial role in immutable lists
  by creating new nodes and connecting them together. This function
  serves as the foundation for building new linked lists.

## Features

- Efficiency: Storing multiple elements in a single node reduces memory
  fragmentation and improves cache utilization.
- Common Operations: Supports typical linked list operations such as
  adding, getting, setting, and removing elements.
- Advanced Operations: Provides advanced operations like inversion,
  filtering, mapping, and reduction.

## Project structure

- `list.py` -- implementation of `UnrolledNode` class and
  `UnrolledLinkedList` class with multiple functions, including adding,
  getting, setting, and removing elements, as well as other advanced
  operations
- `list_test.py` -- unit and PBT tests for `unrolled linked list`.

## Contribution

- `Hu Jinghao` (1206041060@qq.com)
  all work
- `Meng Chenxu` (3183093110@qq.com)
  all work

## Changelog

- 28.04.2024 - 4
  Add the test when there are None elements in the data structure,
  i.e., test_api. Add the comparison between immutable and mutable
  to readme.
- 25.04.2024 - 3
  Add type annotations.
- 24.04.2024 - 2
  Add test coverage.
- 23.04.2024 - 1
  Update README. Add formal sections.
- 22.04.2024 - 0
  Initial

## Design notes

- Compared with traditional singly linked lists, unrolled linked
  lists store multiple elements in one node instead of one element
  corresponding to one node. This allows us to focus on storing
  multiple elements in a single node to reduce memory overhead and
  improve cache hits. It has advantages of efficiency. When the
  number of elements is large, unrolled linked list can improve
  memory utilization and access efficiency.
