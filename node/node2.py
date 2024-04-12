class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        
class DoublyLinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            return
        last_node = self.head
        while last_node.next:
            last_node = last_node.next
        last_node.next = new_node
        new_node.prev = last_node

    def print_list(self):
        current_node = self.head
        while current_node:
            print(current_node.data, end=" <-> ")
            current_node = current_node.next
        print("None")

    def delete_node(self, key):
        current_node = self.head
        while current_node:
            if current_node.data == key:
                if current_node.prev is None:
                    self.head = current_node.next
                    if current_node.next:
                        current_node.next.prev = None
                else:
                    current_node.prev.next = current_node.next
                    if current_node.next:
                        current_node.next.prev = current_node.prev
                return
            current_node = current_node.next

    def edit_node(self, key, new_data):
        current_node = self.head
        while current_node:
            if current_node.data == key:
                current_node.data = new_data
                return
            current_node = current_node.next

    def traverse(self):
        current_node = self.head
        while current_node:
            print(current_node.data, end=" <-> ")
            current_node = current_node.next
        print("None")


# Пример использования
dllist = DoublyLinkedList()
dllist.append(1)
dllist.append(2)
dllist.append(3)
dllist.traverse()
dllist.delete_node(2)
dllist.traverse()
dllist.edit_node(3, 4)
dllist.traverse()
