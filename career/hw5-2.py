import heapq

def last_stone(stones):
    while len(stones) > 1:
        heapq._heapify_max(stones)
        first = stones.pop(0)
        heapq._heapify_max(stones)
        second = stones.pop(0)
        diff = first - second
        if diff == 0:
            pass
        else:
            stones.append(diff)
    return 0 if len(stones) == 0 else stones[0]

# print(last_stone([2,3,4,5,6]))