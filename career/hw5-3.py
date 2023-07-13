import random

def sort_array(nums):
    
    def quicksort(nums, lo, hi):
        if lo < hi:
            partition_resting_point = partition(nums, lo, hi)
            quicksort(nums, lo, partition_resting_point - 1)
            quicksort(nums, partition_resting_point + 1, hi)
        
    def partition(nums, lo, hi):
        pivotIdx = random.randint(lo, hi)
        nums[pivotIdx], nums[hi] = nums[hi], nums[pivotIdx]
        pivot = nums[hi]
        
        l_idx = lo
        r_idx = hi-1
        while l_idx <= r_idx:
            if nums[l_idx] <= pivot:
                l_idx+=1
            elif nums[r_idx] >= pivot:
                r_idx-=1
            else:
                nums[l_idx], nums[r_idx] = nums[r_idx], nums[l_idx]
                l_idx+=1
                r_idx-=1
        
        nums[l_idx], nums[hi] = nums[hi], nums[l_idx]
        return l_idx
    
    quicksort(nums, 0, len(nums)-1)
    return nums

def kth_largest(array, k):
    return sort_array(array)[-k]