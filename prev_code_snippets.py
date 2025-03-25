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



        # placing stones
    def mousePressEvent(self, event):
        x, y = event.position().x(), event.position().y()
        col = int(x // CELL_SIZE)   # x-value
        row = int(y // CELL_SIZE)   # y-value

        if self.is_valid_move(row, col):
            self.board[row][col] = self.current_player
            self.update()

            # check for win
            if check_if_win(self.board, row, col, self.current_player):
                winner_color = "Black" if self.current_player == 1 else "White"
                self.game_over_signal.emit(winner_color)
            else:
                self.current_player = -1 if self.current_player == 1 else 1
                self.is_ai_turn = True if self.current_player == -1 else False
                # self.update()

        if self.is_ai_turn:
            start_time = time.time()
            self.ai_move()
            end_time = time.time()
            execution_time = end_time - start_time
            print(f"AI move execution time: {execution_time:.6f} seconds")

            self.is_ai_turn = False