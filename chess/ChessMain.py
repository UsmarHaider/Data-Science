# """
# Main driver file.
# Handling user input.
# Displaying current GameStatus object.
# """

# import pygame as p # using alias p for pygame
# import ChessEngine, ChessAI # importing ChessEngine.py and ChessAI.py
# import sys # importing sys
# from multiprocessing import Process, Queue # importing Process and Queue from multiprocessing

# BOARD_WIDTH = BOARD_HEIGHT = 512 # 400 is another option
# MOVE_LOG_PANEL_WIDTH = 250 
# MOVE_LOG_PANEL_HEIGHT = BOARD_HEIGHT 
# DIMENSION = 8 # dimensions of a chess board are 8x8
# SQUARE_SIZE = BOARD_HEIGHT // DIMENSION     
# MAX_FPS = 15
# IMAGES = {}

# # Initialize a global dictionary of images. This will be called exactly once in the main.
# def loadImages():
#     """
#     Initialize a global directory of images.
#     This will be called exactly once in the main.
#     """
#     pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ'] # list of pieces
#     for piece in pieces: # for loop to iterate through the list of pieces
#         IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQUARE_SIZE, SQUARE_SIZE)) # load the images and scale them to the square size


# def main(): # main function
#     """
#     The main driver for our code.
#     This will handle user input and updating the graphics.
#     """
#     p.init() # initialize pygame
#     screen = p.display.set_mode((BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH, BOARD_HEIGHT)) # set the screen size
#     clock = p.time.Clock() # set the clock for the game
#     screen.fill(p.Color("white")) # fill the screen with white color
#     game_state = ChessEngine.GameState() # create an instance of the GameState class
#     valid_moves = game_state.getValidMoves() # get the valid moves
#     move_made = False  # flag variable for when a move is made
#     animate = False  # flag variable for when we should animate a move
#     loadImages()  # do this only once before while loop
#     running = True
#     square_selected = ()  # no square is selected initially, this will keep track of the last click of the user (tuple(row,col))
#     player_clicks = []  # this will keep track of player clicks (two tuples)
#     game_over = False
#     ai_thinking = False
#     move_undone = False
#     move_finder_process = None
#     move_log_font = p.font.SysFont("Arial", 14, False, False)
#     player_one = True  # if a human is playing white, then this will be True, else False
#     player_two = False  # if a hyman is playing white, then this will be True, else False

#     while running: # while loop to run the game until the user quits
#         human_turn = (game_state.white_to_move and player_one) or (not game_state.white_to_move and player_two) # check if it is the human's turn
#         for e in p.event.get(): # for loop to iterate through the events
#             if e.type == p.QUIT: # if the user quits
#                 p.quit() # quit the game
#                 sys.exit()  # exit the program
#             # mouse handler
#             elif e.type == p.MOUSEBUTTONDOWN: # if the user clicks the mouse
#                 if not game_over: # if the game is not over
#                     location = p.mouse.get_pos()  # (x, y) location of the mouse
#                     col = location[0] // SQUARE_SIZE # get the column of the mouse click
#                     row = location[1] // SQUARE_SIZE # get the row and column of the mouse click
#                     if square_selected == (row, col) or col >= 8:  # user clicked the same square twice
#                         square_selected = ()  # deselect
#                         player_clicks = []  # clear clicks
#                     else: # if the user clicks a different square
#                         square_selected = (row, col) # select the square
#                         player_clicks.append(square_selected)  # append for both 1st and 2nd click
#                     if len(player_clicks) == 2 and human_turn:  # after 2nd click
#                         move = ChessEngine.Move(player_clicks[0], player_clicks[1], game_state.board) # create a move object using the player clicks
#                         for i in range(len(valid_moves)): # for loop to iterate through the valid moves
#                             if move == valid_moves[i]: # if the move is valid
#                                 game_state.makeMove(valid_moves[i]) # make the move on the board
#                                 move_made = True # set the move made flag to true
#                                 animate = True # set the animate flag to true
#                                 square_selected = ()  # reset user clicks
#                                 player_clicks = [] # reset user clicks
#                         if not move_made: # if the move is not valid
#                             player_clicks = [square_selected] # set the player clicks to the square selected

#             # key handler
#             elif e.type == p.KEYDOWN: # if the user presses a key
#                 if e.key == p.K_z:  # undo when 'z' is pressed
#                     game_state.undoMove() # undo the move
#                     move_made = True # set the move made flag to true
#                     animate = False # set the animate flag to false
#                     game_over = False # set the game over flag to false
#                     if ai_thinking: # if the AI is thinking
#                         move_finder_process.terminate() # terminate the move finder process
#                         ai_thinking = False # set the AI thinking flag to false
#                     move_undone = True # set the move undone flag to true
#                 if e.key == p.K_r:  # reset the game when 'r' is pressed
#                     game_state = ChessEngine.GameState() # create a new instance of the GameState class
#                     valid_moves = game_state.getValidMoves() # get the valid moves
#                     square_selected = () # reset the square selected
#                     player_clicks = [] # reset the player clicks
#                     move_made = False # set the move made flag to false
#                     animate = False # set the animate flag to false
#                     game_over = False # set the game over flag to false
#                     if ai_thinking: # if the AI is thinking
#                         move_finder_process.terminate() # terminate the move finder process
#                         ai_thinking = False # set the AI thinking flag to false
#                     move_undone = True # set the move undone flag to true

#         # AI move finder
#         if not game_over and not human_turn and not move_undone: # if the game is not over and it is not the human's turn and the move is not undone
#             if not ai_thinking: # if the AI is not thinking
#                 ai_thinking = True # set the AI thinking flag to true
#                 return_queue = Queue()  # used to pass data between threads
#                 move_finder_process = Process(target=ChessAI.findBestMove, args=(game_state, valid_moves, return_queue)) # create a process to find the best move
#                 move_finder_process.start() # start the process

#             if not move_finder_process.is_alive(): # if the move finder process is not alive
#                 ai_move = return_queue.get() # get the AI move
#                 if ai_move is None: # if the AI move is none
#                     ai_move = ChessAI.findRandomMove(valid_moves) # find a random move
#                 game_state.makeMove(ai_move) # make the AI move
#                 move_made = True # set the move made flag to true
#                 animate = True # set the animate flag to true
#                 ai_thinking = False # set the AI thinking flag to false

#         if move_made: # if the move is made
#             if animate: # if the animate flag is true
#                 animateMove(game_state.move_log[-1], screen, game_state.board, clock) # animate the move
#             valid_moves = game_state.getValidMoves() # get the valid moves
#             move_made = False # set the move made flag to false
#             animate = False # set the animate flag to false
#             move_undone = False # set the move undone flag to false

#         drawGameState(screen, game_state, valid_moves, square_selected) # draw the game state

#         if not game_over: # if the game is not over
#             drawMoveLog(screen, game_state, move_log_font) # draw the move log

#         if game_state.checkmate: # if the game is in checkmate
#             game_over = True # set the game over flag to true
#             if game_state.white_to_move: # if it is white's turn
#                 drawEndGameText(screen, "Black wins by checkmate") # draw the end game text
#             else:   
#                 drawEndGameText(screen, "White wins by checkmate") # draw the end game text

#         elif game_state.stalemate: # if the game is in stalemate
#             game_over = True # set the game over flag to true
#             drawEndGameText(screen, "Stalemate") # draw the end game text

#         clock.tick(MAX_FPS) # set the clock tick to the max fps
#         p.display.flip() # update the display


# def drawGameState(screen, game_state, valid_moves, square_selected): # draw the game state function
#     """
#     Responsible for all the graphics within current game state.
#     """
#     drawBoard(screen)  # draw squares on the board
#     highlightSquares(screen, game_state, valid_moves, square_selected)
#     drawPieces(screen, game_state.board)  # draw pieces on top of those squares


# def drawBoard(screen): # draw the board function
#     """
#     Draw the squares on the board.
#     The top left square is always light.
#     """
#     global colors # global variable for colors
#     colors = [p.Color("white"), p.Color("gray")] # colors for the board
#     for row in range(DIMENSION): # for loop to iterate through the rows
#         for column in range(DIMENSION): # for loop to iterate through the columns
#             color = colors[((row + column) % 2)] # get the color of the square
#             p.draw.rect(screen, color, p.Rect(column * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)) # draw the square


# def highlightSquares(screen, game_state, valid_moves, square_selected): # highlight the squares function
#     """
#     Highlight square selected and moves for piece selected.
#     """
#     if (len(game_state.move_log)) > 0: # if there is a move in the move log
#         last_move = game_state.move_log[-1] # get the last move
#         s = p.Surface((SQUARE_SIZE, SQUARE_SIZE)) # create a surface
#         s.set_alpha(100) # transparency value 0 -> transparent, 255 -> opaque
#         s.fill(p.Color('green')) # fill the surface with green color
#         screen.blit(s, (last_move.end_col * SQUARE_SIZE, last_move.end_row * SQUARE_SIZE)) # blit the surface
#     if square_selected != (): # if the square selected is not empty
#         row, col = square_selected # get the row and column of the square selected
#         if game_state.board[row][col][0] == (
#                 'w' if game_state.white_to_move else 'b'):  # square_selected is a piece that can be moved
#             # highlight selected square
#             s = p.Surface((SQUARE_SIZE, SQUARE_SIZE)) # create a surface
#             s.set_alpha(100)  # transparency value 0 -> transparent, 255 -> opaque
#             s.fill(p.Color('blue'))
#             screen.blit(s, (col * SQUARE_SIZE, row * SQUARE_SIZE)) # blit the surface
#             # highlight moves from that square
#             s.fill(p.Color('yellow')) # fill the surface with yellow color
#             for move in valid_moves: # for loop to iterate through the valid moves
#                 if move.start_row == row and move.start_col == col: # if the move start row and column is equal to the row and column of the square selected
#                     screen.blit(s, (move.end_col * SQUARE_SIZE, move.end_row * SQUARE_SIZE)) # blit the surface


# def drawPieces(screen, board): # draw the pieces function
#     """
#     Draw the pieces on the board using the current game_state.board
#     """
#     for row in range(DIMENSION): # for loop to iterate through the rows
#         for column in range(DIMENSION): # for loop to iterate through the columns
#             piece = board[row][column] # get the piece
#             if piece != "--": # if the piece is not empty
#                 screen.blit(IMAGES[piece], p.Rect(column * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)) # blit the piece


# def drawMoveLog(screen, game_state, font):  # draw the move log function
#     """
#     Draws the move log.

#     """
#     move_log_rect = p.Rect(BOARD_WIDTH, 0, MOVE_LOG_PANEL_WIDTH, MOVE_LOG_PANEL_HEIGHT) # create a rectangle for the move log
#     p.draw.rect(screen, p.Color('black'), move_log_rect) # draw the rectangle
#     move_log = game_state.move_log # get the move log
#     move_texts = [] # list of move texts
#     for i in range(0, len(move_log), 2):   # for loop to iterate through the move log
#         move_string = str(i // 2 + 1) + '. ' + str(move_log[i]) + " " # get the move string
#         if i + 1 < len(move_log): # if the index is less than the length of the move log
#             move_string += str(move_log[i + 1]) + "  " # get the move string
#         move_texts.append(move_string) # append the move string to the move texts

#     moves_per_row = 3 # moves per row
#     padding = 5 # padding for the move log
#     line_spacing = 2 # line spacing for the move log
#     text_y = padding # text y for the move log
#     for i in range(0, len(move_texts), moves_per_row): # for loop to iterate through the move texts
#         text = "" # text for the move log
#         for j in range(moves_per_row): # for loop to iterate through the moves per row
#             if i + j < len(move_texts): # if the index is less than the length of the move texts
#                 text += move_texts[i + j] # get the move text

#         text_object = font.render(text, True, p.Color('white')) # render the text
#         text_location = move_log_rect.move(padding, text_y) # get the text location
#         screen.blit(text_object, text_location) # blit the text
#         text_y += text_object.get_height() + line_spacing # get the text y


# def drawEndGameText(screen, text): # draw the end game text function 
#     font = p.font.SysFont("Helvetica", 32, True, False) # set the font for the end game text
#     text_object = font.render(text, False, p.Color("gray")) # render the text object
#     text_location = p.Rect(0, 0, BOARD_WIDTH, BOARD_HEIGHT).move(BOARD_WIDTH / 2 - text_object.get_width() / 2,
#                                                                  BOARD_HEIGHT / 2 - text_object.get_height() / 2) # get the text location
#     screen.blit(text_object, text_location) # blit the text
#     text_object = font.render(text, False, p.Color('black')) # render the text object
#     screen.blit(text_object, text_location.move(2, 2)) # blit the text


# def animateMove(move, screen, board, clock): # animate the move function
#     """
#     Animating a move
#     """
#     global colors
#     d_row = move.end_row - move.start_row # get the row and column of the piece moved
#     d_col = move.end_col - move.start_col # get the row and column of the piece moved
#     frames_per_square = 10  # frames to move one square
#     frame_count = (abs(d_row) + abs(d_col)) * frames_per_square # get the frame count for the move
#     for frame in range(frame_count + 1): # for loop to iterate through the frames
#         row, col = (move.start_row + d_row * frame / frame_count, move.start_col + d_col * frame / frame_count) # get the row and column of the piece
#         drawBoard(screen) # draw squares on the board 
#         drawPieces(screen, board) # draw pieces in current location
#         # erase the piece moved from its ending square
#         color = colors[(move.end_row + move.end_col) % 2] # get the color of the square
#         end_square = p.Rect(move.end_col * SQUARE_SIZE, move.end_row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE) # get the end square
#         p.draw.rect(screen, color, end_square)  # draw a rectangle on top of the piece moved
#         # draw captured piece onto rectangle
#         if move.piece_captured != '--': # if the piece captured is not empty
#             if move.is_enpassant_move: # if it is an enpassant move
#                 enpassant_row = move.end_row + 1 if move.piece_captured[0] == 'b' else move.end_row - 1 # get the enpassant row
#                 end_square = p.Rect(move.end_col * SQUARE_SIZE, enpassant_row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE) # get the end square
#             screen.blit(IMAGES[move.piece_captured], end_square) # blit the captured piece
#         # draw moving piece
#         screen.blit(IMAGES[move.piece_moved], p.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)) # blit the moving piece
#         p.display.flip() # update the display
#         clock.tick(60) # set the clock tick to 60


# if __name__ == "__main__": # if the name is main
#     main() # call the main function








# //////////////////////////////////////////////////////////////////////////////////

# import random

# # Define the Python quiz questions and answers
# python_quiz = [
#     {
#         "question": "What is the output of the following code?\n\nprint(2 + 2 * 3)",
#         "options": ["4", "8", "10", "14"],
#         "answer": "8"
#     },
#     {
#         "question": "Which of the following is an immutable data type in Python?",
#         "options": ["List", "Tuple", "Dictionary", "Set"],
#         "answer": "Tuple"
#     },
#     {
#         "question": "What is the correct way to open and read a file in Python?",
#         "options": ["open('file.txt', 'r')", "open('file.txt', 'w')", "open('file.txt', 'a')", "open('file.txt', 'x')"],
#         "answer": "open('file.txt', 'r')"
#     },
#     {
#         "question": "What is the output of the following code?\n\nprint(len([1, 2, 3, 4, 5]))",
#         "options": ["1", "2", "3", "5"],
#         "answer": "5"
#     }
# ]

# # Function to ask the Python quiz questions
# def ask_python_questions():
#     score = 0
#     random.shuffle(python_quiz)
    
#     for question in python_quiz:
#         print(question["question"])
#         for index, option in enumerate(question["options"]):
#             print(f"{index+1}. {option}")
        
#         user_answer = input("Enter the number corresponding to your answer: ")
#         selected_option = question["options"][int(user_answer) - 1]
        
#         if selected_option == question["answer"]:
#             print("Correct answer!")
#             score += 1
#         else:
#             print(f"Wrong answer! The correct answer is: {question['answer']}")
        
#         print()
    
#     print(f"You scored {score} out of {len(python_quiz)} in the Python quiz.\n")
#     return score


# # Main game function
# def play_chess():
#     # Ask Python quiz questions
#     python_score = ask_python_questions()
    
#     # Continue with the chess game if the user scored at least 2 points in the Python quiz
#     if python_score >= 2:
#         print("Starting the chess game...")
        
#     else:
#         print("Sorry, you need to score at least 2 points in the Python quiz to play the chess game.")


# # Start the game
# play_chess()

# ////////////////////////////////////////////////////////////////////////////////////////


import random

# Define the Python quiz questions and answers
python_quiz = [
    {
        "question": "What is the output of the following code?\n\nprint(2 + 2 * 3)",
        "options": ["4", "8", "10", "14"],
        "answer": "8"
    },
    {
        "question": "Which of the following is an immutable data type in Python?",
        "options": ["List", "Tuple", "Dictionary", "Set"],
        "answer": "Tuple"
    },
    {
        "question": "What is the correct way to open and read a file in Python?",
        "options": ["open('file.txt', 'r')", "open('file.txt', 'w')", "open('file.txt', 'a')", "open('file.txt', 'x')"],
        "answer": "open('file.txt', 'r')"
    },
    {
        "question": "What is the output of the following code?\n\nprint(len([1, 2, 3, 4, 5]))",
        "options": ["1", "2", "3", "5"],
        "answer": "5"
    }
]

# Function to ask the Python quiz questions
def ask_python_questions():
    score = 0
    random.shuffle(python_quiz)
    
    for question in python_quiz:
        print(question["question"])
        for index, option in enumerate(question["options"]):
            print(f"{index+1}. {option}")
        
        user_answer = input("Enter the number corresponding to your answer: ")
        selected_option = question["options"][int(user_answer) - 1]
        
        if selected_option == question["answer"]:
            print("Correct answer!")
            score += 1
        else:
            print(f"Wrong answer! The correct answer is: {question['answer']}")
        
        print()
    
    print(f"You scored {score} out of {len(python_quiz)} in the Python quiz.\n")
    return score



# Main game function
def main():
    
    # Ask Python quiz questions
    python_score = ask_python_questions()
    
    # Continue with the chess game if the user scored at least 2 points in the Python quiz
    if python_score >= 2:
        print("Starting the chess game...")
        playchess()
    else:
        print("Sorry, you need to score at least 2 points in the Python quiz to play the chess game.")



"""
Main driver file.
Handling user input.
Displaying current GameStatus object.
"""

import pygame as p # using alias p for pygame
import ChessEngine, ChessAI # importing ChessEngine.py and ChessAI.py
import sys # importing sys
from multiprocessing import Process, Queue # importing Process and Queue from multiprocessing

BOARD_WIDTH = BOARD_HEIGHT = 512 # 400 is another option
MOVE_LOG_PANEL_WIDTH = 250 
MOVE_LOG_PANEL_HEIGHT = BOARD_HEIGHT 
DIMENSION = 8 # dimensions of a chess board are 8x8
SQUARE_SIZE = BOARD_HEIGHT // DIMENSION     
MAX_FPS = 15
IMAGES = {}

# Initialize a global dictionary of images. This will be called exactly once in the main.
def loadImages():
    """
    Initialize a global directory of images.
    This will be called exactly once in the main.
    """
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ'] # list of pieces
    for piece in pieces: # for loop to iterate through the list of pieces
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQUARE_SIZE, SQUARE_SIZE)) # load the images and scale them to the square size


def playchess(): # main function
    """
    The main driver for our code.
    This will handle user input and updating the graphics.
    """
    p.init() # initialize pygame
    screen = p.display.set_mode((BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH, BOARD_HEIGHT)) # set the screen size
    clock = p.time.Clock() # set the clock for the game
    screen.fill(p.Color("white")) # fill the screen with white color
    game_state = ChessEngine.GameState() # create an instance of the GameState class
    valid_moves = game_state.getValidMoves() # get the valid moves
    move_made = False  # flag variable for when a move is made
    animate = False  # flag variable for when we should animate a move
    loadImages()  # do this only once before while loop
    running = True
    square_selected = ()  # no square is selected initially, this will keep track of the last click of the user (tuple(row,col))
    player_clicks = []  # this will keep track of player clicks (two tuples)
    game_over = False
    ai_thinking = False
    move_undone = False
    move_finder_process = None
    move_log_font = p.font.SysFont("Arial", 14, False, False)
    player_one = True  # if a human is playing white, then this will be True, else False
    player_two = False  # if a hyman is playing white, then this will be True, else False

    while running: # while loop to run the game until the user quits
        human_turn = (game_state.white_to_move and player_one) or (not game_state.white_to_move and player_two) # check if it is the human's turn
        for e in p.event.get(): # for loop to iterate through the events
            if e.type == p.QUIT: # if the user quits
                p.quit() # quit the game
                sys.exit()  # exit the program
            # mouse handler
            elif e.type == p.MOUSEBUTTONDOWN: # if the user clicks the mouse
                if not game_over: # if the game is not over
                    location = p.mouse.get_pos()  # (x, y) location of the mouse
                    col = location[0] // SQUARE_SIZE # get the column of the mouse click
                    row = location[1] // SQUARE_SIZE # get the row and column of the mouse click
                    if square_selected == (row, col) or col >= 8:  # user clicked the same square twice
                        square_selected = ()  # deselect
                        player_clicks = []  # clear clicks
                    else: # if the user clicks a different square
                        square_selected = (row, col) # select the square
                        player_clicks.append(square_selected)  # append for both 1st and 2nd click
                    if len(player_clicks) == 2 and human_turn:  # after 2nd click
                        move = ChessEngine.Move(player_clicks[0], player_clicks[1], game_state.board) # create a move object using the player clicks
                        for i in range(len(valid_moves)): # for loop to iterate through the valid moves
                            if move == valid_moves[i]: # if the move is valid
                                game_state.makeMove(valid_moves[i]) # make the move on the board
                                move_made = True # set the move made flag to true
                                animate = True # set the animate flag to true
                                square_selected = ()  # reset user clicks
                                player_clicks = [] # reset user clicks
                        if not move_made: # if the move is not valid
                            player_clicks = [square_selected] # set the player clicks to the square selected

            # key handler
            elif e.type == p.KEYDOWN: # if the user presses a key
                if e.key == p.K_z:  # undo when 'z' is pressed
                    game_state.undoMove() # undo the move
                    move_made = True # set the move made flag to true
                    animate = False # set the animate flag to false
                    game_over = False # set the game over flag to false
                    if ai_thinking: # if the AI is thinking
                        move_finder_process.terminate() # terminate the move finder process
                        ai_thinking = False # set the AI thinking flag to false
                    move_undone = True # set the move undone flag to true
                if e.key == p.K_r:  # reset the game when 'r' is pressed
                    game_state = ChessEngine.GameState() # create a new instance of the GameState class
                    valid_moves = game_state.getValidMoves() # get the valid moves
                    square_selected = () # reset the square selected
                    player_clicks = [] # reset the player clicks
                    move_made = False # set the move made flag to false
                    animate = False # set the animate flag to false
                    game_over = False # set the game over flag to false
                    if ai_thinking: # if the AI is thinking
                        move_finder_process.terminate() # terminate the move finder process
                        ai_thinking = False # set the AI thinking flag to false
                    move_undone = True # set the move undone flag to true

        # AI move finder
        if not game_over and not human_turn and not move_undone: # if the game is not over and it is not the human's turn and the move is not undone
            if not ai_thinking: # if the AI is not thinking
                ai_thinking = True # set the AI thinking flag to true
                return_queue = Queue()  # used to pass data between threads
                move_finder_process = Process(target=ChessAI.findBestMove, args=(game_state, valid_moves, return_queue)) # create a process to find the best move
                move_finder_process.start() # start the process

            if not move_finder_process.is_alive(): # if the move finder process is not alive
                ai_move = return_queue.get() # get the AI move
                if ai_move is None: # if the AI move is none
                    ai_move = ChessAI.findRandomMove(valid_moves) # find a random move
                game_state.makeMove(ai_move) # make the AI move
                move_made = True # set the move made flag to true
                animate = True # set the animate flag to true
                ai_thinking = False # set the AI thinking flag to false

        if move_made: # if the move is made
            if animate: # if the animate flag is true
                animateMove(game_state.move_log[-1], screen, game_state.board, clock) # animate the move
            valid_moves = game_state.getValidMoves() # get the valid moves
            move_made = False # set the move made flag to false
            animate = False # set the animate flag to false
            move_undone = False # set the move undone flag to false

        drawGameState(screen, game_state, valid_moves, square_selected) # draw the game state

        if not game_over: # if the game is not over
            drawMoveLog(screen, game_state, move_log_font) # draw the move log

        if game_state.checkmate: # if the game is in checkmate
            game_over = True # set the game over flag to true
            if game_state.white_to_move: # if it is white's turn
                drawEndGameText(screen, "Black wins by checkmate") # draw the end game text
            else:   
                drawEndGameText(screen, "White wins by checkmate") # draw the end game text

        elif game_state.stalemate: # if the game is in stalemate
            game_over = True # set the game over flag to true
            drawEndGameText(screen, "Stalemate") # draw the end game text

        clock.tick(MAX_FPS) # set the clock tick to the max fps
        p.display.flip() # update the display


def drawGameState(screen, game_state, valid_moves, square_selected): # draw the game state function
    """
    Responsible for all the graphics within current game state.
    """
    drawBoard(screen)  # draw squares on the board
    highlightSquares(screen, game_state, valid_moves, square_selected)
    drawPieces(screen, game_state.board)  # draw pieces on top of those squares


def drawBoard(screen): # draw the board function
    """
    Draw the squares on the board.
    The top left square is always light.
    """
    global colors # global variable for colors
    colors = [p.Color("white"), p.Color("gray")] # colors for the board
    for row in range(DIMENSION): # for loop to iterate through the rows
        for column in range(DIMENSION): # for loop to iterate through the columns
            color = colors[((row + column) % 2)] # get the color of the square
            p.draw.rect(screen, color, p.Rect(column * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)) # draw the square


def highlightSquares(screen, game_state, valid_moves, square_selected): # highlight the squares function
    """
    Highlight square selected and moves for piece selected.
    """
    if (len(game_state.move_log)) > 0: # if there is a move in the move log
        last_move = game_state.move_log[-1] # get the last move
        s = p.Surface((SQUARE_SIZE, SQUARE_SIZE)) # create a surface
        s.set_alpha(100) # transparency value 0 -> transparent, 255 -> opaque
        s.fill(p.Color('green')) # fill the surface with green color
        screen.blit(s, (last_move.end_col * SQUARE_SIZE, last_move.end_row * SQUARE_SIZE)) # blit the surface
    if square_selected != (): # if the square selected is not empty
        row, col = square_selected # get the row and column of the square selected
        if game_state.board[row][col][0] == (
                'w' if game_state.white_to_move else 'b'):  # square_selected is a piece that can be moved
            # highlight selected square
            s = p.Surface((SQUARE_SIZE, SQUARE_SIZE)) # create a surface
            s.set_alpha(100)  # transparency value 0 -> transparent, 255 -> opaque
            s.fill(p.Color('blue'))
            screen.blit(s, (col * SQUARE_SIZE, row * SQUARE_SIZE)) # blit the surface
            # highlight moves from that square
            s.fill(p.Color('yellow')) # fill the surface with yellow color
            for move in valid_moves: # for loop to iterate through the valid moves
                if move.start_row == row and move.start_col == col: # if the move start row and column is equal to the row and column of the square selected
                    screen.blit(s, (move.end_col * SQUARE_SIZE, move.end_row * SQUARE_SIZE)) # blit the surface


def drawPieces(screen, board): # draw the pieces function
    """
    Draw the pieces on the board using the current game_state.board
    """
    for row in range(DIMENSION): # for loop to iterate through the rows
        for column in range(DIMENSION): # for loop to iterate through the columns
            piece = board[row][column] # get the piece
            if piece != "--": # if the piece is not empty
                screen.blit(IMAGES[piece], p.Rect(column * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)) # blit the piece


def drawMoveLog(screen, game_state, font):  # draw the move log function
    """
    Draws the move log.

    """
    move_log_rect = p.Rect(BOARD_WIDTH, 0, MOVE_LOG_PANEL_WIDTH, MOVE_LOG_PANEL_HEIGHT) # create a rectangle for the move log
    p.draw.rect(screen, p.Color('black'), move_log_rect) # draw the rectangle
    move_log = game_state.move_log # get the move log
    move_texts = [] # list of move texts
    for i in range(0, len(move_log), 2):   # for loop to iterate through the move log
        move_string = str(i // 2 + 1) + '. ' + str(move_log[i]) + " " # get the move string
        if i + 1 < len(move_log): # if the index is less than the length of the move log
            move_string += str(move_log[i + 1]) + "  " # get the move string
        move_texts.append(move_string) # append the move string to the move texts

    moves_per_row = 3 # moves per row
    padding = 5 # padding for the move log
    line_spacing = 2 # line spacing for the move log
    text_y = padding # text y for the move log
    for i in range(0, len(move_texts), moves_per_row): # for loop to iterate through the move texts
        text = "" # text for the move log
        for j in range(moves_per_row): # for loop to iterate through the moves per row
            if i + j < len(move_texts): # if the index is less than the length of the move texts
                text += move_texts[i + j] # get the move text

        text_object = font.render(text, True, p.Color('white')) # render the text
        text_location = move_log_rect.move(padding, text_y) # get the text location
        screen.blit(text_object, text_location) # blit the text
        text_y += text_object.get_height() + line_spacing # get the text y


def drawEndGameText(screen, text): # draw the end game text function 
    font = p.font.SysFont("Helvetica", 32, True, False) # set the font for the end game text
    text_object = font.render(text, False, p.Color("gray")) # render the text object
    text_location = p.Rect(0, 0, BOARD_WIDTH, BOARD_HEIGHT).move(BOARD_WIDTH / 2 - text_object.get_width() / 2,
                                                                 BOARD_HEIGHT / 2 - text_object.get_height() / 2) # get the text location
    screen.blit(text_object, text_location) # blit the text
    text_object = font.render(text, False, p.Color('black')) # render the text object
    screen.blit(text_object, text_location.move(2, 2)) # blit the text


def animateMove(move, screen, board, clock): # animate the move function
    """
    Animating a move
    """
    global colors
    d_row = move.end_row - move.start_row # get the row and column of the piece moved
    d_col = move.end_col - move.start_col # get the row and column of the piece moved
    frames_per_square = 10  # frames to move one square
    frame_count = (abs(d_row) + abs(d_col)) * frames_per_square # get the frame count for the move
    for frame in range(frame_count + 1): # for loop to iterate through the frames
        row, col = (move.start_row + d_row * frame / frame_count, move.start_col + d_col * frame / frame_count) # get the row and column of the piece
        drawBoard(screen) # draw squares on the board 
        drawPieces(screen, board) # draw pieces in current location
        # erase the piece moved from its ending square
        color = colors[(move.end_row + move.end_col) % 2] # get the color of the square
        end_square = p.Rect(move.end_col * SQUARE_SIZE, move.end_row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE) # get the end square
        p.draw.rect(screen, color, end_square)  # draw a rectangle on top of the piece moved
        # draw captured piece onto rectangle
        if move.piece_captured != '--': # if the piece captured is not empty
            if move.is_enpassant_move: # if it is an enpassant move
                enpassant_row = move.end_row + 1 if move.piece_captured[0] == 'b' else move.end_row - 1 # get the enpassant row
                end_square = p.Rect(move.end_col * SQUARE_SIZE, enpassant_row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE) # get the end square
            screen.blit(IMAGES[move.piece_captured], end_square) # blit the captured piece
        # draw moving piece
        screen.blit(IMAGES[move.piece_moved], p.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)) # blit the moving piece
        p.display.flip() # update the display
        clock.tick(60) # set the clock tick to 60


if __name__ == "__main__": # if the name is main
    main() # call the main function






