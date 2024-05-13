#MonaTechnology
import pygame
import sys
import random
from pygame.locals import *

# cette section contient toutes les variables que nous utiliserons dans Puzzle Game In Python
w_of_board = 4 
h_of_board = 4  
block_size = 80
win_width = 640
win_height = 480
FPS = 30
BLANK = None

# c'est essentiellement pour gérer les différentes couleurs du composant
# nous avons également utilisé des variables pour maintenir la taille du texte dans Puzzle Game In Python
BLACK = (5,   24,   31)
WHITE = (255, 255, 255)
BRIGHTBLUE = (0,  50, 255)
DARKTURQUOISE = (255, 255, 255)
BLUE = (53,  81, 92)
GREEN = (50, 98,   2)
RED = (94, 67, 67)
BGCOLOR = DARKTURQUOISE
TILECOLOR = BLUE
TEXTCOLOR = WHITE
BORDERCOLOR = RED
BASICFONTSIZE = 15
TEXT = GREEN

BUTTONCOLOR = WHITE
BUTTONTEXTCOLOR = BLACK
MESSAGECOLOR = GREEN

# il s'agit de laisser de l'espace des deux côtés du bloc
XMARGIN = int((win_width - (block_size * w_of_board + (w_of_board - 1))) / 2)
YMARGIN = int((win_height - (block_size * h_of_board + (h_of_board - 1))) / 2)

# ce sont les variables de gestion des touches du clavier
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'



def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, RESET_SURF, RESET_RECT, NEW_SURF, NEW_RECT, SOLVE_SURF, SOLVE_RECT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((win_width, win_height))
    # nous avons donné un titre en utilisant la fonction set_caption dans pygame
    pygame.display.set_caption('Mona Technology Slide Puzzle')
    BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)

    # ces variables stockent les différentes options qui seront affichées sur le côté droit de notre grille principale
    # ceux-ci ci-dessous ne traitent que la partie conception des options
    RESET_SURF, RESET_RECT = makeText(
        'Reinitialiser',    TEXT, BGCOLOR, win_width - 120, win_height - 310)
    NEW_SURF,   NEW_RECT = makeText(
        'Nouveau Jeu', TEXT, BGCOLOR, win_width - 120, win_height - 280)
    SOLVE_SURF, SOLVE_RECT = makeText(
        'Resoudre',    TEXT, BGCOLOR, win_width - 120, win_height - 250)

    mainBoard, solutionSeq = generateNewPuzzle(80)
    
    SOLVEDBOARD = start_playing()
    
    allMoves = []
    
    while True:
        slideTo = None
        msg = 'Cliquez sur un bloc ou appuyez sur les touches flechees pour faire glisser le bloc.'
        if mainBoard == SOLVEDBOARD:
            msg = 'Resolu!'

        drawBoard(mainBoard, msg)
        check_exit_req()
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                spotx, spoty = getSpotClicked(
                    mainBoard, event.pos[0], event.pos[1])

                if (spotx, spoty) == (None, None):
                    # this is to check if the user clicked on an option button
                    if RESET_RECT.collidepoint(event.pos):
                        # this below linw will come into action of the user clicked on Reset button
                        rst_animation(mainBoard, allMoves)
                        allMoves = []
                    elif NEW_RECT.collidepoint(event.pos):
                        # this below linw will come into action of the user clicked on New Game button
                        mainBoard, solutionSeq = generateNewPuzzle(80)
                        allMoves = []
                    elif SOLVE_RECT.collidepoint(event.pos):
                        # this below linw will come into action of the user clicked on Solve button
                        rst_animation(mainBoard, solutionSeq + allMoves)
                        allMoves = []
                else:
                    # this else block in Puzzle Game In Python is just to check that the moved tile has a blank
                    blankx, blanky = getBlankPosition(mainBoard)
                    if spotx == blankx + 1 and spoty == blanky:
                        slideTo = LEFT
                    elif spotx == blankx - 1 and spoty == blanky:
                        slideTo = RIGHT
                    elif spotx == blankx and spoty == blanky + 1:
                        slideTo = UP
                    elif spotx == blankx and spoty == blanky - 1:
                        slideTo = DOWN

            elif event.type == KEYUP:
                # this elif block will handle the checking if the user pressed a key to slide a tile
                if event.key in (K_LEFT, K_a) and isValidMove(mainBoard, LEFT):
                    slideTo = LEFT
                elif event.key in (K_RIGHT, K_d) and isValidMove(mainBoard, RIGHT):
                    slideTo = RIGHT
                elif event.key in (K_UP, K_w) and isValidMove(mainBoard, UP):
                    slideTo = UP
                elif event.key in (K_DOWN, K_s) and isValidMove(mainBoard, DOWN):
                    slideTo = DOWN
        # this block will handle the fucntionality of displaying the message for controls
        if slideTo:
            # show slide on screen
            sliding_animation(
                mainBoard, slideTo, 'Cliquez sur un bloc ou appuyez sur les touches flechees pour faire glisser le bloc.', 8)
            take_turn(mainBoard, slideTo)
            allMoves.append(slideTo)
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def terminate():
    pygame.quit()
    sys.exit()


def check_exit_req():
    
    for event in pygame.event.get(QUIT):
        
        terminate()
    
    for event in pygame.event.get(KEYUP):
        if event.key == K_ESCAPE:  
            terminate()
        pygame.event.post(event)


def start_playing():
    
    counter = 1
    board = []
    for x in range(w_of_board):
        column = []
        for y in range(h_of_board):
            column.append(counter)
            counter += w_of_board
        board.append(column)
        counter -= w_of_board * (h_of_board - 1) + w_of_board - 1

    board[w_of_board-1][h_of_board-1] = BLANK
    return board


def getBlankPosition(board):
    for x in range(w_of_board):
        for y in range(h_of_board):
            if board[x][y] == BLANK:
                return (x, y)


def take_turn(board, move):
    blankx, blanky = getBlankPosition(board)

    if move == UP:
        board[blankx][blanky], board[blankx][blanky +
                                             1] = board[blankx][blanky + 1], board[blankx][blanky]
    elif move == DOWN:
        board[blankx][blanky], board[blankx][blanky -
                                             1] = board[blankx][blanky - 1], board[blankx][blanky]
    elif move == LEFT:
        board[blankx][blanky], board[blankx +
                                     1][blanky] = board[blankx + 1][blanky], board[blankx][blanky]
    elif move == RIGHT:
        board[blankx][blanky], board[blankx -
                                     1][blanky] = board[blankx - 1][blanky], board[blankx][blanky]


def isValidMove(board, move):
    blankx, blanky = getBlankPosition(board)
    return (move == UP and blanky != len(board[0]) - 1) or \
           (move == DOWN and blanky != 0) or \
           (move == LEFT and blankx != len(board) - 1) or \
           (move == RIGHT and blankx != 0)


def ramdom_moves(board, lastMove=None):
    
    validMoves = [UP, DOWN, LEFT, RIGHT]

    if lastMove == UP or not isValidMove(board, DOWN):
        validMoves.remove(DOWN)
    if lastMove == DOWN or not isValidMove(board, UP):
        validMoves.remove(UP)
    if lastMove == LEFT or not isValidMove(board, RIGHT):
        validMoves.remove(RIGHT)
    if lastMove == RIGHT or not isValidMove(board, LEFT):
        validMoves.remove(LEFT)
    return random.choice(validMoves)


def getLeftTopOfTile(block_x, block_y):
    left = XMARGIN + (block_x * block_size) + (block_x - 1)
    top = YMARGIN + (block_y * block_size) + (block_y - 1)
    return (left, top)


def getSpotClicked(board, x, y):
    for block_x in range(len(board)):
        for block_y in range(len(board[0])):
            left, top = getLeftTopOfTile(block_x, block_y)
            tileRect = pygame.Rect(left, top, block_size, block_size)
            if tileRect.collidepoint(x, y):
                return (block_x, block_y)
    return (None, None)


def draw_block(block_x, block_y, number, adjx=0, adjy=0):
    left, top = getLeftTopOfTile(block_x, block_y)
    pygame.draw.rect(DISPLAYSURF, TILECOLOR, (left + adjx,
                     top + adjy, block_size, block_size))
    text_renderign = BASICFONT.render(str(number), True, TEXTCOLOR)
    text_in_rect = text_renderign.get_rect()
    text_in_rect.center = left + \
        int(block_size / 2) + adjx, top + int(block_size / 2) + adjy
    DISPLAYSURF.blit(text_renderign, text_in_rect)


def makeText(text, color, bgcolor, top, left):
    text_renderign = BASICFONT.render(text, True, color, bgcolor)
    text_in_rect = text_renderign.get_rect()
    text_in_rect.topleft = (top, left)
    return (text_renderign, text_in_rect)

def drawBoard(board, message):
    DISPLAYSURF.fill(BGCOLOR)
    if message:
        text_renderign, text_in_rect = makeText(
            message, MESSAGECOLOR, BGCOLOR, 5, 5)
        DISPLAYSURF.blit(text_renderign, text_in_rect)

    for block_x in range(len(board)):
        for block_y in range(len(board[0])):
            if board[block_x][block_y]:
                draw_block(block_x, block_y, board[block_x][block_y])

    left, top = getLeftTopOfTile(0, 0)
    width = w_of_board * block_size
    height = h_of_board * block_size
    pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (left - 5,
                     top - 5, width + 11, height + 11), 4)

    DISPLAYSURF.blit(RESET_SURF, RESET_RECT)
    DISPLAYSURF.blit(NEW_SURF, NEW_RECT)
    DISPLAYSURF.blit(SOLVE_SURF, SOLVE_RECT)

def sliding_animation(board, direction, message, animationSpeed):
    blankx, blanky = getBlankPosition(board)
    if direction == UP:
        move_in_xaxis = blankx
        move_in_yaxis = blanky + 1
    elif direction == DOWN:
        move_in_xaxis = blankx
        move_in_yaxis = blanky - 1
    elif direction == LEFT:
        move_in_xaxis = blankx + 1
        move_in_yaxis = blanky
    elif direction == RIGHT:
        move_in_xaxis = blankx - 1
        move_in_yaxis = blanky

    drawBoard(board, message)
    baseSurf = DISPLAYSURF.copy()
    
    take_left, take_top = getLeftTopOfTile(move_in_xaxis, move_in_yaxis)
    pygame.draw.rect(baseSurf, BGCOLOR, (take_left,
                     take_top, block_size, block_size))

    for i in range(0, block_size, animationSpeed):
        
        check_exit_req()
        DISPLAYSURF.blit(baseSurf, (0, 0))
        if direction == UP:
            draw_block(move_in_xaxis, move_in_yaxis,
                       board[move_in_xaxis][move_in_yaxis], 0, -i)
        if direction == DOWN:
            draw_block(move_in_xaxis, move_in_yaxis,
                       board[move_in_xaxis][move_in_yaxis], 0, i)
        if direction == LEFT:
            draw_block(move_in_xaxis, move_in_yaxis,
                       board[move_in_xaxis][move_in_yaxis], -i, 0)
        if direction == RIGHT:
            draw_block(move_in_xaxis, move_in_yaxis,
                       board[move_in_xaxis][move_in_yaxis], i, 0)

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def generateNewPuzzle(numSlides):
    
    sequence = []
    board = start_playing()
    drawBoard(board, '')
    pygame.display.update()
    
    pygame.time.wait(500)
    lastMove = None
    for i in range(numSlides):
        move = ramdom_moves(board, lastMove)
        sliding_animation(board, move, 'patientez pendant la Generation d\'un nouveau puzzle...',
                          animationSpeed=int(block_size / 3))
        take_turn(board, move)
        sequence.append(move)
        lastMove = move
    return (board, sequence)


def rst_animation(board, allMoves):
    
    reverse_moves = allMoves[:]
    reverse_moves.reverse()

    for move in reverse_moves:
        if move == UP:
            opp_moves = DOWN
        elif move == DOWN:
            opp_moves = UP
        elif move == RIGHT:
            opp_moves = LEFT
        elif move == LEFT:
            opp_moves = RIGHT
        sliding_animation(board, opp_moves, '',
                          animationSpeed=int(block_size / 2))
        take_turn(board, opp_moves)

if __name__ == '__main__':
    main()
