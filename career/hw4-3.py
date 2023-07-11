def drown(board):
    board = board.copy()

    if not board:
        return None
    
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 'O':
                # bfs
                to_drown = 1 # by default we drown
                k = 0
                stack = [[i, j]]
                while len(stack) > k:
                    x, y = stack[k][0], stack[k][1]
                    board[x][y] = 'I' # temp paint
                    # look up
                    if x - 1 < 0:
                        to_drown = 0
                    elif board[x - 1][y] == 'O':
                        stack.append([x-1, y])
                    # look down
                    if x + 1 > len(board) - 1:
                        to_drown = 0
                    elif board[x + 1][y] == 'O':
                        stack.append([x + 1, y])
                    # look left
                    if y - 1 < 0:
                        to_drown = 0
                    elif board[x][y - 1] == 'O':
                        stack.append([x, y - 1])
                    # look right
                    if y + 1 > len(board[0]) - 1:
                        to_drown = 0
                    elif board[x][y + 1] == 'O':
                        stack.append([x, y + 1])              

                    k += 1
                # drown
                if to_drown:
                    for a, b in stack:
                        board[a][b] = 'X'
                else:
                    for a, b in stack:
                        board[a][b] = 'O'

    return board





# array = [
#     ['X', 'X', 'X', 'X', 'X'],
#     ['X', 'O', 'O', 'O', 'X'],
#     ['O', 'X', 'X', 'O', 'X']
# ]

# print(drown(array))