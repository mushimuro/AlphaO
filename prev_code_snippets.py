# 좌측 상단 + 우측 하단 대각선
if ((y != 0 or x!= 0) and board[max(0, y - 1)][max(0, x - 1)] == color) or ((y != 14 or x != 14) and board[min(14, y + 1)][min(14, x + 1)] == color):
    xrange = [max(0, x-4), min(15, x+5)]
    yrange = [max(0, y - 4), min(15, y + 5)]

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
    #if check_list_five(color, line): return True