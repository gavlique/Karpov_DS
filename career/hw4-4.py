class Node:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def kth_smallest(head, k):
    ls = []

    def inorder(head):
        if head is not None:
            inorder(head.left)
            ls.append(head.val)
            inorder(head.right)
        return ls

    result = inorder(head)

    return result[k-1]


head = Node(5)
left = Node(3)
head.left = left
right = Node(6)
head.right = right
left_left = Node(2)
left.left = left_left
left_right = Node(4)
left.right = left_right
left_left_left = Node(1)
left_left.left = left_left_left

kth_smallest(head, 3)

