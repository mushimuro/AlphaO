import copy
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


# TODO: is_valid 랑 is_placeable 이랑 뭐가 다름? - 웅기
# board is (y,x)
# color : black : 1 & white : -1 & default : 0
def is_valid(y, x):
    return board[y][x] == 0

# y,x 를 좌표를 받았을 때 이게 out of bound 인지 확인하는 함수
# is_valid 하는게 딱히 없으면 is_valid 로 바꿀 예정
def is_invalid(y, x):
    return x < 0 or x > 14 or y < 0 or y > 14

#####################################
# 이거 이름을 check_list_for_win() 같은걸로 바꾸는게?
#####################################
# only checks for winning status
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


def pre_check(gui_board, y, x, color):
    line = []

    # 가로줄 ; This removes edge cases
    if (gui_board[y][max(0,x-1)] == color) or (gui_board[y][min(14,x+1)] == color):
        # normal case or edge cases
        if ((x != 14 and x != 0) or (x == 14 and gui_board[y][x-1] == color) or (x == 0 and gui_board[y][x+1] == color)):
            for i in range(max(0, x-5), min(15, x+6), 1):
                line.append(gui_board[y][i])
            # check for 5-win
            if check_list(color, line): return "win"   # TODO : change return "checked" -> return True

    # 세로줄 (14,12)
    if (gui_board[max(0, y - 1)][x] == color) or (gui_board[min(14, y + 1)][x] == color):
        if ((y != 14 and y != 0) or (y == 14 and gui_board[y-1][x] == color) or (y == 0 and gui_board[y+1][x] == color)):
            for i in range(max(0, y - 5), min(15, y + 6), 1):
                line.append(gui_board[i][x])
            # check for 5-win
            check = check_list(color, line)
            if check:
                return "win"   # TODO : change return "checked" -> return True

    # 좌측 상단 + 우측 하단 대각선
    if (gui_board[max(0, y - 1)][max(0, x - 1)] == color) or (gui_board[min(14, y + 1)][min(14, x + 1)] == color):
        if ((y != 14 and y != 0 and x != 14 and x != 0) or ((y == 0 or x == 0) and gui_board[y+1][x+1] == color) or ((y == 14 or x == 14) and board[y-1][x-1] == color)):
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
                line.append(gui_board[y+i][x+i])
            # check for 5-win
            if check_list(color, line): return "win"   # TODO : change return "checked" -> return True

    # 좌측 하단 + 우측 상단
    if (gui_board[min(14, y + 1)][max(0, x - 1)] == color) or (gui_board[max(0, y - 1)][min(14, x + 1)] == color):
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
                line.append(gui_board[y+i][x-i])
            # check for 5-win
            if check_list(color, line): return "win"   # TODO : change return "checked" -> return True


    # if not 5 stone
    return "Not is_five"   # TODO : change to False

# 흑돌이 둔 후, 금수가 생기는지 확인
# 금수가 생기면 ban 리스트에 저장
def find_prohibit_point(gui_board, y, x):
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
                    if is_samsam(gui_board, cur_y, cur_x) or is_double_four(gui_board, cur_y, cur_x) or is_overline(gui_board, cur_y,cur_x):
                        ban.append({cur_y, cur_x})
                # Black
                elif board[cur_y][cur_x] == 1:
                    cnt += 1
                # White
                elif board[cur_y][cur_x] == -1:
                    break

                cur_y, cur_x = y + list_dy[j * 2 + i], x + list_dx[j * 2 + i]


# 백돌을 둠으로써 금수가 해제되는지 확인
def check_prohibit_point(gui_board, ban):
    if len(ban) == 0: return

    for i in ban:
        y, x = i
        if is_samsam(y, x) or is_double_four(y, x) or is_overline(gui_board, y, x):
            ban.remove(i)


# TODO 한줄에 4-4 나오는거 추가
# 8방향에서 흑돌, 첫번째 공백만 담는 리스트 생성
# 그 리스트에서 오목을 만들 수 있는지 확인
# 오목을 2개 이상 만들 수 있으면 4-4로 간주하고 리턴
def is_double_four(gui_board, y, x):
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
                if is_invalid(cur_y, cur_x): break
                if gui_board[cur_y][cur_x] == 0:
                    empty_cnt += 1
                elif empty_cnt == 2 or gui_board[cur_y][cur_x] == -1:
                    break

                if i == 0:
                    line.append(gui_board[cur_y][cur_x])
                else:
                    line.insert(0, gui_board[cur_y][cur_x])
                    center += 1

                cur_y, cur_x = y + list_dy[j * 2 + i], x + list_dx[j * 2 + i]

        # 오목되는지 체크
        if make_five_row(line):
            four_cnt += 1
            if four_cnt >= 2: return True
    return False

# 받은 리스트에서 오목을 만들 수 있는지 확인
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

# 장목 확인
# 4방향 확인해서 돌이 6개 이상 인지 확인
def is_overline(gui_board, y,x):
    for j in range(4):
        cnt = 0
        # 양쪽의 돌을 같이 세서 한번에 확인
        for i in range(2):
            cur_y, cur_x = y, x
            while True:
                # out of bound check
                if is_invalid(cur_y, cur_x): break

                # board 에 다른 돌이면 탈출
                if gui_board[cur_y][cur_x] == 0 or gui_board[cur_y][cur_x] == -1:
                    break
                # 흑돌 일때만 카운트
                else:
                    cnt += 1
                cur_y, cur_x = y + list_dy[j * 2 + i], x + list_dx[j * 2 + i]
        # 6개 이상이면 장목
        if cnt > 5:
            return True

    return False

def get_stone_direction(gui_board, y, x, color, direction_vector):

    cnt = 1  # 시작 돌 포함
    dy = direction_vector[0]
    dx = direction_vector[1]
    
    
    # 정방향 탐색 
    yy, xx = y, x
    for coord in range(1,5):        
        yy = y + dy * coord
        xx = x + dx * coord
        if yy < 0 or yy >= 15 or xx < 0 or xx >= 15  or gui_board[yy][xx] != color:
            break
        cnt += 1
    
    # 역방향 탐색
    yy, xx = y, x
    for coord in range(1,5):       
        yy = y - dy * coord
        xx = x - dx * coord
        if yy < 0 or yy >= 15 or xx < 0 or xx >= 15  or gui_board[yy][xx] != color:
            break
        cnt += 1

    return cnt


def is_samsam(board, y, x, color):
    cnt = 0
    gui_board = copy.deepcopy(board)
    gui_board[y][x] = 1 #흑이라 치고

    for direction in range(4):
        open_three = False # 각 dircetion 시작 시 초기화
        for i in range(2):

            idx = direction * 2 + i
            yy, xx = list_dy[idx], list_dx[idx] # direction 저장
            ny, nx = y, x # (y,x) 시작

            while True: # 타겟 좌표에서 8방 빈칸 색
                ny, nx = ny + yy, nx + xx
                if nx < 0 or nx >=15 or ny < 0 or ny >= 15 or gui_board[ny][nx] != 0: # 범위 벗어난 경우
                    break
                else:
                    continue
            if 0 < nx < 15 and 0 < ny < 15 and gui_board[ny][nx] == 1: # 바운드 안에 빈칸좌표 확인
                direction_vector = (yy,xx) # open4 케이스에서 오목 확인하기 위해 방향 저장
                cy, cx = ny, nx # 열린 4를 확인 하기 위해 좌표 저장
            else:
                continue

            gui_board[cy][cx] = 1 # 놨다 치고
            c_line = [] # 오목체크 라인

            for c in range(-4, 5): # cy,cx를 중심 좌표로 받고, 저장된 디렉션 벡터기반 해당 라인 저장
                ny_line = cy + c * direction_vector[0]
                nx_line = cx + c * direction_vector[1]

                if 0 <= ny_line < 15 and 0 <= nx_line < 15:
                    c_line.append(gui_board[ny_line][nx_line])
                else:
                    c_line.append(0)

            if make_five_row(c_line): # 오목확인, open_four << 확정 오픈4, check_open_four << 잠재적 오픈4
                open_four = 0

            else:
                check_open_four = 0
                for j in range(2):
                    jdx = direction * 2 + j
                    cyy, cxx = list_dy[jdx], list_dx[jdx]
                    nny, nnx = cy, cx # (cy, cx) 부터 탐색 시작

                    while True:
                        nny, nnx = nny + cyy, nnx + cxx
                        if nnx < 0 or nnx >=15 or nny < 0 or nny >= 15 or gui_board[nny][nnx] != 0:
                            break

                    if 0 < nnx < 15 and 0 < nny < 15 and gui_board[nny][nnx] == 1:
                        if get_stone_direction(gui_board, cy, cx, color, direction_vector) == 4:
                            check_open_four += 1

                if check_open_four >= 2:

                    if get_stone_direction(gui_board, cy, cx, color, direction_vector) >= 4:

                        open_four = 1

                    else:
                        open_four = 0
                else:
                    open_four = 0

            gui_board[cy][cx] = 0 #복구

            if open_four == 1:# 다시 이전 빈칸 board[y][x]와서 오픈 3 가능성 확인
                #if 오목이고, 장목이 아니고, 삼삼이나 사사가 아니면, 트루
                open_three = True
                break
        if open_three: #오픈삼 카운트
            cnt += 1

    gui_board[y][x] = 0 # 다시 빈칸 복구

    if cnt >= 2:
        print("is SAMSAM")
        return True
    return False





                

