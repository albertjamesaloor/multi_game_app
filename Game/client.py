import pygame
from network import Network
from button import mainButton, Button
import constants
import user_management
from game import RPS, Shooter

pygame.font.init()
pygame.mixer.init()
pygame.mixer.set_num_channels(16)

win = pygame.display.set_mode((constants.width, constants.height))
pygame.display.set_caption("Rock Paper Scissors")

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("Assets/font.ttf", size)

def draw_rps_win(win, game, p, score_a, score_b):
    win.blit(constants.BACKGROUND, (0, 0))
    
    if not(RPS.connected()):
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Waiting for Player...", 1, constants.white)
        win.blit(text, (constants.width/2 - text.get_width()/2, constants.height/2 - text.get_height()/2))
    else:
        win.blit(constants.BACKGROUND_TITLE,(constants.width/2 - constants.BACKGROUND_TITLE.get_width()/2, constants.height/2 - constants.BACKGROUND_TITLE.get_height()/2))
        font = pygame.font.SysFont("comicsans", 40)
        text = font.render("Your Move", 1, constants.Mint_Green)
        win.blit(text, (constants.width/4 - text.get_width()/2, 100))

        text = font.render("Opponents", 1, constants.Mint_Green)
        win.blit(text, (constants.width*0.75 - text.get_width()/2, 100))

        Player0_score = font.render(f"Score: {score_a}", 1, constants.white)
        Player1_score = font.render(f"Score: {score_b}", 1, constants.white)
        win.blit(Player0_score, (constants.width - Player0_score.get_width() - 10, 10))
        win.blit(Player1_score, (10, 10))

        move1 = RPS.get_player_move(0)
        move2 = RPS.get_player_move(1)
        if RPS.bothWent():
            text1 = font.render(move1, 1, constants.white)
            text2 = font.render(move2, 1, constants.white)
        else:
            if RPS.p1Went and p == 0:
                text1 = font.render(move1, 1, constants.white)
            elif RPS.p1Went:
                text1 = font.render("Locked In", 1, constants.Mint_Green)
            else:
                text1 = font.render("Waiting...", 1, constants.Mint_Green)

            if RPS.p2Went and p == 1:
                text2 = font.render(move2, 1, constants.white)
            elif RPS.p2Went:
                text2 = font.render("Locked In", 1, constants.Mint_Green)
            else:
                text2 = font.render("Waiting...", 1, constants.Mint_Green)

        if p == 1:
            win.blit(text2, (constants.width/4 - text.get_width()/2, 520))
            win.blit(text1, (constants.width*0.75 - text.get_width()/2, 520))
        else:
            win.blit(text1, (constants.width/4 - text.get_width()/2, 520))
            win.blit(text2, (constants.width*0.75 - text.get_width()/2, 520))

        for btn in btns:
            btn.draw(win)

    pygame.display.update()

btns = [Button("Rock", 470, 600, constants.Pale_Lavender), Button("Paper", 590, 600, constants.Pale_Lavender), Button("Scissors", 710, 600, constants.Pale_Lavender)]

#rock paper scissors
def rps():
    
    run = True
    clock = pygame.time.Clock()
    n = Network()
    player = int(n.getP())
    print("You are player", player)

    score_a = 0
    score_b = 0
    while run:
        clock.tick(60)
        try:
            game = n.send("get")
        except:
            run = False
            print("Couldn't get game")
            break
        
        if RPS.bothWent():
            draw_rps_win(win, game, player, score_a, score_b)
            
            if player == 0:
                if RPS.get_player_move(0) == "Rock":
                    win.blit(constants.PLAYER_ROCK_IMAGE, (0, constants.height/2 - constants.height*0.2))
                elif RPS.get_player_move(0) == "Paper":
                    win.blit(constants.PLAYER_PAPER_IMAGE, (0, constants.height/2 - constants.height*0.2))
                elif RPS.get_player_move(0) == "Scissors":
                    win.blit(constants.PLAYER_SCISSORS_IMAGE, (0, constants.height/2 - constants.height*0.2))

                if RPS.get_player_move(1) == "Rock":
                    win.blit(constants.OPPONENT_ROCK_IMAGE, (constants.width*0.6 , constants.height/2 - constants.height*0.2))
                elif RPS.get_player_move(1) == "Paper":
                    win.blit(constants.OPPONENT_PAPER_IMAGE, (constants.width*0.6 , constants.height/2 - constants.height*0.2))
                elif RPS.get_player_move(1) == "Scissors":
                    win.blit(constants.OPPONENT_SCISSORS_IMAGE, (constants.width*0.6 , constants.height/2 - constants.height*0.2))

            if player == 1:
                if RPS.get_player_move(1) == "Rock":
                    win.blit(constants.PLAYER_ROCK_IMAGE, (0, constants.height/2 - constants.height*0.2))
                elif RPS.get_player_move(1) == "Paper":
                    win.blit(constants.PLAYER_PAPER_IMAGE, (0, constants.height/2 - constants.height*0.2))
                elif RPS.get_player_move(1) == "Scissors":
                    win.blit(constants.PLAYER_SCISSORS_IMAGE, (0, constants.height/2 - constants.height*0.2))

                if RPS.get_player_move(0) == "Rock":
                    win.blit(constants.OPPONENT_ROCK_IMAGE, (constants.width*0.6, constants.height/2 - constants.height*0.2))
                elif RPS.get_player_move(0) == "Paper":
                    win.blit(constants.OPPONENT_PAPER_IMAGE, (constants.width*0.6 , constants.height/2 - constants.height*0.2))
                elif RPS.get_player_move(0) == "Scissors":
                    win.blit(constants.OPPONENT_SCISSORS_IMAGE, (constants.width*0.6, constants.height/2 - constants.height*0.2))

            pygame.time.delay(500)
            try:
                game = n.send("reset")
            except:
                run = False
                print("Couldn't get game")
                break

            
            if (game.winner() == 1 and player == 1) or (game.winner() == 0 and player == 0):
                score_b += 1
            elif game.winner() == -1:
                pass

            else:
                score_a += 1

            if score_a == 3 or score_b == 3:
                score_a = score_b = 0
                font = pygame.font.SysFont("Times New Roman", 300)
                if score_b > score_a:
                    text = font.render("You Won!", 1, constants.Electric_Blue)
                elif score_a < score_b:
                    text = font.render("You Lost...", 1, constants.Electric_Blue)

                win.blit(text, (constants.width/2 - text.get_width()/2, constants.height/2 - text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(3000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in btns:
                    if btn.click(pos) and game.connected():
                        if player == 0:
                            if not game.p1Went:
                                n.send(btn.text)
                        else:
                            if not game.p2Went:
                                n.send(btn.text)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    score_a = score_b = 0
                    n.close()
                    main_menu(username)

        draw_rps_win(win, game, player, score_a, score_b)

def draw_shooter_win(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    win.blit(constants.SPACE, (0, 0))
    pygame.draw.rect(win, constants.black, constants.BORDER)
    win.blit(constants.YELLOW_SPACESHIP, (yellow.x, yellow.y))
    win.blit(constants.RED_SPACESHIP, (red.x, red.y))

    # Display health
    red_health_text = constants.HEALTH_FONT.render(f"Health: {red_health}", 1, constants.white)
    yellow_health_text = constants.HEALTH_FONT.render(f"Health: {yellow_health}", 1, constants.white)
    win.blit(red_health_text, (constants.width - red_health_text.get_width() - 10, 10))
    win.blit(yellow_health_text, (10, 10))

    # Draw bullets
    for bullet in red_bullets:
        pygame.draw.rect(win, constants.RED, bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(win, constants.YELLOW, bullet)

    pygame.display.update()

def draw_winner(text):
    draw_text = constants.WINNER_FONT.render(text, 1, constants.white)
    win.blit(draw_text, (constants.width / 2 - draw_text.get_width() // 2, constants.height / 2 - draw_text.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(5000)

#shooter game
def shooter():
    red = pygame.Rect(1020, 360, constants.SPACESHIP_width, constants.SPACESHIP_height)
    yellow = pygame.Rect(200, 360, constants.SPACESHIP_width, constants.SPACESHIP_height)

    red_bullets = []
    yellow_bullets = []

    red_health = 10
    yellow_health = 10

    clock = pygame.time.Clock()
    constants.SPACE_BGM.play(-1)  # Loop the background music indefinitely
    constants.SPACE_BGM.set_volume(0.5)  # Lower background music volume


    run = True
    while run:
        clock.tick(constants.FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < constants.MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height // 2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    constants.BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(red_bullets) < constants.MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height // 2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    constants.BULLET_FIRE_SOUND.play()
                if event.key == pygame.K_ESCAPE:
                    red_health = yellow_health = 10
                    constants.SPACE_BGM.stop()
                    main_menu(username)

            if event.type == constants.RED_HIT:
                red_health -= 1
                constants.BULLET_HIT_SOUND.play()

            if event.type == constants.YELLOW_HIT:
                yellow_health -= 1
                constants.BULLET_HIT_SOUND.play()

        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow Wins!"
        if yellow_health <= 0:
            winner_text = "Red Wins!"

        if winner_text != "":
            constants.WIN_SOUND.play()
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        Shooter.yellow_handle_movement(keys_pressed, yellow)
        Shooter.red_handle_movement(keys_pressed, red)

        Shooter.handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_shooter_win(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)

    shooter()

def main_menu(username):
    stats = user_management.load_user_stats(username)
    run = True
    clock = pygame.time.Clock()
    while True:
        clock.tick(60)
        win.blit(constants.BACKGROUND,(0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        RPS_BUTTON = mainButton(image=pygame.image.load("Assets/Play Rect.png"), pos=(640, 250), 
                            text_input="RPS", font=get_font(75), base_color=constants.Blue, hovering_color=constants.white)
        SHOOTER_BUTTON = mainButton(image=pygame.image.load("Assets/Options Rect.png"), pos=(640, 400), 
                            text_input="SHOOTER", font=get_font(75), base_color=constants.Blue, hovering_color=constants.white)
        QUIT_BUTTON = mainButton(image=pygame.image.load("Assets/Quit Rect.png"), pos=(640, 550), 
                            text_input="QUIT", font=get_font(75), base_color=constants.Blue, hovering_color=constants.white)

        win.blit(MENU_TEXT, MENU_RECT)

        for button in [RPS_BUTTON, SHOOTER_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(win)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if RPS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    rps()
                if SHOOTER_BUTTON.checkForInput(MENU_MOUSE_POS):
                    shooter()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    run = False 

        pygame.display.update()

while True:
    username = user_management.login(win)
    main_menu(username)
    