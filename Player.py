import numpy as np
import math
import copy
import random
infinity = float("inf")


class AIPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)
        self.limited_depth = 3

    def get_alpha_beta_move(self, board):
        """
        Given the current state of the board, return the next move based on
        the alpha-beta pruning algorithm

        This will play against either itself or a human player

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """
        
        # board = [x[:] for x in board]
        board = np.copy(board)

        if self.player_number == 1:
            player_2 = 2
        else:
            player_2 = 1


        def max_value(board):
            if (self.game_completed(board,1) or self.game_completed(board,2)):
                return self.evaluation_function(board),-1


            if self.limited_depth == 0:
                return self.evaluation_function(board), -1

            v = -infinity
            mov = 0

            self.limited_depth -= 1

            moves = self.actions(board)
            # random.shuffle(moves)

            for a in moves:

                minV = min_value(self.update_board(a, board, self.player_number))

                if (v < minV[0]):
                    v = minV[0]
                    mov = a
            self.limited_depth += 1

            return v,mov

        def min_value(board):

            if (self.game_completed(board,1) or self.game_completed(board,2)):
                return self.evaluation_function(board),-1

            if self.limited_depth == 0:
                return self.evaluation_function(board), -1

            v = infinity
            mov = 0

            self.limited_depth -= 1

            moves = self.actions(board)
            # random.shuffle(moves)
            for a in moves:
                maxV = max_value(self.update_board(a, board, player_2))
                if (v > maxV[0]):
                    v = maxV[0]
                    mov = a
            self.limited_depth += 1
            return v,mov

        utility,mov = max_value(board)
        print(utility)

        return mov

    def get_expectimax_move(self, board):
        """
        Given the current state of the board, return the next move based on
        the expectimax algorithm.

        This will play against the random player, who chooses any valid move
        with equal probability

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """
        raise NotImplementedError('Whoops I don\'t know what to do')

    def evaluation_function(self, board):
        """
        Given the current stat of the board, return the scalar value that
        represents the evaluation function for the current player

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The utility value for the current board
        """
        if(self.player_number == 1):
            player_2 = 2
        else:
            player_2 = 1

        player_num = self.player_number

        heur = 0
        state = board
        for i in range(0, 7):
            for j in range(0, 6):
                # check horizontal streaks
                try:
                    # add player one streak scores to heur
                    if state[i][j] == state[i + 1][j] == player_num:
                        heur += 10
                    if state[i][j] == state[i + 1][j] == state[i + 2][j] == player_num:
                        heur += 100
                    if state[i][j] == state[i + 1][j] == state[i + 2][j] == state[i + 3][j] == player_num:
                        heur += 10000
                    # if state[i][j] == state[i + 1][j] == state[i + 2][j] == state[i + 3][j] == state[i + 4][j] == player_num:
                    #     heur += 10000
                except IndexError:
                    pass
                
                try:
                    # subtract player two streak score to heur
                    if state[i][j] == state[i + 1][j] == player_2:
                        heur -= 10
                    if state[i][j] == state[i + 1][j] == state[i + 2][j] == player_2:
                        heur -= 100
                    if state[i][j] == state[i + 1][j] == state[i + 2][j] == state[i + 3][j] == player_2:
                        heur -= 10000
                        # return -10000
                    # if state[i][j] == state[i + 1][j] == state[i + 2][j] == state[i + 3][j] == state[i + 4][j] == player_2:
                    #     heur -= 100000
                except IndexError:
                    pass

                # check vertical streaks
                try:
                    # add player one vertical streaks to heur
                    if state[i][j] == state[i][j + 1] == player_num:
                        heur += 10
                    if state[i][j] == state[i][j + 1] == state[i][j + 2] == player_num:
                        heur += 100
                    if state[i][j] == state[i][j + 1] == state[i][j + 2] == state[i][j + 3] == player_num:
                        heur += 10000
                    # if state[i][j] == state[i][j + 1] == state[i][j + 2] == state[i][j + 3] == state[i][j + 4] == player_num:
                    #     heur += 10000
                except IndexError:
                    pass
                
                try:
                    # subtract player two streaks from heur
                    if state[i][j] == state[i][j + 1] == player_2:
                        heur -= 10
                    if state[i][j] == state[i][j + 1] == state[i][j + 2] == player_2:
                        heur -= 100
                    if state[i][j] == state[i][j + 1] == state[i][j + 2] == state[i][j + 3] == player_2:
                        heur -= 10000
                        # return -10000
                    # if state[i][j] == state[i][j + 1] == state[i][j + 2] == state[i][j + 3] == state[i][j + 4] == player_2:
                    #     heur -= 100000
                except IndexError:
                    pass

                # check positive diagonal streaks
                try:
                    # add player one streaks to heur
                    if not j + 3 > 6 and state[i][j] == state[i + 1][j + 1] == player_num:
                        heur += 10
                    if not j + 3 > 6 and state[i][j] == state[i + 1][j + 1] == state[i + 2][j + 2] == player_num:
                        heur += 100
                    if not j + 3 > 6 and state[i][j] == state[i + 1][j + 1] == state[i + 2][j + 2] \
                            == state[i + 3][j + 3] == player_num:
                        heur += 10000
                except IndexError:
                    pass
                
                try:
                    # add player two streaks to heur
                    if not j + 3 > 6 and state[i][j] == state[i + 1][j + 1] == player_2:
                        heur -= 10
                    if not j + 3 > 6 and state[i][j] == state[i + 1][j + 1] == state[i + 2][j + 2] == player_2:
                        heur -= 100
                    if not j + 3 > 6 and state[i][j] == state[i + 1][j + 1] == state[i + 2][j + 2] \
                            == state[i + 3][j + 3] == player_2:
                        heur -= 10000
                        # return -10000
                except IndexError:
                    pass

                # check negative diagonal streaks
                try:
                    # add  player one streaks
                    if state[i][j] == state[i + 1][j - 1] == player_num:
                        heur += 10
                    if state[i][j] == state[i + 1][j - 1] == state[i + 2][j - 2] == player_num:
                        heur += 100
                    if state[i][j] == state[i + 1][j - 1] == state[i + 2][j - 2] \
                            == state[i + 3][j - 3] == player_num:
                        heur += 10000

                except IndexError:
                    pass
                
                try:
                    # subtract player two streaks
                    if state[i][j] == state[i + 1][j - 1] == player_2:
                        heur -= 10
                    if state[i][j] == state[i + 1][j - 1] == state[i + 2][j - 2] == player_2:
                        heur -= 100
                    if state[i][j] == state[i + 1][j - 1] == state[i + 2][j - 2] \
                            == state[i + 3][j - 3] == player_2:
                        heur -= 10000
                        # return -10000
                except IndexError:
                    pass
        return heur

    def game_completed(self,board,player_num):
        player_win_str = '{0}{0}{0}{0}'.format(player_num)
        to_str = lambda a: ''.join(a.astype(str))
        board = np.copy(board)

        def check_horizontal(b):
            for row in b:
                if player_win_str in to_str(row):
                    return True
            return False

        def check_verticle(b):
            return check_horizontal(b.T)

        def check_diagonal(b):
            for op in [None, np.fliplr]:
                op_board = op(b) if op else b
                
                root_diag = np.diagonal(op_board, offset=0).astype(np.int)
                if player_win_str in to_str(root_diag):
                    return True

                for i in range(1, b.shape[1]-3):
                    for offset in [i, -i]:
                        diag = np.diagonal(op_board, offset=offset)
                        diag = to_str(diag.astype(np.int))
                        if player_win_str in diag:
                            return True

            return False

        return (check_horizontal(board) or
                check_verticle(board) or
                check_diagonal(board))


    def actions(self, board):
        acts = []
        for i in range(7):
            if 0 in board[:, i]:
                acts.append(i)
        return acts

    def update_board(self, move, board, player_num):
        # board = [x[:] for x in board]
        board = np.copy(board)
        if 0 in board[:, move]:
            update_row = -1
            for row in range(1, board.shape[0]):
                update_row = -1
                if board[row, move] > 0 and board[row - 1, move] == 0:
                    update_row = row - 1
                elif row == board.shape[0] - 1 and board[row, move] == 0:
                    update_row = row

                if update_row >= 0:
                    board[update_row, move] = player_num
                    return board
        else:
            print(board)
            err = 'Invalid move by player {}. Column {}'.format(player_num, move)
            raise Exception(err)

    def clear_board(self, move, board, player_num):
        if player_num in board[:, move]:
            update_row = -1
            for row in range(1, board.shape[0]):
                update_row = -1
                if board[row, move] > 0 and board[row - 1, move] == 0:
                    update_row = row

                if update_row >= 0:
                    board[update_row, move] = 0
                    return board
        else:
            print(board)
            err = 'Invalid move by player {}. Column {}'.format(player_num, move)
            raise Exception(err)



class RandomPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'random'
        self.player_string = 'Player {}:random'.format(player_number)

    def get_move(self, board):
        """
        Given the current board state select a random column from the available
        valid moves.

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """
        valid_cols = []
        for col in range(board.shape[1]):
            if 0 in board[:, col]:
                valid_cols.append(col)

        return np.random.choice(valid_cols)


class HumanPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'human'
        self.player_string = 'Player {}:human'.format(player_number)

    def get_move(self, board):
        """
        Given the current board state returns the human input for next move

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """

        valid_cols = []
        for i, col in enumerate(board.T):
            if 0 in col:
                valid_cols.append(i)

        move = int(input('Enter your move: '))

        while move not in valid_cols:
            print('Column full, choose from:{}'.format(valid_cols))
            move = int(input('Enter your move: '))

        return move

