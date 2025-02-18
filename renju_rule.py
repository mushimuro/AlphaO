import numpy as np

board = np.zeros((15, 15))


# board is (y,x)
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

# TODO : change return "checked" -> return True
def is_five(y, x, color):
    line = []

    # 가로줄 ; This removes edge cases
    if (x != 0 and board[y][max(0,x-1)] == color) or (x != 14 and board[y][min(14,x+1)] == color):
        for i in range(max(0, x-4), min(15, x+5), 1):
            line.append(board[y][i])
        # check for 5-win
        if check_list_five(color, line): return "checked"

    # 세로줄 (14,12)
    if (y != 0 and board[max(0, y - 1)][x] == color) or (y != 14 and board[min(14, y + 1)][x] == color):
        for i in range(max(0, y - 4), min(14, y + 5), 1):
            line.append(board[i][x])
        # check for 5-win
        if check_list_five(color, line): return "checked"

    # 좌측 상단 + 우측 하단 대각선
    if ((y != 0 or x!= 0) and board[max(0, y - 1)][max(0, x - 1)] == color) or ((y != 14 or x != 14) and board[min(14, y + 1)][min(14, x + 1)] == color):
        xrange = [max(0, x-4), min(15, x+5)]
        yrange = [max(0, y - 4), min(15, y + 5)]
    
        y_lower_range = yrange[0] - y    # negative val
        y_upper_range = yrange[-1] - y   # positive val
        x_lower_range = xrange[0] - x
        x_upper_range = xrange[-1] - x

        if y_lower_range < x_lower_range:
            lower_range = x_lower_range
        else:
            lower_range = y_lower_range

        if y_upper_range > x_upper_range:
            upper_range = x_upper_range
        else:
            upper_range = y_upper_range

        for i in range(lower_range , upper_range , 1):
            line.append(board[y+i][x+i])
        # check for 5-win
        if check_list_five(color, line): return "checked"

    # TODO
    # 좌측 하단 + 우측 상단
    # if...

    # if not 5 stone 
    # TODO : change to False
    return "Not is_five"

