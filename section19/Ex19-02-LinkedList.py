"""
파일명: Ex19-02-LinkedList.py

연결 리스트(Linked List)
    저장된 각 데이터가 (데이터)+(다음 데이터의 포인터)로 이루어진 것으로
    한 방향으로만 탐색 가능한 구조
"""

class Node:

    def __init__(self, data, next=None):
        self.data = data
        self.next = next


class LinkedList:

    def __init__(self):
        self.head = None

    def add_node(self, data):
        """
        7 3 9 1 6
        add_node(7)
        data = 7
        new_node = Node(7)

        add_node(3)
        data = 3
        new_node = Node(3)
        current = Node(7)

        add_node(9)
        data = 9
        new_node = Node(9)
        current = Node(7)

        """

        new_node = Node(data)   # 새로운 노드 생성

        if self.head is None:
            self.head = new_node
            return

        current = self.head

        while current.next is not None:
            current = current.next

        current.next = new_node

    def insert_node(self, find_data, insert_data):
        if self.head is None:
            return
        """
        [7 3 9 1 6]
        insert_node(9, 99)
        find_data = 9
        insert_data = 99
        
        head.data(7) == find_data(9)
        current = Node(7)
        next.data(3) == find_data(9)
        next.data(9) == find_data(9)
        """
        if self.head.data == find_data:
            self.head = Node(insert_data, self.head)

        current = self.head
        while current.next is not None:
            if current.next.data == find_data:
                new_node = Node(insert_data, current.next)
                current.next = new_node
                return
            current = current.next

        self.add_node(insert_data)


    def delete_node(self, del_data):
        if self.head is None:
            return

        """
        delete_node(1)
        del_data = 1
        
        
        """

        if self.head.data == del_data:
            self.head = self.head.next
            return

        current = self.head

        while current.next is not None:
            if current.next.data == del_data:
                current.next = current.next.next
                return
            current = current.next


    def print_list(self):
        current = self.head
        while current is not None:
            print(current.data, end=' ')
            current = current.next


# 실행코드
linked_list = LinkedList()
linked_list.add_node(7)
linked_list.add_node(3)
linked_list.add_node(9)
linked_list.add_node(1)
linked_list.add_node(6)

linked_list.insert_node(9, 99)

linked_list.delete_node(1)

linked_list.print_list()


