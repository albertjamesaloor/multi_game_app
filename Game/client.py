import pygame
from network import Network
from button import * 
from constants import *
from draw_utils import *
from game import Shooter, Wordler
from user_management import *

pygame.font.init()
pygame.mixer.init()
pygame.mixer.set_num_channels(16)

win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Rock Paper Scissors")


btns = [Button("Rock", 470, 600,  Pale_Lavender), Button("Paper", 590, 600,  Pale_Lavender), Button("Scissors", 710, 600,  Pale_Lavender)]

#rock paper scissors
def rps(server):
    
    run = False
    clock = pygame.time.Clock()
    n = Network(server)
    player_flag = n.getP()
    font = pygame.font.SysFont("Times New Roman", 150)
    font2 = pygame.font.SysFont("Times New Roman", 50)
    text2 = font2.render("Not connected to server...", 1,  white)
    

    score_a = 0
    score_b = 0
    if player_flag == None:
        print("Not connected to server")
        win.blit(text2,  (width / 2 - text2.get_width() / 2, height * 0.2))
    else:
        player = int(n.getP())
        print("You are player", player)
        run = True

    while run:
        clock.tick(60)
        try:
            game = n.send("get")
        except:
            run = False
            print("Couldn't get game")
            break
        
        if game.bothWent():
            draw_rps_win(win, game, player, score_a, score_b)
            
            if player == 0:
                if game.get_player_move(0) == "Rock":
                    win.blit( PLAYER_ROCK_IMAGE, (0, height/2 - height*0.2))
                elif game.get_player_move(0) == "Paper":
                    win.blit( PLAYER_PAPER_IMAGE, (0, height/2 - height*0.2))
                elif game.get_player_move(0) == "Scissors":
                    win.blit( PLAYER_SCISSORS_IMAGE, (0, height/2 - height*0.2))

                if game.get_player_move(1) == "Rock":
                    win.blit( OPPONENT_ROCK_IMAGE, (width*0.6 , height/2 - height*0.2))
                elif game.get_player_move(1) == "Paper":
                    win.blit( OPPONENT_PAPER_IMAGE, (width*0.6 , height/2 - height*0.2))
                elif game.get_player_move(1) == "Scissors":
                    win.blit( OPPONENT_SCISSORS_IMAGE, (width*0.6 , height/2 - height*0.2))

            if player == 1:
                if game.get_player_move(1) == "Rock":
                    win.blit( PLAYER_ROCK_IMAGE, (0, height/2 - height*0.2))
                elif game.get_player_move(1) == "Paper":
                    win.blit( PLAYER_PAPER_IMAGE, (0, height/2 - height*0.2))
                elif game.get_player_move(1) == "Scissors":
                    win.blit( PLAYER_SCISSORS_IMAGE, (0, height/2 - height*0.2))

                if game.get_player_move(0) == "Rock":
                    win.blit( OPPONENT_ROCK_IMAGE, (width*0.6, height/2 - height*0.2))
                elif game.get_player_move(0) == "Paper":
                    win.blit( OPPONENT_PAPER_IMAGE, (width*0.6 , height/2 - height*0.2))
                elif game.get_player_move(0) == "Scissors":
                    win.blit( OPPONENT_SCISSORS_IMAGE, (width*0.6, height/2 - height*0.2))

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
                result = ""

                # Show message before resetting the scores
                if score_b > score_a:
                    text = font.render("You Won!", 1,  Electric_Green)
                    result = "win"  # Use = instead of +=
                elif score_a > score_b:
                    text = font.render("You Lost...", 1,  Dark_Red)
                    result = "lose"  # Use = instead of +=

                # Display the result
                win.blit( RECTANGLE, (0, 0))
                win.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
                pygame.display.update()  # Update the display to show the result

                # Update and save user stats
                update_user_rps_stats(stats, result)
                save_user_stats(username, stats)

                # Reset scores after the message is shown and stats are updated
                score_a = score_b = 0

            pygame.display.update()
            pygame.time.delay(1000)

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
                    run = False
                    main_menu(server)

        draw_rps_win(win, game, player, score_a, score_b)

#shooter game
def shooter(server):
    red = pygame.Rect(1020, 360,  SPACESHIP_width,  SPACESHIP_height)
    yellow = pygame.Rect(200, 360,  SPACESHIP_width,  SPACESHIP_height)

    red_bullets = []
    yellow_bullets = []

    red_health = 10
    yellow_health = 10

    clock = pygame.time.Clock()
    SPACE_BGM.play(-1)  # Loop the background music indefinitely
    SPACE_BGM.set_volume(0.5)  # Lower background music volume


    run = True
    while run:
        clock.tick( FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) <  MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height // 2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(red_bullets) <  MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height // 2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_ESCAPE:
                    red_health = yellow_health = 10
                    SPACE_BGM.stop()
                    run = False
                    main_menu(server)

            if event.type ==  RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type ==  YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow Wins!"
        if yellow_health <= 0:
            winner_text = "Red Wins!"

        if winner_text != "":
            WIN_SOUND.play()
            draw_winner(winner_text)
            update_user_shooter_stats(stats, winner_text)
            save_user_stats(username, stats)
            break

        keys_pressed = pygame.key.get_pressed()
        Shooter.yellow_handle_movement(keys_pressed, yellow)
        Shooter.red_handle_movement(keys_pressed, red)

        Shooter.handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_shooter_win(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)

    shooter()

def stats_win(server):
    clock = pygame.time.Clock()
    
    run = True
    while run:
        clock.tick( FPS)
        stats = load_user_stats(username)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    main_menu(server)
        
        draw_stats_win(win, stats)
    stats_win()

# def wordler(server):
#     game = Wordler(exit_to_menu_callback=lambda: main_menu(server))
#     run = True
#     while run:
#         game.new()
#         game.run()



def main_menu(server):
    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(60)
        win.fill(BGCOLOUR)

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        RPS_BUTTON = mainButton(image=None, pos=(640, 250), 
                            text_input="Rock Paper Scissors", font=get_font(50), base_color= THE_OTHER_BLUE, hovering_color= white)
        SHOOTER_BUTTON = mainButton(image=None, pos=(640, 360), 
                            text_input="SHOOTER", font=get_font(50), base_color= THE_OTHER_BLUE, hovering_color= white)
        STATS_BUTTON = mainButton(image=None, pos=(640, 470), 
                            text_input="STATS", font=get_font(50), base_color= THE_OTHER_BLUE, hovering_color= white)
        # WORDLER_BUTTON = mainButton(image=None, pos=(960, 390), 
        #                     text_input="WORDLER", font=get_font(65), base_color= THE_OTHER_BLUE, hovering_color= white)
        QUIT_BUTTON = mainButton(image=None, pos=(640, 580), 
                            text_input="QUIT", font=get_font(70), base_color= Dark_Red, hovering_color= white)
        

        win.blit(MENU_TEXT, MENU_RECT)

        for button in [RPS_BUTTON, SHOOTER_BUTTON, STATS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(win)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if RPS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    rps(server)
                if SHOOTER_BUTTON.checkForInput(MENU_MOUSE_POS):
                    shooter(server)
                if STATS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    stats_win(server)
                # if WORDLER_BUTTON.checkForInput(MENU_MOUSE_POS):
                #     wordler(server)
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    run = False 

        pygame.display.update()

while True:
    username, stats, found_server = login(win)

    main_menu(found_server)   