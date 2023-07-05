def maj_element(nums):
    dict = {}
    for num in nums:
        dict.setdefault(num, 0)
        dict[num] += 1
    max_el = 0
    maj = None
    for key in dict:
        if dict[key] > max_el:
            max_el = dict[key]
            maj = key
    return maj

# nums = [3, 5, 5, 1]

# print(maj_element(nums))