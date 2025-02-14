import numpy as np

board = np.zeros((15, 15))

# color : black : 1 & white : -1 & default : 0
def is_valid(x, y):
    return board[x][y] == 0

def check_list_five(color, line):
    maxN = 0
    count = 0
    for i in range(len(line)):
        # check white is 5
        if color == -1 and count == 5:
            return True

        if line[i] == color:
            count += 1
            maxN = max(maxN, count)
        else:
            count = 0

    if maxN == 5:
        return True

    return False

def is_five(x, y, color):
    line = []

    # 가로줄
    if board[max(0,x-1)][y] == color or board[min(15,x+1)][y] == color:
        # edge case -> pass
        if x == 0 or x == 15:
            pass
        # non-edge cases
        else:
            for i in range(max(0, x-4), min(16, x+5), 1):
                line.append(board[i][y])
            # check for 5-win
            if check_list_five(color, line): return True

    # 세로줄
    elif board[x][max(0, y - 1)] == color or board[x][min(15, y + 1)] == color:
        # edge case -> pass
        if y == 0 or y == 15:
            pass
        # non-edge cases
        else:
            for i in range(max(0, y - 4), min(16, y + 5), 1):
                line.append(board[x][i])
            # check for 5-win
            if check_list_five(color, line): return True

    # 세로줄

    # 오른 대각선
    elif board[max(0, x - 1)][max(0, y - 1)] == color or board[min(15, x + 1)][min(15, y + 1)] == color:
        # edge case -> pass
        if x == 0 or x == 15 or y == 0 or y == 15:
            pass
        # non-edge cases
        else:
            xrange = [max(0, x-4), min(16, x+5)]
            yrange = [max(0, y - 4), min(16, y + 5)]
            mixrange = [min(xrange[0], yrange[0]), min(xrange[0], yrange[0])]

            for i in range (mixrange[0], mixrange[1], 1):
                line.append(board[][])
            # if y - 4 < 0:
            #     for i in range(0, y + 5, 1):
            #         line.append(board[x + i][i])
            #     # 불편 = 편안 (?)
            # elif y + 4 > 15:
            #     for i in range(y - 4, 16, 1):
            #         line.append(board[x][i])
            #     # 불편 = 편안 (?)
            # else:
            #     if board[x][y - 1] == color or board[x][y + 1] == color:
            #         for i in range(-4, 5, 1):
            #             line.append(board[x][y + i])
                # 불편 = 편안 (?)
            # check for 5-win
            if check_list_five(color, line): return True

    # 대각선 * 2