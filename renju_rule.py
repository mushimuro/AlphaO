import numpy as np

board = np.zeros((15, 15), dtype=int)


# board is (y,x)
# color : black : 1 & white : -1 & default : 0
def is_valid(y, x):
    return board[y][x] == 0

def check_list(color, line):
    maxN = 0
    count = 0
    for i in range(len(line)):
        # check white is 5 (white can have 5+ in a row)
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


def pre_check(y, x, color):
    line = []

    # 가로줄 ; This removes edge cases
    if (board[y][max(0,x-1)] == color) or (board[y][min(14,x+1)] == color):
        # normal case or edge cases
        if ((x != 14 and x != 0) or (x == 14 and board[y][x-1] == color) or (x == 0 and board[y][x+1] == color)):
            for i in range(max(0, x-5), min(15, x+6), 1):
                line.append(board[y][i])
            # check for 5-win
            if check_list(color, line): return "checked"   # TODO : change return "checked" -> return True

    # 세로줄 (14,12)
    if (board[max(0, y - 1)][x] == color) or (board[min(14, y + 1)][x] == color):
        if ((y != 14 and y != 0) or (y == 14 and board[y-1][x] == color) or (y == 0 and board[y+1][x] == color)):
            for i in range(max(0, y - 5), min(15, y + 6), 1):
                line.append(board[i][x])
            # check for 5-win
            if check_list(color, line): return "checked"   # TODO : change return "checked" -> return True

    # 좌측 상단 + 우측 하단 대각선
    if (board[max(0, y - 1)][max(0, x - 1)] == color) or (board[min(14, y + 1)][min(14, x + 1)] == color):
        if ((y != 14 and y != 0 and x != 14 and x != 0) or ((y == 0 or x == 0) and board[y+1][x+1] == color) or ((y == 14 or x == 14) and board[y-1][x-1] == color)):
            xrange = [max(0, x-5), min(15, x+6)]
            yrange = [max(0, y - 5), min(15, y + 6)]
        
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
            if check_list(color, line): return "checked"   # TODO : change return "checked" -> return True

    # 좌측 하단 + 우측 상단
    if (board[min(14, y + 1)][max(0, x - 1)] == color) or (board[max(0, y - 1)][min(14, x + 1)] == color):
        if ((y != 14 and y != 0 and x != 14 and x != 0) or ((y == 14 or x == 0) and board[y-1][x+1]) or ((y == 0 or x == 14) and board[y+1][x-1])):
            xrange = [max(0, x-5), min(15, x+6)]
            yrange = [max(0, y - 5), min(15, y + 6)]
        
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
                line.append(board[y+i][x-i])
            # check for 5-win
            if check_list(color, line): return "checked"   # TODO : change return "checked" -> return True


    # if not 5 stone 
    return "Not is_five"   # TODO : change to False

