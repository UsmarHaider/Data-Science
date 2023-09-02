"""
Storing all the information about the current state of chess game.
Determining valid moves at current state.
It will keep move log.
"""


class GameState:
    # piece square tables
    # positive score means white is in advantage, negative score means black is in advantage
    # source: https://www.chessprogramming.org
    def __init__(self):
        # board is an 8x8 2d list, each element of the list has 2 characters.
        # The first character represents the color of the piece, 'b' or 'w'
        # The second character represents the type of the piece, 'K', 'Q', 'R', 'B', 'N' or 'p'
        # "--" represents an empty space with no piece
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        # move function dictionary mapping piece moved to the function it performs
        #   (note: pawn promotion and en-passant are not handled here)
        #   (note2: castling is not handled here)
        #   (note3: the key:value pairs are piece:method)
        #   (note4: the methods are defined below)
        #   (note5: the methods take in the row, column, and moves list as parameters)
        # move function getPawnMoves is defined below
        # move function getRookMoves is defined below
        # move function getKnightMoves is defined below
        # move function getBishopMoves is defined below
        # move function getQueenMoves is defined below
        # move function getKingMoves is defined below
        self.moveFunctions = {"p": self.getPawnMoves, "R": self.getRookMoves, "N": self.getKnightMoves,
                              "B": self.getBishopMoves, "Q": self.getQueenMoves, "K": self.getKingMoves}
        self.white_to_move = True # if it is white's turn
        self.move_log = [] # log of all the moves made in the game
        self.white_king_location = (7, 4) # the current location of the white king (row, col)
        self.black_king_location = (0, 4) # the current location of the black king (row, col)
        self.checkmate = False # if the game is over or not
        self.stalemate = False # if the game is over or not
        self.in_check = False # if the current player is in check
        self.pins = [] # squares where the allied pinned piece is and the direction pinned from
        self.checks = [] # squares where enemy is applying a check
        self.enpassant_possible = ()  # coordinates for the square where en-passant capture is possible
        self.enpassant_possible_log = [self.enpassant_possible] # keep track of en-passant squares so we can undo
        self.current_castling_rights = CastleRights(True, True, True, True) # castling rights at the start of the game
        self.castle_rights_log = [CastleRights(self.current_castling_rights.wks, self.current_castling_rights.bks,
                                               self.current_castling_rights.wqs, self.current_castling_rights.bqs)] # keep track of castling rights so we can undo
        

    def makeMove(self, move):
        # make the move (will not work for castling, pawn promotion and en-passant)
        
        #Takes a Move as a parameter and executes it.
        #(this will not work for castling, pawn promotion and en-passant)
        
        self.board[move.start_row][move.start_col] = "--" # empty the start square  
        self.board[move.end_row][move.end_col] = move.piece_moved # move the piece to the end square
        self.move_log.append(move)  # log the move so we can undo it later
        self.white_to_move = not self.white_to_move  # switch players
        # update king's location if moved
        if move.piece_moved == "wK": # if the white king moved 
            self.white_king_location = (move.end_row, move.end_col) # update the location of the white king
        elif move.piece_moved == "bK": # if the black king moved
            self.black_king_location = (move.end_row, move.end_col) # update the location of the black king

        # pawn promotion
        if move.is_pawn_promotion: # if the move is a pawn promotion
            # if not is_AI:
            #    promoted_piece = input("Promote to Q, R, B, or N:") #take this to UI later
            #    self.board[move.end_row][move.end_col] = move.piece_moved[0] + promoted_piece
            # else:
            self.board[move.end_row][move.end_col] = move.piece_moved[0] + "Q" # default promotion is to queen

        # enpassant move
        if move.is_enpassant_move: # if the move is an en-passant
            self.board[move.start_row][move.end_col] = "--"  # capturing the pawn

        # update enpassant_possible variable
        if move.piece_moved[1] == "p" and abs(move.start_row - move.end_row) == 2:  # only on 2 square pawn advance
            self.enpassant_possible = ((move.start_row + move.end_row) // 2, move.start_col) # the square where en-passant capture is possible
        else:
            self.enpassant_possible = () # reset enpassant_possible

        # castle move
        if move.is_castle_move: # if the move is a castle move
            if move.end_col - move.start_col == 2:  # king-side castle move
                self.board[move.end_row][move.end_col - 1] = self.board[move.end_row][
                    move.end_col + 1]  # moves the rook to its new square
                self.board[move.end_row][move.end_col + 1] = '--'  # erase old rook
            else:  # queen-side castle move
                self.board[move.end_row][move.end_col + 1] = self.board[move.end_row][
                    move.end_col - 2]  # moves the rook to its new square
                self.board[move.end_row][move.end_col - 2] = '--'  # erase old rook

        self.enpassant_possible_log.append(self.enpassant_possible) # update the enpassant_possible log

        # update castling rights - whenever it is a rook or king move
        self.updateCastleRights(move) # update the castle rights        
        self.castle_rights_log.append(CastleRights(self.current_castling_rights.wks, self.current_castling_rights.bks,
                                                   self.current_castling_rights.wqs, self.current_castling_rights.bqs)) # update the castle rights log

    def undoMove(self):
        """
        Undo the last move
        """
        if len(self.move_log) != 0:  # make sure that there is a move to undo
            move = self.move_log.pop() # pop the last move from the move log
            self.board[move.start_row][move.start_col] = move.piece_moved # put the piece back to its start square
            self.board[move.end_row][move.end_col] = move.piece_captured # put the captured piece back to its end square
            self.white_to_move = not self.white_to_move  # swap players
            # update the king's position if needed
            if move.piece_moved == "wK": # if the white king moved
                self.white_king_location = (move.start_row, move.start_col) # update the location of the white king
            elif move.piece_moved == "bK":# if the black king moved
                self.black_king_location = (move.start_row, move.start_col) # update the location of the black king
            # undo en passant move
            if move.is_enpassant_move: # if the move was an en-passant move
                self.board[move.end_row][move.end_col] = "--"  # leave landing square blank
                self.board[move.start_row][move.end_col] = move.piece_captured # put the captured piece back to the start square it was captured from

            self.enpassant_possible_log.pop() # update the enpassant_possible log
            self.enpassant_possible = self.enpassant_possible_log[-1] # update the enpassant_possible variable

            # undo castle rights
            self.castle_rights_log.pop()  # get rid of the new castle rights from the move we are undoing
            self.current_castling_rights = self.castle_rights_log[
                -1]  # set the current castle rights to the last one in the list
            # undo the castle move
            if move.is_castle_move: # if the move was a castle move
                if move.end_col - move.start_col == 2:  # king-side
                    self.board[move.end_row][move.end_col + 1] = self.board[move.end_row][move.end_col - 1] # moves the rook to its new square
                    self.board[move.end_row][move.end_col - 1] = '--' # erase old rook
                else:  # queen-side
                    self.board[move.end_row][move.end_col - 2] = self.board[move.end_row][move.end_col + 1] # moves the rook to its new square
                    self.board[move.end_row][move.end_col + 1] = '--' # erase old rook
            self.checkmate = False # since we can only get to this method if the king is not in checkmate, we can safely say that checkmate is false
            self.stalemate = False # since we can only get to this method if the king is not in stalemate, we can safely say that stalemate is false

    def updateCastleRights(self, move): # update the castle rights given the move
        """
        Update the castle rights given the move
        """
        if move.piece_captured == "wR": # if a white rook was captured
            if move.end_col == 0:  # left rook
                self.current_castling_rights.wqs = False # white can no longer castle queen-side
            elif move.end_col == 7:  # right rook
                self.current_castling_rights.wks = False # white can no longer castle king-side
        elif move.piece_captured == "bR": # if a black rook was captured
            if move.end_col == 0:  # left rook
                self.current_castling_rights.bqs = False # black can no longer castle queen-side
            elif move.end_col == 7:  # right rook
                self.current_castling_rights.bks = False # black can no longer castle king-side

        if move.piece_moved == 'wK': # if the white king moved
            self.current_castling_rights.wqs = False # white can no longer castle queen-side
            self.current_castling_rights.wks = False # white can no longer castle king-side
        elif move.piece_moved == 'bK': # if the black king moved
            self.current_castling_rights.bqs = False # black can no longer castle queen-side
            self.current_castling_rights.bks = False # black can no longer castle king-side
        elif move.piece_moved == 'wR': # if a white rook moved
            if move.start_row == 7: # if the white rook moved from the first row
                if move.start_col == 0:  # left rook
                    self.current_castling_rights.wqs = False # white can no longer castle queen-side
                elif move.start_col == 7:  # right rook
                    self.current_castling_rights.wks = False # white can no longer castle king-side
        elif move.piece_moved == 'bR': # if a black rook moved
            if move.start_row == 0: # if the black rook moved from the first row
                if move.start_col == 0:  # left rook
                    self.current_castling_rights.bqs = False # black can no longer castle queen-side
                elif move.start_col == 7:  # right rook
                    self.current_castling_rights.bks = False # black can no longer castle king-side

    def getValidMoves(self): # all moves considering checks
        """
        All moves considering checks.
        """
        temp_castle_rights = CastleRights(self.current_castling_rights.wks, self.current_castling_rights.bks,
                                          self.current_castling_rights.wqs, self.current_castling_rights.bqs) # copy the current castle rights
        # advanced algorithm
        moves = [] # list of moves
        self.in_check, self.pins, self.checks = self.checkForPinsAndChecks() # check for pins and checks

        if self.white_to_move:# if it is white's turn
            king_row = self.white_king_location[0] # get the row of the white king
            king_col = self.white_king_location[1] # get the column of the white king
        else:
            king_row = self.black_king_location[0] # get the row of the black king
            king_col = self.black_king_location[1] # get the column of the black king
        if self.in_check:
            if len(self.checks) == 1:  # only 1 check, block the check or move the king
                moves = self.getAllPossibleMoves()
                # to block the check you must put a piece into one of the squares between the enemy piece and your king
                check = self.checks[0]  # check information
                check_row = check[0] # get the row of the enemy piece checking the king
                check_col = check[1] # get the column of the enemy piece checking the king
                piece_checking = self.board[check_row][check_col]
                valid_squares = []  # squares that pieces can move to
                # if knight, must capture the knight or move your king, other pieces can be blocked
                if piece_checking[1] == "N": # if the piece checking the king is a knight
                    valid_squares = [(check_row, check_col)] # the only valid move is to capture the knight
                else: # if the piece checking the king is not a knight
                    for i in range(1, 8): # check for all squares between the king and the piece checking it
                        valid_square = (king_row + check[2] * i,
                                        king_col + check[3] * i)  # check[2] and check[3] are the check directions
                        valid_squares.append(valid_square) # add the valid square to the list of valid squares
                        if valid_square[0] == check_row and valid_square[
                            1] == check_col:  # once you get to piece and check
                            break # you are done, no more valid squares past this one
                # get rid of any moves that don't block check or move king
                for i in range(len(moves) - 1, -1, -1):  # iterate through the list backwards when removing elements
                    if moves[i].piece_moved[1] != "K":  # move doesn't move king so it must block or capture
                        if not (moves[i].end_row,
                                moves[i].end_col) in valid_squares:  # move doesn't block or capture piece
                            moves.remove(moves[i])
            else:  # double check, king has to move
                self.getKingMoves(king_row, king_col, moves)
        else:  # not in check - all moves are fine
            moves = self.getAllPossibleMoves() # get all the possible moves
            if self.white_to_move: # if it is white's turn
                self.getCastleMoves(self.white_king_location[0], self.white_king_location[1], moves) # get the castle moves for white
            else: 
                self.getCastleMoves(self.black_king_location[0], self.black_king_location[1], moves) # get the castle moves for black

        if len(moves) == 0: # either checkmate or stalemate
            if self.inCheck(): # if the player is in check
                self.checkmate = True # it is checkmate
            else: # if the player is not in check
                # TODO stalemate on repeated moves
                self.stalemate = True # it is stalemate 
        else:
            self.checkmate = False # it is not checkmate
            self.stalemate = False # it is not stalemate

        self.current_castling_rights = temp_castle_rights # update the castle rights
        return moves # return the list of moves

    def inCheck(self): # determine if a current player is in check
        """
        Determine if a current player is in check
        """
        if self.white_to_move: # if it is white's turn
            return self.squareUnderAttack(self.white_king_location[0], self.white_king_location[1]) # determine if enemy can attack the square row col
        else:
            return self.squareUnderAttack(self.black_king_location[0], self.black_king_location[1])     # determine if enemy can attack the square row col

    def squareUnderAttack(self, row, col): # determine if enemy can attack the square row col
        """
        Determine if enemy can attack the square row col
        """
        self.white_to_move = not self.white_to_move  # switch to opponent's point of view
        opponents_moves = self.getAllPossibleMoves() # get all the possible moves
        self.white_to_move = not self.white_to_move # switch turns back
        for move in opponents_moves: # for each move the opponent can make
            if move.end_row == row and move.end_col == col:  # square is under attack
                return True # square is under attack
        return False # square is not under attack

    def getAllPossibleMoves(self): # all moves without considering checks
        """
        All moves without considering checks.
        """
        moves = [] # list of moves
        for row in range(len(self.board)): # for each row in the board 
            for col in range(len(self.board[row])): # for each column in the board
                turn = self.board[row][col][0] # get the color of the piece
                if (turn == "w" and self.white_to_move) or (turn == "b" and not self.white_to_move): # if it is the current player's turn
                    piece = self.board[row][col][1] # get the type of the piece
                    self.moveFunctions[piece](row, col, moves)  # calls appropriate move function based on piece type
        return moves

    def checkForPinsAndChecks(self): # check for pins and checks
        pins = []  # squares pinned and the direction its pinned from
        checks = []  # squares where enemy is applying a check
        in_check = False
        if self.white_to_move: # if it is white's turn
            enemy_color = "b" # the enemy color
            ally_color = "w" # the ally color
            start_row = self.white_king_location[0] # the row of the white king
            start_col = self.white_king_location[1] # the column of the white king
        else: 
            enemy_color = "w" # the enemy color
            ally_color = "b" # the ally color
            start_row = self.black_king_location[0] # the row of the black king
            start_col = self.black_king_location[1]
        # check outwards from king for pins and checks, keep track of pins
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)) # the directions to check
        for j in range(len(directions)): # check each direction
            direction = directions[j] # get the direction
            possible_pin = ()  # reset possible pins
            for i in range(1, 8): # check 1 to 7 squares away
                end_row = start_row + direction[0] * i # the row of the square to check
                end_col = start_col + direction[1] * i # the column of the square to check
                if 0 <= end_row <= 7 and 0 <= end_col <= 7: # on board
                    end_piece = self.board[end_row][end_col] # the piece on the square
                    if end_piece[0] == ally_color and end_piece[1] != "K": # if the piece is an ally piece and not a king
                        if possible_pin == ():  # first allied piece could be pinned
                            possible_pin = (end_row, end_col, direction[0], direction[1])
                        else:  # 2nd allied piece - no check or pin from this direction
                            break
                    elif end_piece[0] == enemy_color:
                        enemy_type = end_piece[1]
                        # 5 possibilities in this complex conditional
                        # 1.) orthogonally away from king and piece is a rook
                        # 2.) diagonally away from king and piece is a bishop
                        # 3.) 1 square away diagonally from king and piece is a pawn
                        # 4.) any direction and piece is a queen
                        # 5.) any direction 1 square away and piece is a king
                        if (0 <= j <= 3 and enemy_type == "R") or (4 <= j <= 7 and enemy_type == "B") or (
                                i == 1 and enemy_type == "p" and (
                                (enemy_color == "w" and 6 <= j <= 7) or (enemy_color == "b" and 4 <= j <= 5))) or (
                                enemy_type == "Q") or (i == 1 and enemy_type == "K"):
                            if possible_pin == ():  # no piece blocking, so check
                                in_check = True
                                checks.append((end_row, end_col, direction[0], direction[1]))
                                break
                            else:  # piece blocking so pin
                                pins.append(possible_pin)
                                break
                        else:  # enemy piece not applying checks
                            break
                else:
                    break  # off board
        # check for knight checks
        knight_moves = ((-2, -1), (-2, 1), (-1, 2), (1, 2), (2, -1), (2, 1), (-1, -2), (1, -2)) # the knight moves to check for checks and pins
        for move in knight_moves: # check each knight move
            end_row = start_row + move[0] # the row of the square to check
            end_col = start_col + move[1] # the column of the square to check
            if 0 <= end_row <= 7 and 0 <= end_col <= 7: # on board
                end_piece = self.board[end_row][end_col] # the piece on the square
                if end_piece[0] == enemy_color and end_piece[1] == "N":  # enemy knight attacking a king
                    in_check = True # the king is in check
                    checks.append((end_row, end_col, move[0], move[1])) # add the check to the list of checks
        return in_check, pins, checks # return if the king is in check, the pins, and the checks

    def getPawnMoves(self, row, col, moves): # get the pawn moves
        """
        Get all the pawn moves for the pawn located at row, col and add the moves to the list.
        """
        piece_pinned = False # if the piece is pinned
        pin_direction = () # the direction of the pin
        for i in range(len(self.pins) - 1, -1, -1): # check if the piece is pinned
            if self.pins[i][0] == row and self.pins[i][1] == col: # if the piece is pinned
                piece_pinned = True # the piece is pinned
                pin_direction = (self.pins[i][2], self.pins[i][3]) # get the pin direction
                self.pins.remove(self.pins[i]) # remove the pinned piece
                break # there should only be one pinned piece so we can break

        if self.white_to_move: # if it is white's turn
            move_amount = -1 # the amount the pawn moves
            start_row = 6 # the starting row of the pawn
            enemy_color = "b" # the enemy color
            king_row, king_col = self.white_king_location # the location of the white king
        else:
            move_amount = 1 # the amount the pawn moves
            start_row = 1 # the starting row of the pawn
            enemy_color = "w" # the enemy color
            king_row, king_col = self.black_king_location # the location of the black king

        if self.board[row + move_amount][col] == "--":  # 1 square pawn advance
            if not piece_pinned or pin_direction == (move_amount, 0): # if the piece is not pinned or the direction is the same as the pin direction
                moves.append(Move((row, col), (row + move_amount, col), self.board)) # add the move to the list of moves
                if row == start_row and self.board[row + 2 * move_amount][col] == "--":  # 2 square pawn advance
                    moves.append(Move((row, col), (row + 2 * move_amount, col), self.board)) # add the move to the list of moves
        if col - 1 >= 0:  # capture to the left
            if not piece_pinned or pin_direction == (move_amount, -1): # if the piece is not pinned or the direction is the same as the pin direction
                if self.board[row + move_amount][col - 1][0] == enemy_color: # if the piece is an enemy piece
                    moves.append(Move((row, col), (row + move_amount, col - 1), self.board)) # add the move to the list of moves
                if (row + move_amount, col - 1) == self.enpassant_possible: # if the move is an en-passant
                    attacking_piece = blocking_piece = False # if the pawn is attacking or blocking
                    if king_row == row: # if the king is on the same row as the pawn
                        if king_col < col:  # king is left of the pawn
                            # inside: between king and the pawn;
                            # outside: between pawn and border;
                            inside_range = range(king_col + 1, col - 1) # the range of squares between the king and the pawn
                            outside_range = range(col + 1, 8) # the range of squares between the pawn and the border
                        else:  # king right of the pawn
                            inside_range = range(king_col - 1, col, -1) # the range of squares between the king and the pawn
                            outside_range = range(col - 2, -1, -1) # the range of squares between the pawn and the border
                        for i in inside_range: # check the inside range
                            if self.board[row][i] != "--":  # some piece beside en-passant pawn blocks
                                blocking_piece = True # the pawn is blocking
                        for i in outside_range: # check the outside range
                            square = self.board[row][i] # get the square
                            if square[0] == enemy_color and (square[1] == "R" or square[1] == "Q"): # if the square is an enemy rook or queen
                                attacking_piece = True # the pawn is attacking
                            elif square != "--": # if the square is not empty
                                blocking_piece = True # the pawn is blocking
                    if not attacking_piece or blocking_piece: # if the pawn is not attacking or blocking
                        moves.append(Move((row, col), (row + move_amount, col - 1), self.board, is_enpassant_move=True)) # add the move to the list of moves
        if col + 1 <= 7:  # capture to the right
            if not piece_pinned or pin_direction == (move_amount, +1): # if the piece is not pinned or the direction is the same as the pin direction
                if self.board[row + move_amount][col + 1][0] == enemy_color: # if the piece is an enemy piece
                    moves.append(Move((row, col), (row + move_amount, col + 1), self.board)) # add the move to the list of moves
                if (row + move_amount, col + 1) == self.enpassant_possible: # if the move is an en-passant
                    attacking_piece = blocking_piece = False # if the pawn is attacking or blocking
                    if king_row == row: # if the king is on the same row as the pawn
                        if king_col < col:  # king is left of the pawn
                            # inside: between king and the pawn;
                            # outside: between pawn and border;
                            inside_range = range(king_col + 1, col) # the range of squares between the king and the pawn
                            outside_range = range(col + 2, 8) # the range of squares between the pawn and the border
                        else:  # king right of the pawn
                            inside_range = range(king_col - 1, col + 1, -1) # the range of squares between the king and the pawn
                            outside_range = range(col - 1, -1, -1)
                        for i in inside_range:
                            if self.board[row][i] != "--":  # some piece beside en-passant pawn blocks
                                blocking_piece = True
                        for i in outside_range: # check the outside range
                            square = self.board[row][i] # get the square
                            if square[0] == enemy_color and (square[1] == "R" or square[1] == "Q"): # if the square is an enemy rook or queen
                                attacking_piece = True # the pawn is attacking
                            elif square != "--": # if the square is not empty
                                blocking_piece = True # the pawn is blocking
                    if not attacking_piece or blocking_piece: # if the pawn is not attacking or blocking
                        moves.append(Move((row, col), (row + move_amount, col + 1), self.board, is_enpassant_move=True))  # add the move to the list of moves 

    def getRookMoves(self, row, col, moves): # get the rook moves
        """
        Get all the rook moves for the rook located at row, col and add the moves to the list.
        """
        piece_pinned = False # if the piece is pinned
        pin_direction = () # the direction of the pin
        for i in range(len(self.pins) - 1, -1, -1): # check if the piece is pinned
            if self.pins[i][0] == row and self.pins[i][1] == col: # if the piece is pinned
                piece_pinned = True # the piece is pinned
                pin_direction = (self.pins[i][2], self.pins[i][3]) # get the pin direction
                if self.board[row][col][
                    1] != "Q":  # can't remove queen from pin on rook moves, only remove it on bishop moves
                    self.pins.remove(self.pins[i]) # remove the pinned piece
                break # there should only be one rook that is pinned so we can break

        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))  # up, left, down, right
        enemy_color = "b" if self.white_to_move else "w" # get the enemy color
        for direction in directions: # check all the directions
            for i in range(1, 8): # rooks can move max of 7 squares
                end_row = row + direction[0] * i # multiply by i to get the number of squares away
                end_col = col + direction[1] * i # multiply by i to get the number of squares away
                if 0 <= end_row <= 7 and 0 <= end_col <= 7:  # check for possible moves only in boundaries of the board
                    if not piece_pinned or pin_direction == direction or pin_direction == (
                            -direction[0], -direction[1]): # if the piece is not pinned or the direction is the same as the pin direction
                        end_piece = self.board[end_row][end_col] # get the piece on the end square
                        if end_piece == "--":  # empty space is valid
                            moves.append(Move((row, col), (end_row, end_col), self.board)) # add the move to the list of moves
                        elif end_piece[0] == enemy_color:  # capture enemy piece
                            moves.append(Move((row, col), (end_row, end_col), self.board)) # add the move to the list of moves
                            break
                        else:  # friendly piece
                            break
                else:  # off board
                    break

    def getKnightMoves(self, row, col, moves): # get the knight moves
        """
        Get all the knight moves for the knight located at row col and add the moves to the list.
        """
        piece_pinned = False # if the piece is pinned
        for i in range(len(self.pins) - 1, -1, -1): # check if the piece is pinned
            if self.pins[i][0] == row and self.pins[i][1] == col: # if the piece is pinned
                piece_pinned = True # the piece is pinned
                self.pins.remove(self.pins[i]) # remove the pinned piece
                break # there should only be one knight that is pinned so we can break

        knight_moves = ((-2, -1), (-2, 1), (-1, 2), (1, 2), (2, -1), (2, 1), (-1, -2),
                        (1, -2))  # up/left up/right right/up right/down down/left down/right left/up left/down
        ally_color = "w" if self.white_to_move else "b" # get the ally color
        for move in knight_moves: # check all the knight moves
            end_row = row + move[0] # get the end square
            end_col = col + move[1] # get the end square 
            if 0 <= end_row <= 7 and 0 <= end_col <= 7: # check for possible moves only in boundaries of the board
                if not piece_pinned: # if the piece is not pinned
                    end_piece = self.board[end_row][end_col] # get the piece on the end square
                    if end_piece[0] != ally_color:  # so its either enemy piece or empty square
                        moves.append(Move((row, col), (end_row, end_col), self.board)) # add the move to the list of moves

    def getBishopMoves(self, row, col, moves): # get the bishop moves
        """
        Get all the bishop moves for the bishop located at row col and add the moves to the list.
        """
        piece_pinned = False # if the piece is pinned
        pin_direction = () # the direction of the pin
        for i in range(len(self.pins) - 1, -1, -1): # check if the piece is pinned
            if self.pins[i][0] == row and self.pins[i][1] == col: # if the piece is pinned
                piece_pinned = True # the piece is pinned
                pin_direction = (self.pins[i][2], self.pins[i][3]) # get the pin direction
                self.pins.remove(self.pins[i]) # remove the pinned piece
                break # there should only be one bishop that is pinned so we can break

        directions = ((-1, -1), (-1, 1), (1, 1), (1, -1))  # diagonals: up/left up/right down/right down/left
        enemy_color = "b" if self.white_to_move else "w" # get the enemy color
        for direction in directions: # check all the directions
            for i in range(1, 8): # bishop can move max of 7 squares
                end_row = row + direction[0] * i # multiply by i to get the number of squares away
                end_col = col + direction[1] * i # multiply by i to get the number of squares away
                if 0 <= end_row <= 7 and 0 <= end_col <= 7:  # check if the move is on board
                    if not piece_pinned or pin_direction == direction or pin_direction == (
                            -direction[0], -direction[1]): # if the piece is not pinned or the direction is the same as the pin direction
                        end_piece = self.board[end_row][end_col] # get the piece on the end square
                        if end_piece == "--":  # empty space is valid
                            moves.append(Move((row, col), (end_row, end_col), self.board)) # add the move to the list of moves
                        elif end_piece[0] == enemy_color:  # capture enemy piece
                            moves.append(Move((row, col), (end_row, end_col), self.board)) # add the move to the list of moves
                            break
                        else:  # friendly piece
                            break
                else:  # off board
                    break

    def getQueenMoves(self, row, col, moves): # get the queen moves
        """
        Get all the queen moves for the queen located at row col and add the moves to the list.
        """
        self.getBishopMoves(row, col, moves) # get the bishop moves
        self.getRookMoves(row, col, moves) # get the rook moves

    def getKingMoves(self, row, col, moves): # get the king moves
        """
        Get all the king moves for the king located at row col and add the moves to the list.
        """
        row_moves = (-1, -1, -1, 0, 0, 1, 1, 1) # all the possible moves for the king
        col_moves = (-1, 0, 1, -1, 1, -1, 0, 1) # all the possible moves for the king
        ally_color = "w" if self.white_to_move else "b" # get the ally color
        for i in range(8): # check all 8 squares around the king
            end_row = row + row_moves[i] # get the end square
            end_col = col + col_moves[i] # get the end square
            if 0 <= end_row <= 7 and 0 <= end_col <= 7: # check if the move is on board
                end_piece = self.board[end_row][end_col] # get the piece on the end square
                if end_piece[0] != ally_color:  # not an ally piece - empty or enemy
                    # place king on end square and check for checks
                    if ally_color == "w":
                        self.white_king_location = (end_row, end_col) # place king on end square
                    else:
                        self.black_king_location = (end_row, end_col) # place king on end square
                    in_check, pins, checks = self.checkForPinsAndChecks() # check for pins and checks
                    if not in_check: # if the king is not in check
                        moves.append(Move((row, col), (end_row, end_col), self.board)) # add the move to the list of moves
                    # place king back on original location
                    if ally_color == "w": # if it is white's turn
                        self.white_king_location = (row, col) # place the king back to its original location
                    else: 
                        self.black_king_location = (row, col) # place the king back to its original location

    def getCastleMoves(self, row, col, moves): # get the castle moves
        """
        Generate all valid castle moves for the king at (row, col) and add them to the list of moves.
        """
        if self.squareUnderAttack(row, col): # if the king is in check
            return  # can't castle while in check
        if (self.white_to_move and self.current_castling_rights.wks) or (
                not self.white_to_move and self.current_castling_rights.bks): # king side castle
            self.getKingsideCastleMoves(row, col, moves) # get the kingside castle moves
        if (self.white_to_move and self.current_castling_rights.wqs) or (
                not self.white_to_move and self.current_castling_rights.bqs):# queen side castle
            self.getQueensideCastleMoves(row, col, moves) # get the queenside castle moves

    def getKingsideCastleMoves(self, row, col, moves): # get the kingside castle moves
        if self.board[row][col + 1] == '--' and self.board[row][col + 2] == '--': # if the squares between the king and the rook are empty
            if not self.squareUnderAttack(row, col + 1) and not self.squareUnderAttack(row, col + 2): # if the squares between the king and the rook are not under attack
                moves.append(Move((row, col), (row, col + 2), self.board, is_castle_move=True)) # add the kingside castle move to the list of moves

    def getQueensideCastleMoves(self, row, col, moves): # get the queenside castle moves
        if self.board[row][col - 1] == '--' and self.board[row][col - 2] == '--' and self.board[row][col - 3] == '--': # if the squares between the king and the rook are empty
            if not self.squareUnderAttack(row, col - 1) and not self.squareUnderAttack(row, col - 2): # if the squares between the king and the rook are not under attack
                moves.append(Move((row, col), (row, col - 2), self.board, is_castle_move=True)) # add the queenside castle move to the list of moves


class CastleRights: # class for the castle rights
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks # castle rights
        self.bks = bks # castle rights
        self.wqs = wqs # castle rights
        self.bqs = bqs # castle rights


class Move:
    # in chess, fields on the board are described by two symbols, one of them being number between 1-8 (which is corresponding to rows)
    # and the second one being a letter between a-f (corresponding to columns), in order to use this notation we need to map our [row][col] coordinates
    # to match the ones used in the original chess game
    ranks_to_rows = {"1": 7, "2": 6, "3": 5, "4": 4,
                     "5": 3, "6": 2, "7": 1, "8": 0} # ranks to rows
    rows_to_ranks = {v: k for k, v in ranks_to_rows.items()} # rows to ranks
    files_to_cols = {"a": 0, "b": 1, "c": 2, "d": 3,
                     "e": 4, "f": 5, "g": 6, "h": 7} # files to columns
    cols_to_files = {v: k for k, v in files_to_cols.items()} # columns to files

    def __init__(self, start_square, end_square, board, is_enpassant_move=False, is_castle_move=False): # constructor for the move class
        self.start_row = start_square[0] # start square     
        self.start_col = start_square[1] # start square
        self.end_row = end_square[0] # end square
        self.end_col = end_square[1] # end square
        self.piece_moved = board[self.start_row][self.start_col] # piece moved
        self.piece_captured = board[self.end_row][self.end_col] # piece captured
        # pawn promotion
        self.is_pawn_promotion = (self.piece_moved == "wp" and self.end_row == 0) or (
                self.piece_moved == "bp" and self.end_row == 7) # pawn promotion
        # en passant
        self.is_enpassant_move = is_enpassant_move # en passant move
        if self.is_enpassant_move: # if it is an en passant move
            self.piece_captured = "wp" if self.piece_moved == "bp" else "bp" # the piece captured is a pawn
        # castle move
        self.is_castle_move = is_castle_move # castle move

        self.is_capture = self.piece_captured != "--" # if a piece was captured
        self.moveID = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col # move id

    def __eq__(self, other): # overriding the equals method
        """
        Overriding the equals method.
        """
        if isinstance(other, Move): # if the other object is a move
            return self.moveID == other.moveID # return the move id
        return False # return false

    def getChessNotation(self): # get the chess notation for the move
        if self.is_pawn_promotion: # if it is a pawn promotion move 
            return self.getRankFile(self.end_row, self.end_col) + "Q" # return the rank file and the promotion piece
        if self.is_castle_move: # if it is a castle move
            if self.end_col == 1: # if it is a queen-side castle
                return "0-0-0" # return the queen-side castle
            else: # if it is a king-side castle
                return "0-0" # return the king-side castle
        if self.is_enpassant_move: # if it is an en passant move
            return self.getRankFile(self.start_row, self.start_col)[0] + "x" + self.getRankFile(self.end_row,
                                                                                                self.end_col) + " e.p." # return the en passant move
        if self.piece_captured != "--": # if a piece was captured 
            if self.piece_moved[1] == "p": # if the piece moved is a pawn
                return self.getRankFile(self.start_row, self.start_col)[0] + "x" + self.getRankFile(self.end_row,
                                                                                                    self.end_col) # pawn capture
            else:
                return self.piece_moved[1] + "x" + self.getRankFile(self.end_row, self.end_col) #
        else:
            if self.piece_moved[1] == "p": # if the piece moved is a pawn
                return self.getRankFile(self.end_row, self.end_col) # pawn move get rank file function 
            else:
                return self.piece_moved[1] + self.getRankFile(self.end_row, self.end_col) 
        # TODO Disambiguating moves

    def getRankFile(self, row, col): # get the rank file
        return self.cols_to_files[col] + self.rows_to_ranks[row] # return the rank file

    def __str__(self): # overriding the string method
        if self.is_castle_move:# if it is a castle move
            return "0-0" if self.end_col == 6 else "0-0-0" # return the castle move

        end_square = self.getRankFile(self.end_row, self.end_col) # get the end square

        if self.piece_moved[1] == "p": # if the piece moved is a pawn
            if self.is_capture: # if a piece was captured
                return self.cols_to_files[self.start_col] + "x" + end_square # pawn capture
            else:
                return end_square + "Q" if self.is_pawn_promotion else end_square # pawn promotion

        move_string = self.piece_moved[1] # get the piece moved
        if self.is_capture: # if a piece was captured
            move_string += "x" # capture move 
        return move_string + end_square # return the move string 
