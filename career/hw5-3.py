def last_stone(stones: list):
    if len(stones) <= 1:
        return stones
    stones.sort(reverse=True)
    last = stones[0]
    for i in range(1, len(stones)):
        if last > 0:
            last -= stones[i]
        else:
            last += stones[i]
    return last

# arr = [10, 3, 1, 2]
# print(last_stone(arr))
