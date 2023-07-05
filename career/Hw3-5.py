# class Node:
#     def __init__(self, value, next=None):
#         self.value = value
#         self.next = next

#     def __repr__(self):
#         return self.value

# class LinkedList:
#     def __init__(self):
#         self.head = None

#     def __repr__(self):
#         node = self.head
#         nodes = []
#         while node is not None:
#             nodes.append(node.value)
#             node = node.next
#         nodes.append(None)
#         return " -> ".join(map(str, nodes))



# Terrible solution of O(n^k)

# def rotate_right(head, k):
#     curr = head
#     if head == None or head.next == None:
#         return head
#     for i in range(k):
#         first = curr
#         while curr.next != None:
#             prev, curr = curr, curr.next
#         curr.next = first
#         prev.next = None
#     return curr

# Good solution

def rotate_right(head, k):
    curr = head
    
    if k == 0:
        return head
    if head == None:
        return head
    leng = 1
    while curr.next != None:
        curr = curr.next
        leng += 1
    end = curr
    br = k % leng
    if br == 0:
        return head
    else:
        curr = head
        i = 0
        while i != leng - br:
            i += 1
            prev, curr = curr, curr.next
        prev.next = None
        end.next = head
    return curr


# first_node = Node("a")
# second_node = Node('b')
# first_node.next = second_node
# third_node = Node('c')
# second_node.next = third_node
# fourth_node = Node('d')
# third_node.next = fourth_node
# fifth_node = Node('e')
# fourth_node.next = fifth_node

# new_node = rotate_right(first_node, 6)

# ls = LinkedList()
# ls.head = new_node
# print(ls)


