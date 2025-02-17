import numpy as np

board = np.zeros((15, 15))

# TODO : swap y, x 

# color : black : 1 & white : -1 & default : 0
def is_valid(y, x):
    return board[y][x] == 0

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

def is_five(y, x, color):
    line = []

    # 가로줄 ; This removes edge cases
    if (x != 0 and board[y][max(0,x-1)] == color) or (x != 15 and board[y][min(15,x+1)] == color):
        for i in range(max(0, x-4), min(16, x+5), 1):
            line.append(board[y][i])
        # check for 5-win
        if check_list_five(color, line): return True

    # 세로줄
    if (y != 0 and board[max(0, y - 1)][x] == color) or (y != 15 and board[min(15, y + 1)][x] == color):
        for i in range(max(0, y - 4), min(16, y + 5), 1):
            line.append(board[i][x])
        # check for 5-win
        if check_list_five(color, line): return True

    # 좌측 상단 + 우측 하단 대각선
    if ((y != 0 or x!= 0) and board[max(0, y - 1)][max(0, x - 1)] == color) or ((y != 15 or x != 15) and board[min(15, y + 1)][min(15, x + 1)] == color):
        xrange = [max(0, x-4), min(16, x+5)]
        yrange = [max(0, y - 4), min(16, y + 5)]
    
        # use len of x,y range to determine which has shorter range -> use that range to create line
        if len(xrange) > len(yrange):
            lower_range = yrange[0] - y    # negative val
            upper_range = yrange[-1] - y   # positive val
        else:
            lower_range = xrange[0] - x
            upper_range = xrange[-1] - x

        for i in range(lower_range , upper_range , 1):
            line.append(board[y+i][x+i])
        # check for 5-win
        if check_list_five(color, line): return True


    # TODO
    # 좌측 하단 + 우측 상단