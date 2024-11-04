import pygame
from constants import *
from user_management import load_user_stats
from button import Button
from constants import win

btns = [Button("Rock", 470, 600,  Pale_Lavender), Button("Paper", 590, 600,  Pale_Lavender), Button("Scissors", 710, 600,  Pale_Lavender)]

def draw_rps_win(win, game, p, score_a, score_b):
    win.fill( BGCOLOUR)
    
    if not(game.connected()):
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Waiting for Player...", 1,  white)
        win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
    else:
        win.blit( BACKGROUND_TITLE,(width/2 -  BACKGROUND_TITLE.get_width()/2, height/2 -  BACKGROUND_TITLE.get_height()/2))
        font = pygame.font.SysFont("comicsans", 40)
        text = font.render("Your Move", 1,  Mint_Green)
        win.blit(text, (width/4 - text.get_width()/2, 100))
        text = font.render("Opponents", 1,  Mint_Green)
        win.blit(text, (width*0.75 - text.get_width()/2, 100))
        Player0_score = font.render(f"Score: {score_a}", 1,  white)
        Player1_score = font.render(f"Score: {score_b}", 1,  white)
        win.blit(Player0_score, (width - Player0_score.get_width() - 10, 10))
        win.blit(Player1_score, (10, 10))
        move1 = game.get_player_move(0)
        move2 = game.get_player_move(1)
        if game.bothWent():
            text1 = font.render(move1, 1,  white)
            text2 = font.render(move2, 1,  white)
        else:
            if game.p1Went and p == 0:
                text1 = font.render(move1, 1,  white)
            elif game.p1Went:
                text1 = font.render("Locked In", 1,  Mint_Green)
            else:
                text1 = font.render("Waiting...", 1,  Mint_Green)
            if game.p2Went and p == 1:
                text2 = font.render(move2, 1,  white)
            elif game.p2Went:
                text2 = font.render("Locked In", 1,  Mint_Green)
            else:
                text2 = font.render("Waiting...", 1,  Mint_Green)
        if p == 1:
            win.blit(text2, (width/4 - text.get_width()/2, 520))
            win.blit(text1, (width*0.75 - text.get_width()/2, 520))
        else:
            win.blit(text1, (width/4 - text.get_width()/2, 520))
            win.blit(text2, (width*0.75 - text.get_width()/2, 520))
        for btn in btns:
            btn.draw(win)
    pygame.display.update()

def draw_stats_win(win, stats):
    win.fill(BGCOLOUR)
    header_font = pygame.font.SysFont("comicsans", 60)
    stats_font = pygame.font.SysFont("comicsans", 40)
    text = header_font.render("RPS", 1,  white)
    win.blit(text, (width/4 - text.get_width()/2, 100))
    text = header_font.render("Shooter", 1,  white)
    win.blit(text, (width*0.75 - text.get_width()/2, 100))
    rps_total_games = stats_font.render(f"Total Games: {stats['rps_total_games']}", 1,  white)
    win.blit(rps_total_games, (width/4 - text.get_width()/2, 200))
    rps_wins = stats_font.render(f"Wins: {stats['rps_wins']}", 1,  white)
    win.blit(rps_wins, (width/4 - text.get_width()/2, 300))
    rps_losses = stats_font.render(f"Losses: {stats['rps_losses']}", 1,  white)
    win.blit(rps_losses, (width/4 - text.get_width()/2, 400))
    rps_win_rate = stats_font.render(f"Win Rate: {stats['rps_win_rate']}", 1,  white)
    win.blit(rps_win_rate, (width/4 - text.get_width()/2, 500))
    rps_loss_rate = stats_font.render(f"Loss Rate: {stats['rps_loss_rate']}", 1,  white)
    win.blit(rps_loss_rate, (width/4 - text.get_width()/2, 600))
    shooter_total_games = stats_font.render(f"Total Games: {stats['shooter_total_games']}", 1,  white)
    win.blit(shooter_total_games, (width*0.75 - text.get_width()/2, 300))
    shooter_red_wins = stats_font.render(f"Red Wins: {stats['shooter_red_wins']}", 1,  white)
    win.blit(shooter_red_wins, (width*0.75 - text.get_width()/2, 400))
    shooter_yellow_wins = stats_font.render(f"Yellow Wins: {stats['shooter_yellow_wins']}", 1,  white)
    win.blit(shooter_yellow_wins, (width*0.75 - text.get_width()/2, 500))
    pygame.display.update()

def draw_shooter_win(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    win.blit( SPACE, (0, 0))
    pygame.draw.rect(win,  black,  BORDER)
    win.blit( YELLOW_SPACESHIP, (yellow.x, yellow.y))
    win.blit( RED_SPACESHIP, (red.x, red.y))
    # Display health
    red_health_text =  HEALTH_FONT.render(f"Health: {red_health}", 1,  white)
    yellow_health_text =  HEALTH_FONT.render(f"Health: {yellow_health}", 1,  white)
    win.blit(red_health_text, (width - red_health_text.get_width() - 10, 10))
    win.blit(yellow_health_text, (10, 10))
    # Draw bullets
    for bullet in red_bullets:
        pygame.draw.rect(win,  RED, bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(win,  YELLOW, bullet)
    pygame.display.update()

def draw_winner(text):
    draw_text =  WINNER_FONT.render(text, 1,  white)
    win.blit(draw_text, (width / 2 - draw_text.get_width() // 2, height / 2 - draw_text.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(5000)
