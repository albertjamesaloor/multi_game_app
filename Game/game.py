import pygame
import random
from constants import *
from sprites import *

class Shooter:
    def yellow_handle_movement(keys_pressed, yellow):
        if keys_pressed[pygame.K_a] and yellow.x -  VEL > 0:  # LEFT
            yellow.x -=  VEL
        if keys_pressed[pygame.K_d] and yellow.x +  VEL + yellow.width <  BORDER.x:  # RIGHT
            yellow.x +=  VEL
        if keys_pressed[pygame.K_w] and yellow.y -  VEL > 0:  # UP
            yellow.y -=  VEL
        if keys_pressed[pygame.K_s] and yellow.y +  VEL + yellow.height < height - 10:  # DOWN
            yellow.y +=  VEL

    def red_handle_movement(keys_pressed, red):
        if keys_pressed[pygame.K_LEFT] and red.x -  VEL >  BORDER.x:  # LEFT
            red.x -=  VEL
        if keys_pressed[pygame.K_RIGHT] and red.x +  VEL + red.width < width:  # RIGHT
            red.x +=  VEL
        if keys_pressed[pygame.K_UP] and red.y -  VEL > 0:  # UP
            red.y -=  VEL
        if keys_pressed[pygame.K_DOWN] and red.y +  VEL + red.height < height - 10:  # DOWN
            red.y +=  VEL

    def handle_bullets(yellow_bullets, red_bullets, yellow, red):
        for bullet in yellow_bullets:
            bullet.x +=  BULLET_VEL
            if red.colliderect(bullet):
                pygame.event.post(pygame.event.Event( RED_HIT))
                yellow_bullets.remove(bullet)
            elif bullet.x > width:
                yellow_bullets.remove(bullet)

        for bullet in red_bullets:
            bullet.x -=  BULLET_VEL
            if yellow.colliderect(bullet):
                pygame.event.post(pygame.event.Event( YELLOW_HIT))
                red_bullets.remove(bullet)
            elif bullet.x < 0:
                red_bullets.remove(bullet)

class Wordler:
    def __init__(self, exit_to_menu_callback, victory):
        pygame.init()
        self.win = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Wordler")
        self.clock = pygame.time.Clock()
        self.create_word_list()
        self.letters_text = UIElement(width * 0.33, height * 0.05, "Not Enough Letters", white)
        self.exit_to_menu = exit_to_menu_callback
        self.victory = victory

    def create_word_list(self):
        with open("words.txt", "r") as file:
            self.words_list = file.read().splitlines()

    def new(self):
        self.word = random.choice(self.words_list).upper()
        print(self.word)
        self.text = ""
        self.current_row = 0
        self.tiles = []
        self.create_tiles()
        self.flip = True
        self.not_enough_letters = False
        self.timer = 0

    def create_tiles(self):
        for row in range(6):
            self.tiles.append([])
            for col in range(5):
                self.tiles[row].append(Tile((col * (TILESIZE + GAPSIZE)) + MARGIN_X, (row * (TILESIZE + GAPSIZE)) + MARGIN_Y))

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
    def update(self):
        self.add_letter()

    def add_letter(self):
        # empty all the letter in the current row
        for tile in self.tiles[self.current_row]:
            tile.letter = ""

        # add the letters typed to the current row
        for i, letter in enumerate(self.text):
            self.tiles[self.current_row][i].letter = letter
            self.tiles[self.current_row][i].create_font()

    def draw_tiles(self):
        for row in self.tiles:
            for tile in row:
                tile.draw(self.win)

    def draw(self):
        self.win.fill(BGCOLOUR)
        # display the not enough letters text
        if self.not_enough_letters:
            self.timer += 1
            self.letters_text.fade_in()
            if self.timer > 90:
                self.not_enough_letters = False
                self.timer = 0
        else:
            self.letters_text.fade_out()
        self.letters_text.draw(self.win)

        self.draw_tiles()

        pygame.display.flip()

    def row_animation(self):
        # row shaking if not enough letters is inputted
        self.not_enough_letters = True
        start_pos = self.tiles[0][0].x
        amount_move = 4
        move = 3
        win_copy = self.win.copy()
        win_copy.fill(BGCOLOUR)
        for row in self.tiles:
            for tile in row:
                if row != self.tiles[self.current_row]:
                    tile.draw(win_copy)

        while True:
            while self.tiles[self.current_row][0].x < start_pos + amount_move:
                self.win.blit(win_copy, (0, 0))
                for tile in self.tiles[self.current_row]:
                    tile.x += move
                    tile.draw(self.win)
                self.clock.tick(FPS)
                pygame.display.flip()

            while self.tiles[self.current_row][0].x > start_pos - amount_move:
                self.win.blit(win_copy, (0, 0))
                for tile in self.tiles[self.current_row]:
                    tile.x -= move
                    tile.draw(self.win)
                self.clock.tick(FPS)
                pygame.display.flip()

            amount_move -= 2
            if amount_move < 0:
                break

    def box_animation(self):
        # tile scale animation for every letter inserted
        for tile in self.tiles[self.current_row]:
            if tile.letter == "":
                win_copy = self.win.copy()
                for start, end, step in ((0, 6, 1), (0, -6, -1)):
                    for size in range(start, end, 2*step):
                        self.win.blit(win_copy, (0, 0))
                        tile.x -= size
                        tile.y -= size
                        tile.width += size * 2
                        tile.height += size * 2
                        surface = pygame.Surface((tile.width, tile.height))
                        surface.fill(BGCOLOUR)
                        self.win.blit(surface, (tile.x, tile.y))
                        tile.draw(self.win)
                        pygame.display.flip()
                        self.clock.tick(FPS)
                    self.add_letter()
                break

    def reveal_animation(self, tile, colour):
        # reveal colours animation when user input the whole word
        win_copy = self.win.copy()

        while True:
            surface = pygame.Surface((tile.width + 5, tile.height + 5))
            surface.fill(BGCOLOUR)
            win_copy.blit(surface, (tile.x, tile.y))
            self.win.blit(win_copy, (0, 0))
            if self.flip:
                tile.y += 6
                tile.height -= 12
                tile.font_y += 4
                tile.font_height = max(tile.font_height - 8, 0)
            else:
                tile.colour = colour
                tile.y -= 6
                tile.height += 12
                tile.font_y -= 4
                tile.font_height = min(tile.font_height + 8, tile.font_size)
            if tile.font_height == 0:
                self.flip = False

            tile.draw(self.win)
            pygame.display.update()
            self.clock.tick(FPS)

            if tile.font_height == tile.font_size:
                self.flip = True
                break

    def check_letters(self):
        # algorithm to check if the letters inputted correspond to any of the letters in the actual word
        copy_word = [x for x in self.word]
        for i, user_letter in enumerate(self.text):
            colour = LIGHTGREY
            for j, letter in enumerate(copy_word):
                if user_letter == letter:
                    colour = YELLOW
                    if i == j:
                        colour = GREEN
                    copy_word[j] = ""
                    break
            # reveal animation
            self.reveal_animation(self.tiles[self.current_row][i], colour)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.playing = False  # Exit the game loop
                    self.exit_to_menu()

                if event.key == pygame.K_RETURN:

                    if len(self.text) == 5:
                        # check all letters
                        self.check_letters()

                        # if the text is correct or the player has used all his turns
                        if self.text == self.word or self.current_row + 1 == 6:
                            # player lose, lose message is sent
                            if self.text != self.word:
                                self.end_win_text = UIElement(width * 0.33, height * 0.9, f"THE WORD WAS: {self.word}", white)

                            # player win, send win message
                            else:
                                self.end_win_text = UIElement(width * 0.36, height * 0.9, "YOU GUESSED RIGHT", white)
                                self.victory()

                            # restart the game
                            self.playing = False
                            self.end_win()
                            break

                        self.current_row += 1
                        self.text = ""

                    else:
                        # row animation, not enough letters message
                        self.row_animation()

                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]

                else:
                    if len(self.text) < 5 and event.unicode.isalpha():
                        self.text += event.unicode.upper()
                        self.box_animation()
    def end_win(self):
        play_again = UIElement(85, 750, "PRESS ENTER TO PLAY AGAIN", white, 30)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit(0)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return

            self.win.fill(BGCOLOUR)
            self.draw_tiles()
            self.end_win_text.fade_in()
            self.end_win_text.draw(self.win)
            play_again.fade_in()
            play_again.draw(self.win)
            pygame.display.flip()