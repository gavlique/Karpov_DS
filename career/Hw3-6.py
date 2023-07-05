def color_sort(nums):
    zero = 0
    one = 0
    two = len(nums) - 1
    while one <= two:
        if nums[one] == 0:
            nums[one], nums[zero] = nums[zero], nums[one]
            one += 1
            zero += 1
        elif nums[one] == 1:
            one += 1
        else:
            nums[one], nums[two] = nums[two], nums[one]
            two -= 1
    return nums
# nums = [2, 1, 1, 0, 0, 2, 2]

# print(color_sort(nums))
