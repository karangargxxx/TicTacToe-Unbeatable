"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    Returns X,O based on whose turn it is.
    """
    emptyCount = 0
    for row in board:
        for value in row:
            if value == EMPTY:
                emptyCount += 1
    # ie if even number of empty spaces on board than it is O's turn.
    if emptyCount%2 == 0:
        return O
    return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possibleActions = set()
    for i, row in enumerate(board):
        for j, value in enumerate(row):
            if value == EMPTY:
                possibleActions.add((i, j))
    return possibleActions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board,
    without changing the original board.
    """
    if board[action[0]][action[1]] != EMPTY:
        raise Exception("Invalid Action for this board")
    newBoard = deepcopy(board)
    move = player(newBoard)
    newBoard[action[0]][action[1]] = move
    return newBoard


def winner(board):
    """
    Returns the winner of the game, if there is one, else return None.
    """
    # this represents sum of (rows, [col1, col2, col3], [diag1, diag2]).
    sumRow, sumCol, sumDiag = 0, [0, 0, 0], [0, 0]
    # check all rows
    for row in board:
        sumRow = 0
        for value in row:
            if value == X:
                sumRow += 1
            if value == O:
                sumRow -= 1
        if sumRow == 3:
            return X
        elif sumRow == -3:
            return O
    # check all columns and both diagonals
    for i, row in enumerate(board):
        for j, value in enumerate(row):
            if value == X:
                sumCol[j] += 1
            elif value == O:
                sumCol[j] -= 1
            if value == X and i == j:
                sumDiag[0] += 1
            elif value == O and i == j:
                sumDiag[0] -= 1
            if value == X and i+j == 2:
                sumDiag[1] += 1
            elif value == O and i+j == 2:
                sumDiag[1] -= 1
    if 3 in sumCol or 3 in sumDiag:
        # print(sumCol)
        return X
    elif -3 in sumCol or -3 in sumDiag:
        # print(sumCol)
        return O
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    result = winner(board)
    if result == X or result == O:
        return True
    if not any(EMPTY in subList for subList in board):
        return True
    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    This function assumes that if the game has been won by any than there are no more moves made after winning of any X or O.
    In case the above assumption is false than it will not work.
    This has been done to increase performance by not calling the winner function.
    Even EMPTY means X won, Odd means O won.
    If 0 EMPTY then either X won or tie.
    This function tries to maximize performance as much as it can. 
    """
    numEmpty = 0
    for row in board:
        for value in row:
            if value ==  EMPTY:
                numEmpty += 1
    if numEmpty == 0:
        if winner(board) == X:
            return 1
        return 0
    else:
        if numEmpty%2 == 0:
            return 1
        else:
            return -1



def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    curPlayer = player(board)
    possibleActions = list(actions(board))
    possibleResults = []
    if curPlayer == X:
        for action in possibleActions:
            possibleResults.append(minValue(result(board, action), -1))
        choose = possibleResults.index(max(possibleResults))
        return possibleActions[choose]
    else:
        for action in possibleActions:
            possibleResults.append(maxValue(result(board, action), 1))
        choose = possibleResults.index(min(possibleResults))
        return possibleActions[choose]


def maxValue(board, beta):
    """
    A function which returns the value of the current state of board by putting itself into the shoes of the X player,
    it tries to maximize the score or the utility of the board by asking for every action what will be the utility after
    the min player or the O player makes the move.
    This function explores every action by recursively getting score from the min player and then itself to get utility
    of the board for this action if both the players are playing optimally or to say smartly.
    """
    if terminal(board):
        return utility(board)
    score = -1
    possibleActions = actions(board)
    for action in possibleActions:
        if score > beta:
            return score
        score = max(score, minValue(result(board,action), score))
    return score
    

def minValue(board, alpha):
    """
    A function which returns the value of the current state of board by putting itself into the shoes of the O player,
    it tries to minimize the score or the utility of the board by asking for every action what will be the utility after
    the max player or the X player makes the move.
    This function explores every action by recursively getting score from the max player and then itself to get utility
    of the board for this action if both the players are playing optimally or to say smartly.
    """
    if terminal(board):
        return utility(board)
    score = 1
    possibleActions = actions(board)
    for action in possibleActions:
        if score <= alpha:
            return score
        score = min(score, maxValue(result(board,action), score))
    return score
