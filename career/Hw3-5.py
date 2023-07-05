# class Node:
#     def __init__(self, value, next=None):
#         self.value = value
#         self.next = next

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
    leng = 0
    if k == 0:
        return head
    if curr == None:
        return curr
    while curr.next != None:
        curr = curr.next
        leng += 1
    end = curr
    br = leng / k
    if br == 0:
        return head
    else:
        curr = head
        i = 0
        while i != br:
            i += 1
            prev, curr = curr, curr.next
        prev.next = None
        end.next = head
    