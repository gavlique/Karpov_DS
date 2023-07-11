# class Node:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

def are_trees_equal(head_1, head_2):
    if head_1 is None and head_2 is None:
        return True
    if head_1.val != head_2.val:
        return False
    else:
        return are_trees_equal(head_1.left, head_2.left) and are_trees_equal(head_1.right, head_2.right)

# Tree 1
#  1
# 2 3

# left_1 = Node(2)
# right_1 = Node(3)
# head_1 = Node(1, left_1, right_1)

# # Tree 2
# #  1
# # 3 2

# left_2 = Node(3)
# right_2 = Node(2)
# head_2 = Node(1, left_2, right_2)

# print(are_trees_equal(head_1, head_2))