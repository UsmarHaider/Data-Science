
#AI moves are found in this file
import random

#piece score values
piece_score = {"K": 0, "Q": 9, "R": 5, "B": 3, "N": 3, "p": 1}

#piece position score values

knight_scores = [[0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0],
                 [0.1, 0.3, 0.5, 0.5, 0.5, 0.5, 0.3, 0.1],
                 [0.2, 0.5, 0.6, 0.65, 0.65, 0.6, 0.5, 0.2],
                 [0.2, 0.55, 0.65, 0.7, 0.7, 0.65, 0.55, 0.2],
                 [0.2, 0.5, 0.65, 0.7, 0.7, 0.65, 0.5, 0.2],
                 [0.2, 0.55, 0.6, 0.65, 0.65, 0.6, 0.55, 0.2],
                 [0.1, 0.3, 0.5, 0.55, 0.55, 0.5, 0.3, 0.1],
                 [0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0]]

#bishop scores  

bishop_scores = [[0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0],
                 [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
                 [0.2, 0.4, 0.5, 0.6, 0.6, 0.5, 0.4, 0.2],
                 [0.2, 0.5, 0.5, 0.6, 0.6, 0.5, 0.5, 0.2],
                 [0.2, 0.4, 0.6, 0.6, 0.6, 0.6, 0.4, 0.2],
                 [0.2, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.2],
                 [0.2, 0.5, 0.4, 0.4, 0.4, 0.4, 0.5, 0.2],
                 [0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0]]

#rook scores
rook_scores = [[0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
               [0.5, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.5],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.25, 0.25, 0.25, 0.5, 0.5, 0.25, 0.25, 0.25]]

#queen scores
queen_scores = [[0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0],
                [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
                [0.2, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
                [0.3, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
                [0.4, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
                [0.2, 0.5, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
                [0.2, 0.4, 0.5, 0.4, 0.4, 0.4, 0.4, 0.2],
                [0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0]]

#pawn scores
pawn_scores = [[0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8],
               [0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7],
               [0.3, 0.3, 0.4, 0.5, 0.5, 0.4, 0.3, 0.3],
               [0.25, 0.25, 0.3, 0.45, 0.45, 0.3, 0.25, 0.25],
               [0.2, 0.2, 0.2, 0.4, 0.4, 0.2, 0.2, 0.2],
               [0.25, 0.15, 0.1, 0.2, 0.2, 0.1, 0.15, 0.25],
               [0.25, 0.3, 0.3, 0.0, 0.0, 0.3, 0.3, 0.25],
               [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]]

#piece position scores dictionary for all pieces    
piece_position_scores = {
                        #white king scores
                        "wN": knight_scores,
                         #black knight scores
                         "bN": knight_scores[::-1],
                         #white bishop scores
                         "wB": bishop_scores,
                         #black bishop scores
                         "bB": bishop_scores[::-1],
                         #white queen scores
                         "wQ": queen_scores,
                         #black queen scores
                         "bQ": queen_scores[::-1],
                         #white rook scores
                         "wR": rook_scores,
                         #black rook scores
                         "bR": rook_scores[::-1],
                         #white pawn scores
                         "wp": pawn_scores,
                         #black pawn scores
                         "bp": pawn_scores[::-1]}

#checkmate and stalemate scores

CHECKMATE = 1000
STALEMATE = 0

#depth of the search tree
DEPTH = 3

#AI move function
#finds the best move using negamax algorithm
#uses alpha beta pruning to reduce the number of nodes to be evaluated
#uses multithreading to find the best move
#returns the best move
def findBestMove(game_state, valid_moves, return_queue):
    global next_move
    next_move = None
    random.shuffle(valid_moves)
    findMoveNegaMaxAlphaBeta(game_state, valid_moves, DEPTH, -CHECKMATE, CHECKMATE,
                             1 if game_state.white_to_move else -1)
    return_queue.put(next_move)

#negamax algorithm
#returns the best score
def findMoveNegaMaxAlphaBeta(game_state, valid_moves, depth, alpha, beta, turn_multiplier):
    # checkmate and stalemate
    global next_move
    if depth == 0:
        return turn_multiplier * scoreBoard(game_state)
    # move ordering - implement later //TODO
    max_score = -CHECKMATE
    for move in valid_moves:
        # make the move
        # undo the move
        # checkmate and stalemate
        # recursive call
        #MAKE MOVE AND GET VALID MOVES
        game_state.makeMove(move)
        #next move is the valid moves of the next player
        next_moves = game_state.getValidMoves()
        #next_moves = game_state.getAllPossibleMoves()
        # if the next player is white, then the turn multiplier is 1, else -1
        #turn_multiplier = 1 if game_state.white_to_move else -1
        score = -findMoveNegaMaxAlphaBeta(game_state, next_moves, depth - 1, -beta, -alpha, -turn_multiplier)
        #score is greater than max score
        if score > max_score:
            #max score is score
            max_score = score
            #if depth is 0, then next move is move
            if depth == DEPTH:
                #next move is move
                next_move = move
        #game state undo move       
        game_state.undoMove()
        #alpha is max of alpha and max score
        if max_score > alpha:
            #alpha is max score
            alpha = max_score
            #if alpha is greater than or equal to beta, then break
        if alpha >= beta:
            #break
            break
        #return max score
    return max_score

#score board function to score the board
#returns the score

def scoreBoard(game_state):
    """
    Score the board. A positive score is good for white, a negative score is good for black.
    """
    #checkmate and stalemate conditions are checked first and returned accordingly 
    if game_state.checkmate:
        #if white to move, then black wins and score is -1000   
        if game_state.white_to_move:
            #return -1000
            return -CHECKMATE  # black wins
        #else white wins and score is 1000
        else:
            #return 1000
            return CHECKMATE  # white wins
        #if stalemate, then return 0
        #return 0
    elif game_state.stalemate:
        # stalemate is a draw
        #  return 0
        # stalemate is a draw
        return STALEMATE
    #score is 0
    score = 0
    #for each row and column in the board
    #score is updated according to the piece and its position
    #piece position scores are used to score the board
    #piece scores are used to score the board
    for row in range(len(game_state.board)):
        #for each column in the board
        #piece is the piece in the board
        #if piece is not empty
        for col in range(len(game_state.board[row])):
            #piece is the piece in the board
            #if piece is not empty
            #piece position score is 0
            #if piece is not king
            #piece position score is piece position score of the piece
            piece = game_state.board[row][col]
            
            if piece != "--":
                # piece is not empty 
                #  piece position score is piece position score of the piece
                piece_position_score = 0
                #if piece[1] != "K":
                
                if piece[1] != "K":
                    piece_position_score = piece_position_scores[piece][row][col]
                #if piece is white, then score is piece score + piece position score
                if piece[0] == "w":
                    score += piece_score[piece[1]] + piece_position_score
                #else score is piece score + piece position score
                
                
                #piece score is subtracted from the score
                #piece is b and piece score is subtracted from the score
                if piece[0] == "b":
                    # score is subtracted by piece score and piece position score
                    score -= piece_score[piece[1]] + piece_position_score
    # score is returned
    return score

#find random move function
#returns a random valid move

def findRandomMove(valid_moves):
    return random.choice(valid_moves)
