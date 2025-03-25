import numpy as np
from typing import Tuple, List, Optional
from renju_rule import *
import copy

class Minimax:
    def __init__(self, depth: int = 3):
        """
        Initialize the Gomoku AI.
        Args:
            depth (int): The depth of the minimax search tree (default: 3)
        """
        self.depth = depth
        # Using the same direction vectors as in renju_rule.py
        self.list_dx = [-1, 1, -1, 1, 0, 0, 1, -1]
        self.list_dy = [0, 0, -1, 1, -1, 1, -1, 1]

    def evaluate_window(self, window: List[int], color: int) -> int:
        """
        Evaluate a window of 5 positions.
        Args:
            window: List of 5 positions containing 1 (black), -1 (white), or 0 (empty)
            color: Color to evaluate for (1 for black, -1 for white)
        Returns:
            Score for the window
        """
        score = 0
        opponent = -color
                            # a, b, c, d : 1000, e : 10000 - 9000, f : 1000 - 800, g : 800
        # Winning patterns
        if window.count(color) == 5:
            score += 100000
        # Open four (one move to win)
        elif window.count(color) == 4 and window.count(0) == 1:
            score += 10000
        # Open three
        elif window.count(color) == 3 and window.count(0) == 2:
            score += 1000
        # Open two
        elif window.count(color) == 2 and window.count(0) == 3:
            score += 100
        
        # Defensive patterns
        if window.count(opponent) == 4 and window.count(0) == 1:
            score -= 9000
        elif window.count(opponent) == 3 and window.count(0) == 2:
            score -= 800
            
        return score

    def evaluate_board(self, board: List[List[int]], color: int) -> int:
        """
        Evaluate the entire board state.
        Args:
            board: Current game board
            color: Color to evaluate for
        Returns:
            Total score for the board
        """
        score = 0
        
        # Evaluate in all 4 directions using direction vectors
        for direction in range(4):
            for i in range(2):
                idx = direction * 2 + i
                dx, dy = self.list_dx[idx], self.list_dy[idx]
                
                # Scan the board
                for row in range(15):
                    for col in range(15):
                        window = []
                        # Get 5 consecutive positions in current direction
                        for k in range(5):
                            new_row = row + k * dy
                            new_col = col + k * dx
                            if 0 <= new_row < 15 and 0 <= new_col < 15:
                                window.append(board[new_row][new_col])
                            else:
                                break
                        
                        if len(window) == 5:
                            score += self.evaluate_window(window, color)
        
        return score

    def get_valid_moves(self, board: List[List[int]], color: int) -> List[Tuple[int, int]]:
        """
        Get list of valid moves (empty positions near existing stones).
        Consider renju rules (forbidden moves) for black stones.
        Args:
            board: Current game board
            color: Color of the current player (1 for black, -1 for white)
        Returns:
            List of valid move coordinates
        """
        valid_moves = []
        for i in range(15):
            for j in range(15):
                if board[i][j] == 0:  # Empty position
                    # Check if there's a stone within 2 spaces
                    has_neighbor = False
                    for direction in range(4):
                        for side in range(2):
                            idx = direction * 2 + side
                            for dist in range(1, 3):  # Check 1 and 2 spaces away
                                ni = i + self.list_dy[idx] * dist
                                nj = j + self.list_dx[idx] * dist
                                if (0 <= ni < 15 and 0 <= nj < 15 and 
                                    board[ni][nj] != 0):
                                    has_neighbor = True
                                    break
                        if has_neighbor:
                            break
                    
                    if has_neighbor:
                        # Check forbidden moves for black stones
                        if color == 1:  # If black
                            # Check for forbidden moves (33, 44, overline)
                            if (is_double_three(board, i, j, color) or 
                                is_double_four(board, i, j) or 
                                is_overline(board, i, j)):
                                continue
                        valid_moves.append((i, j))
                        
        # print(valid_moves)
        # print("-----------------------------------------------")
        return valid_moves

    def minimax(self, board: List[List[int]], depth: int, alpha: float, beta: float, 
                maximizing_player: bool, color: int) -> Tuple[int, Optional[Tuple[int, int]]]:
        """
        Minimax algorithm with alpha-beta pruning.
        Args:
            board: Current game board
            depth: Current depth in the search tree
            alpha: Alpha value for pruning
            beta: Beta value for pruning
            maximizing_player: True if maximizing, False if minimizing
            color: Color of the current player
        Returns:
            Tuple of (score, best_move)
        """
        # Check for terminal states
        result = check_if_win(board, -1, -1, color)  # Using -1,-1 as dummy coordinates
        if result:
            return (100000 if maximizing_player else -100000), None
        
        if depth == 0:
            return self.evaluate_board(board, color), None

        valid_moves = self.get_valid_moves(board, color)
        if not valid_moves:
            return 0, None

        best_move = valid_moves[0]
        
        if maximizing_player:
            max_eval = float('-inf')
            for move in valid_moves:
                i, j = move
                board[i][j] = color
                eval_score, _ = self.minimax(board, depth-1, alpha, beta, False, color)
                board[i][j] = 0  # Undo move
                
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = float('inf')
            for move in valid_moves:
                i, j = move
                board[i][j] = -color
                eval_score, _ = self.minimax(board, depth-1, alpha, beta, True, color)
                board[i][j] = 0  # Undo move
                
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            return min_eval, best_move

    def get_best_move(self, board: List[List[int]], color: int) -> Optional[Tuple[int, int]]:
        """
        Get the best move for the current board state.
        Args:
            board: Current game board
            color: Color of the current player
        Returns:
            Tuple of (row, col) for the best move
        """
        # For black stones, ensure moves follow renju rules
        _, best_move = self.minimax(
            board, 
            self.depth, 
            float('-inf'), 
            float('inf'), 
            True, 
            color
        )
        
        # Double check the move is valid (especially for black stones)
        if best_move:
            row, col = best_move
            if color == 1:  # If black
                if (is_double_three(board, row, col, color) or 
                    is_double_four(board, row, col) or 
                    is_overline(board, row, col)):
                    # If the best move is forbidden, try to find another valid move
                    valid_moves = self.get_valid_moves(board, color)
                    if valid_moves:
                        return valid_moves[0]  # Return first valid move as fallback
                    return None
        
        return best_move