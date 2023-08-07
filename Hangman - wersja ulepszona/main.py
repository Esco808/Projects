import pygame
import math
import sys


pygame.init()
WIDTH, HEIGHT = 800, 500
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman Game!")


RADIUS = 20
GAP = 15

LETTER_FONT = pygame.font.SysFont('comicsans', 40)
WORD_FONT = pygame.font.SysFont('comicsans', 60)
TITLE_FONT = pygame.font.SysFont('comicsans', 70)


images = []
for i in range(7):
    image = pygame.image.load("hangman" + str(i) + ".png")
    images.append(image)


WHITE = (255,255,255)
BLACK = (0,0,0)

def askword():
    win.fill(WHITE)
    text = LETTER_FONT.render("PLAYER 1: WRITE A WORD", 1, BLACK)
    win.blit(text, (WIDTH/2 - text.get_width()/2, 20))

    user_text = ''
    

    input_rect = pygame.Rect(WIDTH/2 - 200/2, HEIGHT/2 - 70/2, 200, 70)
    color= pygame.Color('chartreuse4')

    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                elif event.key == pygame.K_RETURN:
                    return user_text
                else:
                    user_text += event.unicode
        user_text = user_text.upper()
        pygame.draw.rect(win, color, input_rect)
    
        text_surface = WORD_FONT.render(user_text, 1, BLACK)
        
        win.blit(text_surface, (input_rect.x+5, input_rect.y-5))
        
        input_rect.w = max(100, text_surface.get_width()+10)
        
        pygame.display.flip()
    

def draw(word, guessed, letters):
    win.fill(WHITE)

    text = TITLE_FONT.render("HANGMAN", 1, BLACK)
    win.blit(text, (WIDTH/2 - text.get_width()/2, 20))

    display_word = ""
    for letter in word:
        if letter in guessed:
            display_word += letter + " "
        else:
            display_word += "_ "
    text = WORD_FONT.render(display_word, 1, BLACK)
    win.blit(text, (400, 200))

    for letter in letters:
        x, y, ltr, visible = letter
        if visible:
            pygame.draw.circle(win, BLACK, (x, y), RADIUS, 3)
            text = LETTER_FONT.render(ltr, 1, BLACK)
            win.blit(text, (x - text.get_width()/2, y - text.get_height()/2))

    win.blit(images[hangman_status], (150, 100))
    pygame.display.update()


def display_message(message):
    pygame.time.delay(1000)
    win.fill(WHITE)
    text = WORD_FONT.render(message, 1, BLACK)
    win.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(3000)

def main():
    play = True
    while play:
        global hangman_status

        FPS = 60
        clock = pygame.time.Clock()
        run = True

        letters = []
        startx = round((WIDTH - (RADIUS * 2 + GAP) * 13) / 2)
        starty = 400
        A = 65
        for i in range(26):
            x = startx + GAP * 2 + ((RADIUS * 2 + GAP) * (i % 13))
            y = starty + ((i // 13) * (GAP + RADIUS * 2))
            letters.append([x, y, chr(A + i), True])

        hangman_status = 0
        guessed = []
        word = askword()

        while run:
            clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    play = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    m_x, m_y = pygame.mouse.get_pos()
                    for letter in letters:
                        x, y, ltr, visible = letter
                        if visible:
                            dis = math.sqrt((x - m_x)**2 + (y - m_y)**2)
                            if dis < RADIUS:
                                letter[3] = False
                                guessed.append(ltr)
                                if ltr not in word:
                                    hangman_status += 1
            
            draw(word, guessed, letters)

            won = True
            for letter in word:
                if letter not in guessed:
                    won = False
                    break
            
            if won:
                display_message("You WON!")
                break

            if hangman_status == 6:
                display_message("You LOST!")
                break
        clicked = False
        while clicked == False and play == True:
            win.fill(WHITE)
            text = LETTER_FONT.render("PLAY AGAIN?", 1, BLACK)
            win.blit(text, (WIDTH/2 - text.get_width()/2, 20))
            pygame.draw.circle(win, BLACK, (200, HEIGHT-200), RADIUS*3, 3)
            text = LETTER_FONT.render("YES", 1, BLACK)
            win.blit(text, (200 - text.get_width()/2, HEIGHT - 200 - text.get_height()/2))
            pygame.draw.circle(win, BLACK, (WIDTH - 200, HEIGHT-200), RADIUS*3, 3)
            text = LETTER_FONT.render("NO", 1, BLACK)
            win.blit(text, (WIDTH - 200 - text.get_width()/2, HEIGHT - 200 - text.get_height()/2))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    m_x, m_y = pygame.mouse.get_pos()
                    ydis = math.sqrt((200 - m_x)**2 + (HEIGHT - 200 - m_y)**2)
                    ndis = math.sqrt((WIDTH - 200 - m_x)**2 + (HEIGHT - 200 - m_y)**2)
                    if ydis < RADIUS*3:
                        clicked = True
                        play = True
                        break
                    elif ndis < RADIUS*3:
                        clicked = True
                        play = False
                        break

  
main()
pygame.quit()