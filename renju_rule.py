from itertools import count

import numpy as np
from numpy.matlib import empty

board = np.zeros((15, 15), dtype=int)
ban = []
list_dx = [-1, 1, -1, 1, 0, 0, 1, -1]
list_dy = [0, 0, -1, 1, -1, 1, -1, 1]



# TODO: check if "self".board[][] needs to be applied to all methods

# check if the spot is placeable(empty stone)
def is_placeable(self, y, x):
    if self.board[y][x] == 0:
        return True
    return False


# board is (y,x)
# color : black : 1 & white : -1 & default : 0
def is_valid(y, x):
    return board[y][x] == 0

# 승리 및 장목 확인
# TODO : 장목 되었을때 아예 못두도록 하도록 바꾸기; 현재는 그냥 win-case가 아니도록만 설정해둠
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


# TODO 한줄에 4-4 나오는거 추가
def is_double_four(y, x):
    four_cnt = 0
    # 양쪽 공백 나올때까지 저장(공백도 같이 저장)
    for j in range(4):
        # if open_four(y,x) == 2: return True
        line = [1]
        center = 0
        for i in range(2):
            empty_cnt = 0
            cur_y, cur_x = y, x
            while True:
                if board[cur_y][cur_x] == 0:
                    empty_cnt += 1
                elif empty_cnt == 2 or board[cur_y][cur_x] == -1:
                    break

                if i == 0:
                    line.append(board[cur_y][cur_x])
                else:
                    line.insert(0, board[cur_y][cur_x])
                    center += 1

                cur_y, cur_x = y + list_dy[j * 2 + i], x + list_dx[j * 2 + i]

        # 오목되는지 체크
        if make_five_row(line):
            four_cnt += 1
            if four_cnt >= 2: return True
    return False


def make_five_row(line):
    for i in range(len(line)):
        if line[i] == 0:
            line[i] = 1
            count = 0
            for stone in line:
                if stone == 1:
                    count += 1
                    if count == 5:
                        return True
                else:
                    count = 0
            line[i] = 0
    return False


def is_overline(y,x):
    for j in range(4):
        cnt = 0
        for i in range(2):
            cur_y, cur_x = y, x
            while True:
                if board[cur_y][cur_x] == 0 or board[cur_y][cur_x] == -1:
                    break
                else:
                    cnt += 1
                cur_y, cur_x = y + list_dy[j * 2 + i], x + list_dx[j * 2 + i]

        if cnt > 5:
            return True

    return False

# def get_stone_count(x, y, color):

#     x1, y1 = x, y
#     cnt = 1  # 기준 돌 포함
#     # 4개의 기본 방향: (0, 1, 2, 3) 각 방향마다 두 쪽(양방향) 검사
#     for direction in range(4):
#         for i in range(2):
	       	
#             idx = direction * 2 + i 
            
#             dy = list_dy[idx]
#     	    dx = list_dx[idx]  
#         	x, y = x1, y1
  
#             while True:
#                 x  = x + dx
#                 y  = y + dy
#                 # 범위를 벗어나거나 노검일때 
#                 if x < 0 or x >= 15 or y < 0 or y >= 15 or board[y][x] != 1:
#                     break
                
#                 cnt += 1
#     return cnt

def is_samsam(y, x, color):
    cnt = 0
    board[y][x] = 1 #흑이라 치고 

    for direction in range(4):
        for i in range(2):
            
            idx = direction * 2 + i
            yy, xx = list_dy[idx], list_dx[idx] # direction 저장
            ny, nx = x, y # (y,x) 시작

            while True: # 타겟 좌표에서 8방 빈칸 색
                ny, nx = ny + yy, nx + xx
                if x < 0 or x >=15 or y < 0 or y >= 15 or board[ny][nx] != 0: # 범위 벗어난 경우
                    break
                else:
                    continue
            if 0 <x < 15 and 0 < y < 15 and board[ny][ny] == 1: # 바운드 안에 빈칸좌표 확인
                cy, cx = ny, nx # 열린 4를 확인 하기 위해 좌표 저장
            else:
                continue

            board[cy][cx] = 1 # 놨다 치고

            if is_five(cy, cx, color) == True: # 오목확인, open_four << 확정 오픈4, check_open_four << 잠재적 오픈4
                open_four = 0
            else:
                check_open_four = 0
                for j in range(2):
                    jdx = direction * 2 + j
                    cyy, cxx = list_dy[jdx], list_dx[jdx]
                    nny, nnx = cy, cx # (cy, cx) 부터 탐색 시작
                    
                    while True:
                        nny, nnx = nny + cyy, nnx + cxx
                        if x < 0 or x >=15 or y < 0 or y >= 15 or board[nny][nnx] != 0:
                            break
                    
                    if 0 <x < 15 and 0 < y < 15 and board[nny][nny] == 1:
                        if get_stone_count(cy, cx, color) == 4:
                            check_open_four += 1
              
                if check_open_four >= 2:
                    
                    if get_stone_count(cy, cx, color) == 4:
                        
                        open_four = 1

                    else:
                        open_four = 0
            
            board[cy][cx] = 0 #복구 

            if open_four == 1 and



                

