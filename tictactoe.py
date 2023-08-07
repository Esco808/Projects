import pygame
import math
import sys

pygame.init()
WIDTH, HEIGHT = 600, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TicTacToe")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
WORD_FONT = pygame.font.SysFont('comicsans', 60)

# # board
# board = [(0, 0, "empty")]*9
# for i in range(9):
#     board[i] = (200+(i % 3)*100, 200 + (i//3)*100, "empty")



def draw_x(n, board):
    tmp = list(board[n])
    tmp[2] = "x"
    board[n] = tuple(tmp)

    x, y = board[n][0], board[n][1]
    pygame.draw.line(win, BLACK, (x-30, y-30), (x + 30, y + 30), 3)
    pygame.draw.line(win, BLACK, (x + 30, y - 30), (x - 30, y + 30), 3)


def draw_o(n, board):
    tmp = list(board[n])
    tmp[2] = "o"
    board[n] = tuple(tmp)

    x, y = board[n][0], board[n][1]
    pygame.draw.circle(win, BLACK, (x, y), 30, 3)

def check(symbol, board):
    if board[0][2] == symbol and board[1][2] == symbol and board[2][2] == symbol:
        return True
    elif board[3][2] == symbol and board[4][2] == symbol and board[5][2] == symbol:
        return True
    elif board[6][2] == symbol and board[7][2] == symbol and board[8][2] == symbol:
        return True   
    elif board[0][2] == symbol and board[3][2] == symbol and board[6][2] == symbol:
        return True
    elif board[1][2] == symbol and board[4][2] == symbol and board[7][2] == symbol:
        return True 
    elif board[2][2] == symbol and board[5][2] == symbol and board[8][2] == symbol:
        return True
    elif board[0][2] == symbol and board[4][2] == symbol and board[8][2] == symbol:
        return True
    elif board[2][2] == symbol and board[4][2] == symbol and board[6][2] == symbol:
        return True
    else:
        return False

def draw(board):
    for i in range(9):
        if board[i][2] == "empty":
            return False
    return True

def display_message(message):
    text = WORD_FONT.render(message, 1, BLACK)
    win.blit(text, (WIDTH/2 - text.get_width()/2, 50 - text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(3000)

def main():
    run = True
    while run:
        win.fill(WHITE)
        pygame.draw.line(win, BLACK, (250, 150), (250, 450))
        pygame.draw.line(win, BLACK, (350, 150), (350, 450))
        pygame.draw.line(win, BLACK, (150, 250), (450, 250))
        pygame.draw.line(win, BLACK, (150, 350), (450, 350))
        pygame.display.update()

        board = [(0, 0, "empty")]*9
        for i in range(9):
            board[i] = (200+(i % 3)*100, 200 + (i//3)*100, "empty")

        play = True
        turn = "x"

        while play:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    play = False
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    m_x, m_y = pygame.mouse.get_pos()
                    chosen = False
                    for i in range(9):
                        x, y = board[i][0], board[i][1]
                        distx = abs(x - m_x)
                        disty = abs(y - m_y)
                        if distx < 50 and disty < 50 and board[i][2] == "empty":
                            field = i
                            chosen = True
                            break
                    if turn == "x" and chosen:
                        draw_x(field, board)
                        turn = "o"
                    elif turn == "o" and chosen:
                        draw_o(field, board)
                        turn = "x"
                    pygame.display.update()
                    if check("x", board):
                        play = False
                        display_message("X won")
                    elif check("o", board):
                        play = False
                        display_message("O won")
                    elif draw(board):
                        play = False
                        display_message("Draw")

    pygame.display.update()


main()
pygame.quit()
