# autor: Paweł Ostrowski
import pygame
import math

# ustawienia wlasciwosci wyswietlanego okna
pygame.init()
WIDTH, HEIGHT = 700, 700
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Connect 4")

# przypisanie wartosci RGB do zmiennych dla usprawnienia odwolywania sie do kolorow
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WORD_FONT = pygame.font.SysFont('comicsans', 40)
SMALL_FONT = pygame.font.SysFont('comicsans', 20)

# wczytanie obrazow z plikow
arrow = pygame.image.load("arrow.png")
arrow = pygame.transform.scale(arrow, (40, 40))
plansza = pygame.image.load("board.png")
blue_chip = pygame.image.load("blue.png")
red_chip = pygame.image.load("red.png")

# klasa rodzica
class Board:
    # konstruktor planszy
    def __init__(self):
        # ----------> prosta wersja planszy (opcjonalne) <----------
        # win.fill(WHITE)
        # for i in range(1, 7):
        #     pygame.draw.line(win, BLACK, (i*100, 50), (i*100, 650))
        #     pygame.draw.line(win, BLACK, (0, 50 + i*100), (700, 50 + i*100))
        win.blit(plansza, (0, 0))
        text = SMALL_FONT.render("ARROWS + SPACE", 1, BLACK)
        win.blit(text, (175 - text.get_width()/2, 675 - text.get_height()/2))
        text = SMALL_FONT.render("A, D KEYS + ENTER", 1, BLACK)
        win.blit(text, (525 - text.get_width()/2, 675 - text.get_height()/2))

        pygame.display.update()

        # lista przechowujaca polozenie zetonow na planszy
        self.tab = [[0 for i in range(7)] for j in range(6)]


    # sprawdzenie czy zostal spelniony warunek wygranej
    def check_win(self, turn, column):
        # iteracja do ostatniego wrzuconego zetonu
        i = 0
        while self.tab[i][column] != turn:
            i += 1
        x = i

        # pionowo
        connected = 0
        while i < 6 and self.tab[i][column] == turn:
            connected += 1
            i += 1
        if connected >= 4:
            return True

        # poziomo
        left = 0
        right = 0
        i = 1
        while column - i >= 0 and self.tab[x][column-i] == turn:
            left += 1
            i += 1
        i = 1
        while column + i < 7 and self.tab[x][column+i] == turn:
            right += 1
            i += 1
        if left + right >= 3:
            return True

        # na ukos
        left = 0
        right = 0
        i = 1
        while column - i >= 0 and x - i >= 0 and self.tab[x-i][column-i] == turn:
            left += 1
            i += 1
        i = 1
        while column + i < 7 and x + i < 6 and self.tab[x+i][column+i] == turn:
            right += 1
            i += 1
        if left + right >= 3:
            return True

        left = 0
        right = 0
        i = 1
        while column - i >= 0 and x + i < 6 and self.tab[x+i][column-i] == turn:
            left += 1
            i += 1
        i = 1
        while column + i < 7 and x - i >= 0 and self.tab[x-i][column+i] == turn:
            right += 1
            i += 1
        if left + right >= 3:
            return True
        
        # zwraca False jesli zaden z powyzszych warunkow nie zostal spelniony
        return False
    
    # sprawdzenie warunkow remisu (cala plansza zapelniona bez zwyciestwa zadnej ze stron)
    def check_draw(self):
        for i in range(6):
            for j in range(7):
                if self.tab[i][j] == 0:
                    return False
        return True

# klasa potomna dziedziczaca z klasy Board
class Chip(Board):
    # metoda wyswietlajaca zetony na planszy
    def draw(self):
        for i in range(6):
            for j in range(7):
                if self.tab[i][j] == 1:
                    win.blit(blue_chip, (10 + j*100, 62 + i*100))
                elif self.tab[i][j] == 2:
                    win.blit(red_chip, (10 + j*100, 62 + i*100))
        pygame.display.update()

    # metoda dodajaca zeton
    def add(self, color, column):
        i = 5
        while i >= 0:
            if self.tab[i][column] == 0:
                self.tab[i][column] = color
                return True
            i -= 1
        return False

# zmiana tury
def switch_turn(turn):
    if turn == 1:
        return 2
    elif turn == 2:
        return 1
    else:
        return False

# wyswietlenie zapytania o nowa gre; zwraca True, jesli wcisnieto YES, False - jesli wcisnieto NO


def play_again():
    pygame.time.delay(1000)
    # wyswietlenie okienka z zapytaniem
    pygame.draw.rect(win, WHITE, (100, 200, 500, 300), 0, 0)
    pygame.draw.rect(win, BLACK, (100, 200, 500, 300), 2, 0)
    text = WORD_FONT.render("PLAY AGAIN?", 1, BLACK)
    win.blit(text, (350 - text.get_width()/2, 250))
    pygame.draw.circle(win, BLACK, (200, 400), 50, 2)
    text = WORD_FONT.render("YES", 1, BLACK)
    win.blit(text, (200 - text.get_width()/2, 400 - text.get_height()/2))
    pygame.draw.circle(win, BLACK, (WIDTH - 200, 400), 50, 2)
    text = WORD_FONT.render("NO", 1, BLACK)
    win.blit(text, (WIDTH - 200 - text.get_width()/2, 400 - text.get_height()/2))
    pygame.display.update()

    while True:
        # zapisywanie polozenia kursora
        # metoda MOUSEMOTION sie nie sprawdza, poniewaz nie zapisuje polozenia kursora
        # jesli wskazuje przycisk w momencie zakonczenia gry
        m_x, m_y = pygame.mouse.get_pos()
        # wyliczanie odleglosci od przyciskow
        ydis = math.sqrt((200 - m_x)**2 + (400 - m_y)**2)
        ndis = math.sqrt((WIDTH - 200 - m_x) ** 2 + (400 - m_y)**2)
        # podswietlenie przyciskow po najechaniu kursorem
        if ydis < 50:
            pygame.draw.circle(win, GREEN, (200, 400), 50, 2)
            pygame.display.update()
        elif ndis < 50:
            pygame.draw.circle(win, GREEN, (WIDTH - 200, 400), 50, 2)
            pygame.display.update()
        # wylaczenie podswietlenia
        else:
            pygame.draw.circle(win, BLACK, (200, 400), 50, 2)
            pygame.draw.circle(win, BLACK, (WIDTH - 200, 400), 50, 2)
            pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # jesli wcisnieto YES
                if ydis < 50:
                    return True
                # jesli wcisnieto NO
                elif ndis < 50:
                    return False
            if event.type == pygame.KEYDOWN:
                # zwraca True po wcisnieciu klawisza Y, False po wcisnieciu N
                # dodatkowo podswietla wybrany przycisk na pol sekundy
                pygame.draw.circle(win, BLACK, (200, 400), 50, 2)
                pygame.draw.circle(win, BLACK, (WIDTH - 200, 400), 50, 2)
                if event.key == pygame.K_y:
                    pygame.draw.circle(win, GREEN, (200, 400), 50, 2)
                    pygame.display.update()
                    pygame.time.delay(500)
                    return True
                elif event.key == pygame.K_n:
                    pygame.draw.circle(win, GREEN, (WIDTH - 200, 400), 50, 2)
                    pygame.display.update()
                    pygame.time.delay(500)
                    return False


def main():
    mode = 0   # 0 -> strzalki i spacja, 1 -> A,D i Enter
    run = True
    # petla konczy dzialanie jesli zamknieto okno lub wybrano NO w oknie "PLAY AGAIN?"
    while run:
        b1 = Chip()
        b1.draw()
        play = True
        turn = 1
        keys = 0
        freeze = 0
        pygame.transform.threshold(arrow, arrow, BLUE, BLUE, BLUE, 1, None, True)

        # petla konczy dzialanie kiedy zakonczy sie runda
        while play:
            # zmiana koloru strzalki wskazujacej wybrana kolumne
            if turn == 1:
                pygame.transform.threshold(arrow, arrow, RED, RED, BLUE, 1, None, True)
            else:
                pygame.transform.threshold(arrow, arrow, BLUE, BLUE, RED, 1, None, True)
            m_x, m_y = pygame.mouse.get_pos()
            # ustawienie biezacej kolumny na ta ktora wskazuje myszka, jesli sterowanie klawiatura jest wylaczone
            if keys == 0:
                column = m_x//100
            # zasloniecie strzalki w poprzedniej pozycji
            pygame.draw.rect(win, WHITE, (0, 0, 700, 50), 0, 0)
            # wyswietlenie strzalki w aktualnej pozycji
            win.blit(arrow, (25 + column * 100, 10))

            # zaznaczenie przycisku z aktualnym trybem sterowania na zielono
            if mode == 0:
                pygame.draw.rect(win, BLACK, (425, 660, 200, 30), 3, 5)
                pygame.draw.rect(win, GREEN, (75, 660, 200, 30), 3, 5)
            else:
                pygame.draw.rect(win, BLACK, (75, 660, 200, 30), 3, 5)
                pygame.draw.rect(win, GREEN, (425, 660, 200, 30), 3, 5)

            pygame.display.update()

            # wylaczenie sterowania klawiatura jesli poruszy sie myszka
            if m_x != freeze:
                keys = 0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    play = False
                    run = False
                    del b1
                if event.type == pygame.KEYDOWN:
                    # jesli zostanie wcisnieta strzalka w lewo/prawo albo A/D, zapisywana jest ostatnia pozycja myszki
                    # i sterowanie jest przelaczane na klawiature
                    if ((event.key == pygame.K_RIGHT and mode == 0) or (event.key == pygame.K_d and mode == 1)) and column < 6:
                        m_x, m_y = pygame.mouse.get_pos()
                        freeze = m_x  # zmienna przechowujaca pozycje myszki w osi x
                        keys = 1
                        column += 1
                    elif ((event.key == pygame.K_LEFT and mode == 0) or (event.key == pygame.K_a and mode == 1)) and column > 0:
                        m_x, m_y = pygame.mouse.get_pos()
                        freeze = m_x
                        keys = 1
                        column -= 1
                    elif (event.key == pygame.K_SPACE and mode == 0) or (event.key == pygame.K_RETURN and mode == 1):
                        # jesli uda sie dodac zeton (kolumna nie jest zapelniona), aktualizujemy stan planszy
                        if b1.add(turn, column):
                            b1.draw()

                            # sprawdzenie warunkow zwyciestwa lub remisu po kazdej turze
                            if b1.check_win(turn, column):
                                pygame.draw.rect(
                                    win, WHITE, (0, 0, 700, 50), 0, 0)
                                if turn == 1:
                                    text = WORD_FONT.render(
                                        "BLUE WINS", 1, BLACK)
                                    win.blit(
                                        text, (WIDTH/2 - text.get_width()/2, 0))
                                    pygame.display.update()
                                    run = play_again()
                                else:
                                    text = WORD_FONT.render(
                                        "RED WINS", 1, BLACK)
                                    win.blit(
                                        text, (WIDTH/2 - text.get_width()/2, 0))
                                    pygame.display.update()
                                    run = play_again()

                                play = False
                                del b1
                            elif b1.check_draw():
                                pygame.draw.rect(
                                    win, WHITE, (0, 0, 700, 50), 0, 0)
                                text = WORD_FONT.render("DRAW", 1, BLACK)
                                win.blit(
                                    text, (WIDTH/2 - text.get_width()/2, 0))
                                pygame.display.update()
                                run = play_again()
                                play = False
                                del b1
                            # zmiana tury
                            turn = switch_turn(turn)

                # jesli sterowanie klawiatura jest wylaczone i lewy przycisk myszy zostanie wcisniety, dodajemy zeton (o ile to mozliwe)
                # dalej to samo co w przypadku sterowania klawiatura
                if event.type == pygame.MOUSEBUTTONDOWN:
                    m_x, m_y = pygame.mouse.get_pos()
                    column = m_x//100
                    if m_y >= 660 and m_y <= 690:
                        if m_x >= 75 and m_x <= 275:
                            mode = 0
                        elif m_x >= 425 and m_x <= 625:
                            mode = 1
                    elif keys == 0:
                        if b1.add(turn, column):
                            b1.draw()

                            if b1.check_win(turn, column):
                                pygame.draw.rect(
                                    win, WHITE, (0, 0, 700, 50), 0, 0)
                                if turn == 1:
                                    text = WORD_FONT.render(
                                        "BLUE WINS", 1, BLACK)
                                    win.blit(
                                        text, (WIDTH/2 - text.get_width()/2, 0))
                                    pygame.display.update()
                                    run = play_again()
                                else:
                                    text = WORD_FONT.render(
                                        "RED WINS", 1, BLACK)
                                    win.blit(
                                        text, (WIDTH/2 - text.get_width()/2, 0))
                                    pygame.display.update()
                                    run = play_again()

                                play = False
                                del b1
                            elif b1.check_draw():
                                pygame.draw.rect(
                                    win, WHITE, (0, 0, 700, 50), 0, 0)
                                text = WORD_FONT.render("DRAW", 1, BLACK)
                                win.blit(
                                    text, (WIDTH/2 - text.get_width()/2, 0))
                                pygame.display.update()
                                run = play_again()
                                play = False
                                del b1
                            turn = switch_turn(turn)


main()
pygame.quit()