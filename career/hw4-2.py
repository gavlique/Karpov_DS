# class Node:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

def invert_tree(head):
    if head == None:
        return head
    else:
        head.left, head.right = invert_tree(head.right), invert_tree(head.left)
        return head


# Tree
#    1
#  2   3
# 4 5 6 7


# left_left = Node(4)
# left_right = Node(5)
# right_left = Node(6)
# right_right = Node(7)
# left = Node(2, left_left, left_right)
# right = Node(3, right_left, right_right)
# head = Node(1, left, right)

# invert_tree(head)