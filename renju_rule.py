from itertools import count

import numpy as np
from numpy.matlib import empty

board = np.zeros((15, 15), dtype=int)
ban = []
list_dx = [-1, 1, -1, 1, 0, 0, 1, -1]
list_dy = [0, 0, -1, 1, -1, 1, -1, 1]




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
            return "overline"
            # return True

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


def find_prohibit_point(y, x):
    cnt = 0
    empty = 0

    # list_dx = [-1, 1, -1, 1, 0, 0, 1, -1]
    # list_dy = [0, 0, -1, 1, -1, 1, -1, 1]

    for j in range(4):
        for i in range(2):
            cur_y, cur_x = y, x
            while True:

                if empty == 2:
                    break

                # Empty
                if board[cur_y][cur_x] == 0:
                    empty += 1
                    if is_samsam(cur_y, cur_x) or is_double_four(cur_y, cur_x) or is_overline(cur_y,cur_x):
                        ban.append({cur_y, cur_x})
                # Black
                elif board[cur_y][cur_x] == 1:
                    cnt += 1
                # White
                elif board[cur_y][cur_x] == -1:
                    break

                cur_y, cur_x = y + list_dy[j * 2 + i], x + list_dx[j * 2 + i]


def check_prohibit_point(ban):
    if len(ban) == 0: return

    for i in ban:
        y, x = i
        if is_samsam(y, x) or is_double_four(y, x) or is_overline(y, x):
            ban.remove(i)


def is_double_four(y, x):
    four_cnt = 0

    # list_dx = [-1, 1, -1, 1, 0, 0, 1, -1]
    # list_dy = [0, 0, -1, 1, -1, 1, -1, 1]


    for j in range(4):
        for i in range(2):
            check_board = board.copy()
            check_board[y][x] = 1
            empty_cnt = 0
            cur_y, cur_x = y, x
            if open_four(cur_y, cur_x) == 2: return True
            while True:
                if empty_cnt == 2 or check_board[cur_y][cur_x] == -1:
                    break
                elif check_board[cur_y][cur_x] == 0:
                    empty_cnt += 1
                    check_board[cur_y][cur_x] = 1

                    cnt = 0
                    for k in range(2):
                        while True:
                            if check_board[cur_y][cur_x] == -1 or check_board[cur_y][cur_x] == 0:
                                break
                            else:
                                cnt += 1
                            cur_y, cur_x = y + list_dy[j * 2 + k], x + list_dx[j * 2 + k]
                    if cnt == 5:
                        four_cnt += 1
                        if four_cnt == 2 : return True
                        break

                cur_y, cur_x = y + list_dy[j * 2 + i], x + list_dx[j * 2 + i]

            return False



def is_overline(y,x):
    # list_dx = [-1, 1, -1, 1, 0, 0, 1, -1]
    # list_dy = [0, 0, -1, 1, -1, 1, -1, 1]

    for j in range(4):
        line = [1]
        for i in range(2):
            cur_y, cur_x = y, x
            while True:
                if board[cur_y][cur_x] == 0 or board[cur_y][cur_x] == -1:
                    break
                else:
                    if i == 0:
                        line.append(board[cur_y][cur_x])
                    else:
                        line.insert(0, board[cur_y][cur_x])
                cur_y, cur_x = y + list_dy[j * 2 + i], x + list_dx[j * 2 + i]

        if check_list(1, line) == "overline":
            return True

    return False

