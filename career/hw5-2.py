def min_path(grid):
    arr = [[None for i in range(len(grid[0]))] for j in range(len(grid))]
    arr[0][0] = grid[0][0]
    
    def get_min(arr, i, j):
        if arr[i][j] is not None:
            return arr[i][j]
        else:
            if i == 0:
                arr[i][j] = get_min(arr, i, j - 1) + grid[i][j]
                return arr[i][j]
            elif j == 0:
                arr[i][j] = get_min(arr, i - 1, j) + grid[i][j]
                return arr[i][j]
            else:
                arr[i][j] = min(get_min(arr, i - 1, j), get_min(arr, i, j - 1)) + grid[i][j]
                return arr[i][j]
    
    return get_min(arr, len(grid) - 1, len(grid[0]) - 1)




# grid = [[1, 3, 1], [1, 5, 1], [4, 2, 1]]

# print(min_path(grid))